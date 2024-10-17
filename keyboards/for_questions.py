import aiogram

def MainMenu() -> ReplyKeyboardMarkup:
	kb = [
		[
			types.KeyboardButton(text="Расписание"),
			types.KeyboardButton(text="Найти преподавателя"),
			types.KeyboardButton(text="Войти")
		],
	]
	keyboard = types.ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Воспользуйтесь меню ниже"
		)