import requests
from aiogram import Router
from aiogram.filters import CommandStart, Command
from config_data.config import load_config


router = Router()

config = load_config()


@router.message(CommandStart())
async def process_command_start(message):
    await message.answer(f'Составляю отчеты по CRM')


@router.message(Command(commands=['new']))
async def process_new_command(message, state):
    await message.answer('Hello')
    r = requests.get(config.fid.fid)
    response_dict = r.json()
    await state.update_data(text_data=str(response_dict['data'][-1]))
    await message.answer(str(response_dict['data'][-1]))


@router.message(Command(commands='read'))
async def process_read_command(message, state):
    data = await state.get_data()
    await message.answer(text=str(data))


