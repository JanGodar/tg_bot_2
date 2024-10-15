import asyncio
import logging
from aiogram import Bot, Dispatcher
from environs import Env
from config_data.config import load_config
from handlers import other_handlers, user_handlers
from storage.nats_storage import NatsStorage
from utils.nats_connect import connet_to_nats


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {name} - {message}',
        style='{'
    )

    logger.debug('Starting bot')
    
    config = load_config()

    nc, js = await connet_to_nats(servers=config.nats.servers)

    storage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(
        token=config.tg_bot.token
    )
    dp = Dispatcher(storage=storage)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info('Connection to NATS closed')


asyncio.run(main())