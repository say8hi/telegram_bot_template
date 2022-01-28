from dataclasses import dataclass

from environs import Env


@dataclass
class TelethonConfig:
    api_id: int
    api_hash: str


@dataclass
class TgBot:
    token: str
    admins: list
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    telethon: TelethonConfig


def load_config():
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admins=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("use_redis"),
        ),
        telethon=TelethonConfig(
            api_id=env.str("api_id"),
            api_hash=env.str("api_hash")
        ),
    )
