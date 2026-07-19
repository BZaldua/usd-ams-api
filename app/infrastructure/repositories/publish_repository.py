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

    async def create(
        self, asset_id: int, task_id: int, version: int, fs_path: str, author: str
    ) -> Publish:
        db_publish = Publish(
            asset_id=asset_id,
            task_id=task_id,
            version=version,
            fs_path=fs_path,
            author=author,
        )
        self.db.add(db_publish)
        await self.db.flush()
        return db_publish

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
        result = await self.db.execute(query)
        return result.scalars().first()
