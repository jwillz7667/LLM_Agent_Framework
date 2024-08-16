# core/exceptions.py

class APIKeyError(Exception):
    """Raised when there is an issue with the API Key."""
    pass

class RateLimitExceededError(Exception):
    """Raised when the rate limit is exceeded for a provider."""
    pass

class ProviderNotSupportedError(Exception):
    """Raised when a provider is not supported by the system."""
    pass

class InvalidEnvironmentError(Exception):
    """Raised when an invalid environment is detected."""
    pass
