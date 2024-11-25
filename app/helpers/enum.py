import enum


class UserRole(enum.Enum):
    ADMIN = 'admin'
    GUEST = 'guest'
    MANAGER_FULL_ACCESS = 'manager'
    MANAGER_UPDATE = 'manager-update'

class UserRoleRequest(str, enum.Enum):
    ADMIN = 'admin'
    GUEST = 'guest'
    MANAGER_FULL_ACCESS = 'manager'
    MANAGER_UPDATE = 'manager-update'