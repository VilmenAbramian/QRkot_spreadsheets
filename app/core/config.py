from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Скотофонд'
    app_description: str = ('Сервис для сбора пожертвований'
                            'в фонд скотов и кашек')
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_found.db'

    class Config:
        env_file = ".env"


settings = Settings()