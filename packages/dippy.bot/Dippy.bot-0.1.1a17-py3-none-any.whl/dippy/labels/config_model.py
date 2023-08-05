from pydantic import BaseSettings, Field


class DatabaseConfigModel(BaseSettings):
    engine: str = Field("sqlite+pysqlite", env="ENGINE")
    host: str = Field("", env="HOST")
    username: str = Field("", env="USERNAME")
    password: str = Field("", env="PASSWORD")
    database: str = Field("", env="DATABASE")

    class Config:
        env_prefix = "DIPPY_DB_"


class LabelConfigModel(BaseSettings):
    storage: str = Field("memory", env="STORAGE")
    database: DatabaseConfigModel = DatabaseConfigModel()

    class Config:
        env_prefix = "DIPPY_LABEL_"
