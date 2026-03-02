from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

URL_TS = settings.URL_TS
URL_VS = settings.URL_VS

async_engine_ts = create_async_engine(URL_TS, pool_pre_ping=True,
            pool_recycle=1800,
            echo=True,
            connect_args={
               "command_timeout": 10,  # Таймаут выполнения команды (5 сек)
               "timeout": 15  # Таймаут на само подключение
            }
           )

AsyncSessionTs = async_sessionmaker(bind=async_engine_ts)

async_engine_driver_license = create_async_engine(
    URL_VS,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=True,
    connect_args={
       "command_timeout": 5,  # Таймаут выполнения команды (5 сек)
       "timeout": 10  # Таймаут на само подключение
    })

AsyncSessionVS = async_sessionmaker(bind=async_engine_driver_license)

class Base(DeclarativeBase):
    pass