from typing import Any, Iterator, List


class SkillInfo:
    def __init__(self, **data: Any) -> None:
        self.__command = data["Command"]
        self.__hit_level = data["Hit level"]
        self.__damage = data["Damage"]
        self.__startup_frame = data["Start up frame"]
        self.__block_frame = data["Block frame"]
        self.__hit_frame = data["Hit frame"]
        self.__counter_hit_frame = data["Counter hit frame"]
        self.__notes = data["Notes"]

    @property
    def command(self) -> str:
        return self.__command

    @property
    def hit_level(self) -> str:
        return self.__hit_level

    @property
    def damage(self) -> str:
        return self.__damage

    @property
    def start_up_frame(self) -> str:
        return self.__startup_frame

    @property
    def block_frame(self) -> str:
        return self.__block_frame

    @property
    def hit_frame(self) -> str:
        return self.__hit_frame

    @property
    def counter_hit_frame(self) -> str:
        return self.__counter_hit_frame

    @property
    def notes(self) -> str:
        return self.__notes


class SkillData:
    def __init__(self, **data: Any) -> None:
        self.__status = data["status"]
        self.__info = data["info"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def info(self) -> SkillInfo:
        return SkillInfo(**self.__info)


class AllSkillsData:
    def __init__(self, **data: Any) -> None:
        self.__status = data["status"]
        self.__skill_list = data["skill_list"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def skill_list(self) -> Iterator[SkillInfo]:
        for skill in self.__skill_list:
            yield SkillInfo(**skill)


class GalleryPost:
    def __init__(self, **data: Any) -> None:
        self.__status = data["status"]
        self.__title = data["content"]["title"]
        self.__auhor = data["content"]["auhor"]
        self.__content = data["content"]["content"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def title(self) -> str:
        return self.__title

    @property
    def author(self) -> str:
        return self.__auhor

    @property
    def content(self) -> List[str]:
        return self.__content


class ListsPostInfo:
    def __init__(self, **data: Any) -> None:
        self.__id = data["id"]
        self.__title = data["title"]
        self.__writer = data["writer"]
        self.__date = data["date"]
        self.__recommend = data["recommend"]
        self.__reply = data["reply"]
        self.__views = data["views"]

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def writer(self) -> str:
        return self.__writer

    @property
    def date(self) -> str:
        return self.__date

    @property
    def recommend(self) -> int:
        return self.__recommend

    @property
    def reply(self) -> int:
        return self.__reply

    @property
    def views(self) -> int:
        return self.__views


class GalleryList:
    def __init__(self, **data: Any) -> None:
        self.__status = data["status"]
        self.__total = data["total"]
        self.__lists = data["lists"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def total(self) -> int:
        return self.__total

    @property
    def lists(self) -> Iterator[ListsPostInfo]:
        for post in self.__lists:
            yield ListsPostInfo(post)
