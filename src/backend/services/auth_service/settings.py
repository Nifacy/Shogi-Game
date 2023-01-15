from pydantic import BaseSettings, AmqpDsn, Field, PostgresDsn


class ServiceSettings(BaseSettings):
	amqp_dsn: AmqpDsn = Field(..., env='AMQP_DSN')
	postgres_dsn: PostgresDsn = Field(..., env='POSTGRES_DSN')


settings = ServiceSettings()