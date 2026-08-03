from unittest.mock import AsyncMock

import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api.v1.endpoints import asset_router, task_router
from app.api.v1.mappers import AssetMapper, TaskMapper
from app.services import AssetService, PublishService, TaskService


class APIV1TestProvider(Provider):
    def __init__(
        self,
        task_mock: AsyncMock,
        asset_mock: AsyncMock,
        publish_mock: AsyncMock,
        task_mapper_mock: AsyncMock,
        asset_mapper_mock: AsyncMock,
    ):
        super().__init__()
        self._task_mock = task_mock
        self._asset_mock = asset_mock
        self._publish_mock = publish_mock
        self._task_mapper_mock = task_mapper_mock
        self._asset_mapper_mock = asset_mapper_mock

    @provide(scope=Scope.REQUEST)
    def get_task_service(self) -> TaskService:
        return self._task_mock

    @provide(scope=Scope.REQUEST)
    def get_asset_service(self) -> AssetService:
        return self._asset_mock

    @provide(scope=Scope.REQUEST)
    def get_publish_service(self) -> PublishService:
        return self._publish_mock

    @provide(scope=Scope.APP)
    def get_task_mapper_mock(self) -> TaskMapper:
        return self._task_mapper_mock

    @provide(scope=Scope.APP)
    def get_asset_mapper_mock(self) -> AssetMapper:
        return self._asset_mapper_mock


@pytest.fixture
def task_service_mock():
    return AsyncMock(spec=TaskService)


@pytest.fixture
def asset_service_mock():
    return AsyncMock(spec=AssetService)


@pytest.fixture
def publish_service_mock():
    return AsyncMock(spec=PublishService)


@pytest.fixture
def task_mapper_mock():
    return AsyncMock(spec=TaskMapper)


@pytest.fixture
def asset_mapper_mock():
    return AsyncMock(spec=AssetMapper)


@pytest.fixture
async def client(
    task_service_mock,
    asset_service_mock,
    publish_service_mock,
    task_mapper_mock,
    asset_mapper_mock,
):
    app = FastAPI()

    app.include_router(task_router)
    app.include_router(asset_router)

    provider = APIV1TestProvider(
        task_service_mock,
        asset_service_mock,
        publish_service_mock,
        task_mapper_mock,
        asset_mapper_mock,
    )
    container = make_async_container(provider)
    setup_dishka(container, app)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as cl:
        yield cl

    await container.close()
