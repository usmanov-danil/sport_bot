from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from bot.texts import KEYBOARD
from models.workout import Gymnastic, Workout

# setting callback_data prefix and parts
workout_callback = CallbackData(
    'workout_inline', 'excercise_name', 'excercise_description', 'excercise_link', sep='z'
)


class WorkoutInline:
    def __init__(self, workout: Workout):
        self.workout = workout

    async def start_calendar(self) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=1)
        for item in self.workout.get_gymnastics():
            inline_kb.add(
                InlineKeyboardButton(
                    f'{item.excercise.name} – {item.value}',
                    callback_data=workout_callback.new(
                        item.excercise.name, item.excercise.description, item.excercise.link
                    ),
                )
            )

        return inline_kb

    @staticmethod
    async def process_selection(query: CallbackQuery, data: CallbackData) -> None:
        msg = None
        reply_markup = None

        if gym := data['excercise_name']:
            msg = f'*{gym}*\n'
        if description := data['excercise_description']:
            msg += f'Описание задания: {description}\n'

        if msg:
            await query.message.edit_text(msg)
        if link := data['excercise_link']:
            reply_markup = InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton('Видео', url=link)
            )
            await query.message.edit_reply_markup(reply_markup)
