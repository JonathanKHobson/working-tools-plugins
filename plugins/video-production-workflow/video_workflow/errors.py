class VideoWorkflowError(RuntimeError):
    """Base error for workflow failures."""


class ManifestError(VideoWorkflowError):
    """Raised when a project manifest is invalid."""


class ToolMissingError(VideoWorkflowError):
    """Raised when an external command is required but unavailable."""
