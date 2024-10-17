import aiogram
from keyboards.for_questions import MainMenu

router = Router()  # [1]

@router.message(commands=["start"])
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Войти",
        callback_data="login")
    )
        
    await message.answer(
        "Приветствую, это бот Нефтекамского филиала УУНиТ.\n\n"
        "Он предназначен для:\n"
        "- Просмотра расписания\n"
        "- Просмотра расписания преподавателя\n"
        "Кол-во активных пользователей: 99\n\n"
        "Для продолжения вам необходимо войти в систему с помощью логина и пароля, которые вы используете в личном кабинете.",
        reply_markup=builder.as_markup()
    )

@router.callback_query(text="login")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))

@router.message(Text(text="нет", text_ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )