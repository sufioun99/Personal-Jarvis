"""
Safe Linux Command Executor with security checks
"""
import asyncio
import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class SafeCommandExecutor:
    """
    Execute Linux commands with safety checks
    """
    
    # Dangerous commands that should be blocked in safe mode
    DANGEROUS_COMMANDS = [
        "rm -rf /",
        "mkfs",
        "dd if=",
        ":(){ :|:& };:",  # Fork bomb
        "> /dev/sda",
        "mv /home",
        "chmod -R 777 /",
        "wget.*|.*sh",  # Downloading and piping to shell
        "curl.*|.*sh",
    ]
    
    # Commands that require extra caution
    CAUTIOUS_COMMANDS = [
        "rm",
        "rmdir",
        "mv",
        "chmod",
        "chown",
        "kill",
        "pkill",
        "shutdown",
        "reboot",
        "systemctl",
        "service",
    ]
    
    def __init__(self):
        logger.info("Safe command executor initialized")
    
    async def execute(
        self,
        command: str,
        safe_mode: bool = True,
        timeout: int = 30
    ) -> Dict:
        """
        Execute a Linux command with safety checks
        
        Args:
            command: Command to execute
            safe_mode: Enable safety checks
            timeout: Command timeout in seconds
        
        Returns:
            Dictionary with success status, output, and error
        """
        try:
            # Safety checks
            if safe_mode:
                is_safe, reason = self._check_safety(command)
                if not is_safe:
                    return {
                        "success": False,
                        "output": "",
                        "error": f"Command blocked for safety: {reason}"
                    }
            
            logger.info(f"Executing command: {command[:100]}...")
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='replace')
                error = stderr.decode('utf-8', errors='replace')
                
                success = process.returncode == 0
                
                return {
                    "success": success,
                    "output": output,
                    "error": error if not success else None,
                    "return_code": process.returncode
                }
                
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": f"Command timed out after {timeout} seconds"
                }
                
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    def _check_safety(self, command: str) -> tuple:
        """
        Check if command is safe to execute
        
        Returns:
            Tuple of (is_safe, reason)
        """
        # Check for dangerous commands
        for dangerous in self.DANGEROUS_COMMANDS:
            if re.search(dangerous, command, re.IGNORECASE):
                return False, f"Contains dangerous pattern: {dangerous}"
        
        # Check for cautious commands
        for cautious in self.CAUTIOUS_COMMANDS:
            if re.search(r'\b' + re.escape(cautious) + r'\b', command):
                # Extra validation for cautious commands
                if not self._validate_cautious_command(command, cautious):
                    return False, f"Potentially dangerous use of: {cautious}"
        
        return True, "Command appears safe"
    
    def _validate_cautious_command(self, command: str, cmd: str) -> bool:
        """Validate cautious commands have safe parameters"""
        
        if cmd == "rm":
            # Block rm with -rf on root or system directories
            if re.search(r'rm.*-[rf].*(/|/usr|/etc|/var|/bin|/sbin)', command):
                return False
        
        if cmd in ["chmod", "chown"]:
            # Block recursive operations on root
            if re.search(r'(chmod|chown).*-R.*/($|[^/])', command):
                return False
        
        if cmd in ["shutdown", "reboot"]:
            # Allow but log
            logger.warning(f"System command detected: {cmd}")
        
        return True
    
    def get_safe_command_info(self) -> Dict:
        """Get information about command safety features"""
        return {
            "safe_mode": "enabled",
            "blocked_patterns": len(self.DANGEROUS_COMMANDS),
            "cautious_commands": len(self.CAUTIOUS_COMMANDS),
            "features": [
                "Pattern-based blocking",
                "Timeout protection",
                "Output capture",
                "Error handling"
            ]
        }
