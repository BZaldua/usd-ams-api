from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import AssetModel, PublishModel, TaskModel
from app.infrastructure.repositories.base import BaseRepository


class PublishRepository(BaseRepository[PublishModel]):
    async def get_latest_version(self, asset_id: int, task_id: int) -> int:
        query = (
            select(PublishModel.version)
            .where(PublishModel.asset_id == asset_id, PublishModel.task_id == task_id)
            .order_by(PublishModel.version.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        latest = result.scalars().first()
        return latest if latest is not None else 0

    async def get_latest_publish_path(
        self, asset_name: str, task_name: str
    ) -> Optional[str]:
        query = (
            select(PublishModel.fs_path)
            .join(AssetModel, PublishModel.asset_id == AssetModel.id)
            .join(TaskModel, PublishModel.task_id == TaskModel.id)
            .where(AssetModel.name == asset_name, TaskModel.name == task_name)
            .order_by(PublishModel.version.desc())
            .limit(1)
        )
        result: PublishModel = await self.db.execute(query)
        return result.scalars().first()
