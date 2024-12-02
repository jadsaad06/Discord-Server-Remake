from enum import Enum

# Enum for defining permissions
class Permission(Enum):
    POST_MESSAGE = "post_message"
    VIEW_FEED = "view_feed"
    CREATE_CHANNEL = "create_channel"
    DELETE_CHANNEL = "delete_channel"
    ADD_USER = "add_user"
    REMOVE_USER = "remove_user"
    SCAN_CONTENT = "scan_content"

# Base class
class Member:
    def __init__(self, name: str):
        self._name = name
        self.__permissions = []

    def hasPermission(self, permission):
        return permission in self.__permissions

# Derived class: Admin
class Admin(Member):
    def __init__(self, name: str):
        super().__init__(name)
        self.__permissions = [
            Permission.CREATE_CHANNEL,
            Permission.DELETE_CHANNEL,
            Permission.ADD_USER,
            Permission.REMOVE_USER,
            Permission.POST_MESSAGE,
            Permission.VIEW_FEED,
        ]
    

# Derived class: User
class User(Member):
    def __init__(self, name: str):
        super().__init__(name)
        self.__permissions = [
            Permission.POST_MESSAGE,
            Permission.VIEW_FEED,
        ]

# Derived class: Bot
class Bot(Member):
    def __init__(self, name: str):
        super().__init__(name)
        self.__permissions = [Permission.SCAN_CONTENT]

