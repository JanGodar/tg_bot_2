from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class Fid:
    fid: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    fid: Fid


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        fid=Fid(fid=env('FID_VALUE'))
    )