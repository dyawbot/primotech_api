from enum import Enum


class DBNames(Enum):

    PRIMOUSER = "user_db"
    DEV_DB_POSTGRES = "dev_db_postgres"
    EXTERNALUSER = "externalUser"
    WEBUDGET = "webudget_db"



# print(DBNames.WEBUDGET.value)  # Output: webudget