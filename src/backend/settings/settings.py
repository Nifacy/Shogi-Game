from pydantic import BaseSettings, AmqpDsn, PostgresDsn, Field


class ProjectSettings(BaseSettings):
    amqp_dsn: AmqpDsn = Field(..., env='AMQP_DSN')
    postgres_dsn: PostgresDsn = Field(..., env='POSTGRES_DSN')

    class Config:
        env_file = 'C:/Users/alexg/OneDrive/Рабочий стол/Python/Shogi-Game/file.env'
        env_file_encoding = 'utf-8'
