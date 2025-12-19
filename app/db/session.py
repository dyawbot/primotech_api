from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings
from app.model.declarativebase.base import PrimoUserBase, ExternalUserbase, WeBudgetBase




# Cache so we don’t re-create engines every request
_engine_cache = {}
_session_cache = {}
MODEL_REGISTRY = {
    "primoUser": PrimoUserBase.metadata,
    "externalUser": ExternalUserbase.metadata,
    "webudget": WeBudgetBase.metadata,
}

# DB_MODELS = {
#     db_name: MODEL_REGISTRY[alias]
#     for db_name, alias in settings.db_schemas.items()
# }


def get_engine(db_name: str):
    if db_name not in _engine_cache:
        url = settings.build_db_url(db_name)
        _engine_cache[db_name] = create_async_engine(
            url,
            echo=True, 
            pool_size=5, 
            max_overflow=10,
            pool_timeout=30, 
            pool_recycle=1800)
        
    return _engine_cache[db_name]

def get_sessionmaker(db_name: str):
    if db_name not in _session_cache:
        engine = get_engine(db_name)
        _session_cache[db_name] = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=engine, 
            class_=AsyncSession)
    return _session_cache[db_name]

# engine = create_async_engine(settings.DATABASE_URL,echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)




#ENGINES
# engine = create_async_engine(settings.DATABASE_URL,echo=True)
# webudget_engine = create_async_engine(settings.DB_WEBUDGET_URL, echo=True)


#SESSION MAKERS
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# session_webudget = sessionmaker(autocommit=False, autoflush=False, bind=webudget_engine, class_=AsyncSession)





