"""
Test configuration for pytest
"""
import pytest
import asyncio


# Note: Using session-scoped event loop for performance.
# This is safe for our test suite as tests don't have conflicting fixtures.
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
