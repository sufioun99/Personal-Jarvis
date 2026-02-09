# Contributing to JARVIS

We love your input! We want to make contributing to JARVIS as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the existing style.
6. Issue that pull request!

## Code Style

* Use Python 3.8+ features
* Follow PEP 8 style guide
* Use type hints where appropriate
* Add docstrings to all functions and classes
* Keep functions focused and modular
* Write descriptive variable names

### Example:

```python
async def process_query(self, query: str, voice_output: bool = False) -> Dict[str, Any]:
    """
    Process user query and generate response
    
    Args:
        query: User query text
        voice_output: Whether to output response via voice
        
    Returns:
        Response dictionary with result and metadata
    """
    # Implementation
    pass
```

## Testing

* Write unit tests for new features
* Ensure existing tests pass
* Aim for high code coverage
* Test edge cases

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

## Adding New Features

### New AI Agent

1. Create agent class in `agents/specialized_agents.py`
2. Extend `BaseAgent`
3. Implement `execute()` method
4. Add to orchestrator in `agents/orchestrator.py`
5. Add tests
6. Update documentation

### New API Integration

1. Add method to `api/api_manager.py`
2. Add configuration to `config.py` and `.env.example`
3. Implement caching if appropriate
4. Add error handling
5. Add tests
6. Update documentation

### New Intent Type

1. Add to `IntentType` enum in `core/nlu.py`
2. Add patterns to `_build_intent_patterns()`
3. Add handler in `core/jarvis.py`
4. Add tests
5. Update documentation

## Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/sufioun99/Personal-Jarvis/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We use GitHub issues to track feature requests as well. When proposing a new feature:

- Explain the problem you're trying to solve
- Provide use cases
- Describe the proposed solution
- Consider alternatives
- Note any breaking changes

## Security Issues

If you discover a security vulnerability, please email the maintainers directly instead of using the issue tracker.

## Documentation

* Keep README.md up to date
* Update SETUP.md for installation changes
* Add inline comments for complex logic
* Update API documentation
* Add examples for new features

## Commit Messages

* Use clear and meaningful commit messages
* Start with a verb (Add, Fix, Update, Remove, etc.)
* Keep the first line under 50 characters
* Add detailed description if needed

Examples:
```
Add support for custom wake words
Fix command execution timeout issue
Update documentation for API integration
```

## Code Review Process

1. All submissions require review
2. We use GitHub pull requests for this purpose
3. Reviewers will check:
   - Code quality and style
   - Test coverage
   - Documentation
   - Security implications
   - Performance impact

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- GitHub contributors page

Thank you for contributing to JARVIS! 🎉
