class AppModuleException(Exception):
    """Base exception class for all app exceptions"""

    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppModuleException):
    """Base exception class for not found exceptions"""

    status_code = 404


class AssetNotFoundException(NotFoundException):
    """Business exception when Asset does not exist"""

    def __init__(self, asset_id: int):
        super().__init__(f"Asset ID={asset_id} does not exist")


class TaskNotFoundException(NotFoundException):
    """Business exception when Task does not exist"""

    def __init__(self, task_id: int):
        super().__init__(f"Task ID={task_id} does not exist")


class NoFilteredContentFoundException(NotFoundException):
    """Business exception when some expected value is not found"""

    def __init__(self):
        super().__init__("Requested filtered content foud")
