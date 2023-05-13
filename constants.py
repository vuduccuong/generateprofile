import enum

FILE_TYPES = (
    ("ZIP file", ".zip"),
    ("Tất cả", ".*"),
)


class BrowserType:
    CHROME = "Chrome"
    FIREFOX = "Fire Fox"
    EDGE_DEV = "Edge Dev"

    @classmethod
    def is_chrome(cls, type: str) -> bool:
        return type == cls.CHROME

    @classmethod
    def to_list(cls):
        return [cls.CHROME, cls.FIREFOX, cls.EDGE_DEV]


class CreateType:
    CREATE_NEW_PROFILE = 1
    ADD_PROFILE = 2

    @classmethod
    def is_create_new(cls, action_type: int) -> bool:
        return action_type == cls.CREATE_NEW_PROFILE

    @classmethod
    def is_add_profile(cls, action_type: int) -> bool:
        return action_type == cls.ADD_PROFILE
