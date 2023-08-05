import re
import time
from datetime import datetime

from pydantic import BaseModel, validator


class BillingSchema(BaseModel):
    price: int = 0
    users_count: int = 0
    tariff: str = 'Неопределен'
    pay_period: int = int(time.time())
    is_paid: bool = False

    @validator('price', pre=True)
    def _price_validator(cls, value):
        return int(value)

    @validator('users_count', pre=True)
    def _users_count_validator(cls, value):
        return int(value)

    @validator('pay_period', pre=True)
    def _pay_period_validator(cls, value):
        match = re.search(r'(\d{2}.\d{2}.\d{4})', value).group(1)
        pay_period = time.mktime(datetime.strptime(match, "%d.%m.%Y").timetuple())
        thirteen_months = 60 * 60 * 24 * 30 * 13
        correct_pay_period = pay_period - thirteen_months
        return correct_pay_period
