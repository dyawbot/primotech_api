from enum import Enum
from app.model.UserModels.users import Users, Images


class Tables(Enum):
    USER = Users
    IMAGES = Images

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progresss"
    COMPLETED = "completed"
    SUCCESS = "success"
    UPDATED = "updated"
    IERROR = "network error"
    OERROR = "system_error"
    