from unittest.mock import MagicMock

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.exceptions import app_module_exception_handler, init_exception_handlers
from app.exceptions import AppModuleException


class DummyAppException(AppModuleException):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def test_app_module_exception_handler_returns_correct_json_and_status():
    # Arrange
    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"
    mock_request.url.path = "/api/v1/test"

    exc = DummyAppException(status_code=404, message="Content not found")

    # Act
    response = app_module_exception_handler(mock_request, exc)

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404

    import json

    body = json.loads(response.body.decode("utf-8"))

    assert body["detail"] == "Content not found"
    assert body["error_code"] == "DummyAppException"


def test_app_module_exception_handler_logs_warning(mocker):
    # Arrange
    mock_request = MagicMock(spec=Request)
    mock_request.method = "POST"
    mock_request.url.path = "/api/v1/resource"

    exc = DummyAppException(status_code=400, message="Invalid business rule")

    mock_logger = mocker.patch("app.api.exceptions.logger")

    # Act
    app_module_exception_handler(mock_request, exc)

    # Assert
    expected_log_message = "Error 400 en POST /api/v1/resource -> Invalid business rule"
    mock_logger.warning.assert_called_once_with(expected_log_message)


def test_init_exception_handlers_registers_handler_in_fastapi():
    # Arrange
    mock_app = MagicMock(spec=FastAPI)

    # Act
    init_exception_handlers(mock_app)

    # Assert
    mock_app.add_exception_handler.assert_called_once_with(
        AppModuleException, app_module_exception_handler
    )
