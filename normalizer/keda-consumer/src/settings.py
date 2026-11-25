from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: str
    group: str
    sasl_username: str
    sasl_password: str
    raw_events_topic: str
    normalized_events_topic: str

    model_config = SettingsConfigDict(env_prefix="kafka_")

    @property
    def consumer_config(self) -> dict[str, str]:
        config = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group,
            "auto.offset.reset": "earliest",
            "security.protocol": "SASL_PLAINTEXT",
            "sasl.mechanism": "SCRAM-SHA-256",
            "sasl.username": self.sasl_username,
            "sasl.password": self.sasl_password,
        }
        return config


class Settings(BaseSettings):
    kafka: KafkaSettings = Field(default_factory=lambda: KafkaSettings())  # type: ignore[call-arg]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
