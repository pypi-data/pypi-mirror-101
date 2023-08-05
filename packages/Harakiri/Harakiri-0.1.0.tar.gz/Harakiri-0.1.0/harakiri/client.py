from typing import Any, Dict, Optional
import aiohttp
from harakiri.model import (
    SkillData,
    AllSkillsData,
    GalleryPost,
    GalleryList,
)


class Client:
    @staticmethod
    async def get(path: str, params: Optional[Dict[str, Any]] = None):
        url = "http://manjiapi.ombe.xyz/api" + path
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as resp:
                return await resp.json()

    async def skill_data(self, num: int) -> SkillData:
        return SkillData(**await self.get(f"/skill/{num}"))

    async def all_skills_data(self) -> AllSkillsData:
        return AllSkillsData(**await self.get("/skill/all"))

    async def gallery_post(self, num: int) -> GalleryPost:
        return GalleryPost(**await self.get(f"/gallery/view/{num}"))

    async def gallery_todaytip(self, page: Optional[int] = 1) -> GalleryList:
        return GalleryList(**await self.get(f"/gallery/tt/lists/{page}"))

    async def gallery_search(
        self,
        keyword: str,
        search_mode: Optional[str] = "search_subject_memo",
        page: Optional[int] = 1,
    ):
        """
        search_mode list: search_subject_memo, search_subject, search_memo, search_name
        """
        return GalleryList(
            **await self.get(
                "/gallery/search",
                params={"keyword": keyword, "search_mode": search_mode, "page": page},
            )
        )
