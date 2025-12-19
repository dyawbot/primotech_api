from logging.config import fileConfig

from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool
from app.model.we_budget.users_models import Users
from app.model.we_budget.user_device_models import UserDeviceModels
from app.model.we_budget.partner_models import PartnerModel
from app.model.we_budget.family_models import FamilyModels
from app.model.we_budget.family_member_models import FamilyMemberModels  
from app.model.we_budget.sync_log_models import SyncLogModels
from app.model.we_budget.category_model import CategoryModel
from app.model.we_budget.bank_accounts_model import BankAccountsModel
from app.model.we_budget.transactions_models import TrasactionsModels
from app.model.we_budget.recurring_transactions_model import RecurringTransactionModel
from app.model.we_budget.analytic_cache_model import AnalyticCacheModel
from app.model.declarativebase.base import WeBudgetBase
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = WeBudgetBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    DATABASE_URL = config.get_main_option("sqlalchemy.url")
    sync_url = DATABASE_URL.replace("+asyncpg", "")
    connectable = create_engine(sync_url, poolclass=pool.NullPool)
    
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
