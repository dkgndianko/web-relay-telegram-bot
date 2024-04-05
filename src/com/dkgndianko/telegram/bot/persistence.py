from telegram.ext import PicklePersistence, BasePersistence

from com.dkgndianko.core.config import settings



def get_persistence() -> BasePersistence:
    persistence = PicklePersistence(filepath=settings.TELEGRAM_PERSISTENCE_PATH)
    return persistence