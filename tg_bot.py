from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.utils.markdown import hlink
from main import get_product_info
from main import get_seller_id
import json
import time

bot = Bot(token=YOUR_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Спарсить товары продавца", callback_data="pars"))
    await message.answer("Привет, это бот для парсинга.", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "pars")
async def gaga(call):
    await call.message.answer("Отправь ссылку на какой-нибудь товар продавца.")
    dp.register_message_handler(parsing)


async def parsing(message: types.Message):
    url = message.text.strip()
    seller_id = get_seller_id(url)
    get_product_info(seller_id)

    with open("result.json", "r") as file:
        data = json.load(file)
    for index, item in enumerate(data):
        name = f"{hlink(item.get('name'), item.get('url'))}"
        price = str(item.get("price")/100) + "₽"
        id_card = item.get("id card")
        if item.get("rait") == 0:
            rating = "Нет оценок"
        else:
            rating = item.get("rait")
        if index%20 == 0:
            time.sleep(3)
        await message.answer(f"{name}\nЦена: {price}\nРейтинг: {rating}\nId Карточки: {id_card}")
    await message.answer(f"Id продавца: {seller_id}")
    await message.answer("Выгружены все товары продавца на данный момент.")


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()

