class TerminalError(Exception):
    """Base exception for expected terminal failures."""


class ProviderError(TerminalError):
    """Base error returned by a market-data provider."""


class RetryableProviderError(ProviderError):
    """Temporary provider failure eligible for retry or fallback."""


class ProviderStaleError(RetryableProviderError):
    """Provider returned data that does not meet requested freshness."""


class AuthenticationError(ProviderError):
    """Bad/missing credential; must not be hidden by fallback."""


class PermissionDeniedError(ProviderError):
    """Credential lacks access; must not be hidden by fallback."""


class InvalidSymbolError(ProviderError):
    """Canonical symbol cannot be resolved by this provider."""

class UnknownSymbolError(InvalidSymbolError):
    """Canonical symbol is well-formed but absent from the local registry."""
    
class ConfigurationError(TerminalError):
    """Invalid local application configuration."""
