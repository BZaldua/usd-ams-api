from typing import Optional

from sqlalchemy.future import select

from app.infrastructure.database import Asset, Publish, Task
from app.infrastructure.repositories.base import BaseRepository


class PublishRepository(BaseRepository):
    async def get_latest_version(self, asset_id: int, task_id: int) -> int:
        query = (
            select(Publish.version)
            .where(Publish.asset_id == asset_id, Publish.task_id == task_id)
            .order_by(Publish.version.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        latest = result.scalars().first()
        return latest if latest is not None else 0

    async def get_latest_publish_path(
        self, asset_name: str, task_name: str
    ) -> Optional[str]:
        query = (
            select(Publish.fs_path)
            .join(Asset, Publish.asset_id == Asset.id)
            .join(Task, Publish.task_id == Task.id)
            .where(Asset.name == asset_name, Task.name == task_name)
            .order_by(Publish.version.desc())
            .limit(1)
        )
        result = await self.publish: Publish.execute(query)
        return result.scalars().first()
