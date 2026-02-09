"""
Linux Command Execution Engine with Safety Features
"""
import subprocess
import shlex
from typing import Optional, Tuple, List
import re
from config import settings
from utils.logger import logger


class CommandExecutor:
    """
    Executes Linux commands with safety checks and validation
    """
    
    # Dangerous commands that require confirmation
    DANGEROUS_COMMANDS = [
        "rm", "rmdir", "dd", "mkfs", "fdisk", "parted",
        "shred", "wipefs", "kill", "killall", "pkill",
        "> /dev/", "format", "del"
    ]
    
    # Commands that should never be executed
    BLACKLISTED_COMMANDS = [
        ":(){ :|:& };:",  # Fork bomb
        "rm -rf /",  # Delete everything
        "dd if=/dev/zero of=/dev/sda",  # Wipe disk
        "mkfs.ext4 /dev/sda",  # Format disk
    ]
    
    def __init__(self):
        """Initialize command executor"""
        self.whitelist = settings.whitelisted_commands if settings.command_whitelist else None
        self.enable_sudo = settings.enable_sudo
        self.require_confirmation = settings.require_confirmation
        logger.info(f"Command Executor initialized (sudo: {self.enable_sudo})")
    
    def is_safe_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Check if command is safe to execute
        
        Args:
            command: Command to validate
            
        Returns:
            Tuple of (is_safe, reason)
        """
        command_lower = command.lower().strip()
        
        # Check blacklist
        for blacklisted in self.BLACKLISTED_COMMANDS:
            if blacklisted in command_lower:
                return False, f"Command is blacklisted: {blacklisted}"
        
        # Check if sudo is disabled
        if not self.enable_sudo and command_lower.startswith("sudo"):
            return False, "sudo commands are disabled"
        
        # Check whitelist if enabled
        if self.whitelist:
            base_command = command_lower.split()[0]
            if base_command not in self.whitelist:
                return False, f"Command '{base_command}' not in whitelist"
        
        # Check for dangerous patterns
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                if self.require_confirmation:
                    return False, f"Dangerous command detected: {dangerous}. Confirmation required."
                logger.warning(f"Executing dangerous command: {command}")
        
        return True, None
    
    def parse_natural_language_command(self, nl_command: str) -> Optional[str]:
        """
        Convert natural language to Linux command
        
        Args:
            nl_command: Natural language command description
            
        Returns:
            Corresponding Linux command or None
        """
        nl_lower = nl_command.lower().strip()
        
        # Common command mappings
        mappings = [
            # File operations
            (r"list (all )?files", "ls -la"),
            (r"list files in (.+)", r"ls -la \1"),
            (r"show (current )?directory", "pwd"),
            (r"change to directory (.+)", r"cd \1"),
            (r"create directory (.+)", r"mkdir -p \1"),
            (r"remove (file|directory) (.+)", r"rm -r \2"),
            (r"copy (.+) to (.+)", r"cp -r \1 \2"),
            (r"move (.+) to (.+)", r"mv \1 \2"),
            (r"find files? named (.+)", r"find . -name '\1'"),
            
            # System information
            (r"show (disk|storage) usage", "df -h"),
            (r"show memory usage", "free -h"),
            (r"show (running )?processes", "ps aux"),
            (r"show system (info|information)", "uname -a"),
            (r"show uptime", "uptime"),
            (r"show network interfaces", "ip addr"),
            (r"show (current )?users", "who"),
            
            # Package management (apt-based)
            (r"install package (.+)", r"sudo apt-get install -y \1"),
            (r"update packages", "sudo apt-get update"),
            (r"upgrade packages", "sudo apt-get upgrade -y"),
            (r"remove package (.+)", r"sudo apt-get remove -y \1"),
            (r"search for package (.+)", r"apt-cache search \1"),
            
            # Process management
            (r"kill process (\d+)", r"kill \1"),
            (r"kill process named (.+)", r"pkill \1"),
            (r"restart service (.+)", r"sudo systemctl restart \1"),
            (r"start service (.+)", r"sudo systemctl start \1"),
            (r"stop service (.+)", r"sudo systemctl stop \1"),
            (r"(show )?status of service (.+)", r"sudo systemctl status \2"),
            
            # Network
            (r"check network connections", "netstat -tuln"),
            (r"test (connection|ping) to (.+)", r"ping -c 4 \2"),
            (r"download (.+)", r"wget \1"),
            (r"show (open )?ports", "sudo ss -tuln"),
            
            # File content
            (r"show (content of )?(file )?(.+)", r"cat \3"),
            (r"edit file (.+)", r"nano \1"),
            (r"search for '(.+)' in files", r"grep -r '\1' ."),
        ]
        
        # Try to match patterns
        for pattern, replacement in mappings:
            match = re.search(pattern, nl_lower)
            if match:
                if match.groups():
                    command = re.sub(pattern, replacement, nl_lower)
                else:
                    command = replacement
                logger.info(f"Translated '{nl_command}' to '{command}'")
                return command
        
        logger.warning(f"Could not translate command: {nl_command}")
        return None
    
    def execute_command(
        self, command: str, timeout: int = 30
    ) -> Tuple[bool, str, str]:
        """
        Execute a Linux command
        
        Args:
            command: Command to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        # Validate command safety
        is_safe, reason = self.is_safe_command(command)
        if not is_safe:
            logger.error(f"Command rejected: {reason}")
            return False, "", reason
        
        try:
            logger.info(f"Executing command: {command}")
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=None  # Use current environment
            )
            
            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            if success:
                logger.info(f"Command executed successfully")
                logger.debug(f"Output: {stdout}")
            else:
                logger.warning(f"Command failed with return code {result.returncode}")
                logger.debug(f"Error: {stderr}")
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout} seconds"
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    async def execute_with_llm_translation(
        self, natural_language_command: str, llm_router
    ) -> Tuple[bool, str, str]:
        """
        Execute command after translating with LLM
        
        Args:
            natural_language_command: Natural language description
            llm_router: LLM router for translation
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        # First try pattern-based translation
        command = self.parse_natural_language_command(natural_language_command)
        
        # If pattern matching fails, use LLM
        if not command:
            logger.info("Using LLM for command translation")
            prompt = f"""Convert this natural language command to a Linux shell command.
Only respond with the command itself, no explanations.

Natural language: {natural_language_command}

Linux command:"""
            
            try:
                command = await llm_router.generate_response(
                    prompt,
                    system_prompt="You are a Linux command expert. Convert natural language to shell commands.",
                    task_type="general",
                    temperature=0.1,
                    max_tokens=100
                )
                command = command.strip()
                logger.info(f"LLM translated to: {command}")
            except Exception as e:
                logger.error(f"LLM translation failed: {e}")
                return False, "", "Could not translate command"
        
        # Execute the translated command
        return self.execute_command(command)


# Global command executor instance
command_executor = CommandExecutor()
