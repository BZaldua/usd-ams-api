from dishka import Provider, Scope, provide
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from .api.v1.mappers import AssetMapper, TaskMapper
from .config.database import get_db
from .config.objejct_storage import ObjectStorageConfig
from .infrastructure.repositories import (
    AssetRepository,
    ObjectStorageRepository,
    PublishRepository,
    TaskRepository,
)
from .services import AssetService, PublishService, TaskService


class AppProvider(Provider):

    get_db_session = provide(get_db, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_asset_repository(self, db_session: AsyncSession) -> AssetRepository:
        return AssetRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_publish_repository(self, db_session: AsyncSession) -> PublishRepository:
        return PublishRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_object_storage_config(self) -> ObjectStorageConfig:
        return ObjectStorageConfig()

    @provide(scope=Scope.REQUEST)
    def get_object_storage_repository(
        self, config: ObjectStorageConfig
    ) -> ObjectStorageRepository:
        client = Minio(
            endpoint=config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.secure,
        )
        return ObjectStorageRepository(client, config.bucket_name)

    @provide(scope=Scope.REQUEST)
    def get_asset_service(self, repository: AssetRepository) -> AssetService:
        return AssetService(repository)

    @provide(scope=Scope.REQUEST)
    def get_task_service(self, repository: TaskRepository) -> TaskService:
        return TaskService(repository)

    @provide(scope=Scope.REQUEST)
    def get_publish_service(
        self,
        repository: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
        object_storage_repository: ObjectStorageRepository,
    ) -> PublishService:
        return PublishService(
            repository, asset_service, task_service, object_storage_repository
        )

    @provide(scope=Scope.APP)
    def get_task_mapper(self) -> TaskMapper:
        return TaskMapper()

    @provide(scope=Scope.APP)
    def get_asset_mapper(self, task_mapper: TaskMapper) -> AssetMapper:
        return AssetMapper(task_mapper=task_mapper)
