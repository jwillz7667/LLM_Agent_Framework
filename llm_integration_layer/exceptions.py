# llm_integration_layer/exceptions.py
class RateLimitExceededError(Exception):
    pass

class ProviderNotSupportedError(Exception):
    pass
