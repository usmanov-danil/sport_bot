import datetime

from aiogram.types.user import User as UserRaw
from bot.texts import KBGU_TEXT, KEYBOARD
from repositories.abstract import UserRepository


async def calculate_BMR(repo: UserRepository, sex: str, ai_user: UserRaw) -> int:
    """
    Женщины: BMR= 9,99 * вес (в кг) + 6,25 * рост (в см) – 4,92 * возраст (количество лет) – 161
    Мужчины: BMR = 9,99 * вес (в кг) + 6,25 * рост (в см) – 4,92 * возраст (количество лет) + 5
    """
    user = repo.get_personal_info(ai_user.id)
    bmr = 9.99 * float(user.weight) + 6.25 * int(user.height) - 4.92 * int(user.years)
    bmr += -161 if sex == KEYBOARD['female'] else 5

    return int(bmr)


async def calculate_kbgu_levels(
    repo: UserRepository, sex: str, activity: int, ai_user: UserRaw
) -> str:
    """
    BMR = 9,99*65 + 6,25*165 - 4,92*30 – 161 = 1372
    Норма калорий для поддержания веса = 1372*1,375=1886,5 ккал
    Норма калорий с дефицитом = 1886 - (1886*0,2) = 1509 ккал
    """
    bmr = await calculate_BMR(repo, sex, ai_user)
    normal = int(bmr * activity)
    deficit = int(normal - normal * 0.18)
    surplus = int(normal + normal * 0.18)

    return KBGU_TEXT.format(normal=normal, deficit=deficit, surplus=surplus)
