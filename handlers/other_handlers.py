from aiogram import Router


router = Router()


@router.message()
async def send_answer(message):
    await message.answer('Нет такой команды')