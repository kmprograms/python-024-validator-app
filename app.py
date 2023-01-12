from abc import ABC, abstractmethod
from typing import Any, Callable
import re


class Validator(ABC):
    def __init__(self):
        self.errors = {}

    @abstractmethod
    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    def errors_to_str(self) -> str:
        return f"{', '.join([f'{key}: {message}' for key, message in self.errors.items()])}"

    @staticmethod
    def matches_regex(regex: str, text: str) -> bool:
        return re.match(regex, text) is not None

    @staticmethod
    def has_value_between(range_min: int | float, range_max: int | float, value: int | float) -> bool:
        return range_min <= value <= range_max

    @staticmethod
    def validate_key_value(key: str, data: dict[str, Any], value_condition_fn: Callable[[str], bool]) -> str:
        if key not in data:
            return 'required'

        if not value_condition_fn(data[key]):
            return 'not correct'

        return ''


class CarValidator(Validator):
    def __init__(self, model_regex: str, speed_min: int, speed_max: int):
        super().__init__()
        self.model_regex = model_regex
        self.speed_min = speed_min
        self.speed_max = speed_max

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        self.errors = {}

        model_val_res = self.validate_key_value('model', data, lambda m: Validator.matches_regex(self.model_regex, m))
        if len(model_val_res) > 0:
            self.errors['model'] = model_val_res

        if 'speed' not in data:
            self.errors['speed'] = 'required'
        elif not isinstance(data['speed'], int):
            self.errors['speed'] = 'not a number'
        elif not self.has_value_between(self.speed_min, self.speed_max, data['speed']):
            self.errors['speed'] = 'not in range'

        if len(self.errors) > 0:
            raise ValueError(self.errors_to_str())

        return data


def main() -> None:
    try:
        car_data = {
            'model': 'AUDi',
            'speed': 120
        }

        print(CarValidator(r'^[A-Z]+$', 150, 250).validate(car_data))
    except ValueError as ve:
        print(ve.args[0])

if __name__ == '__main__':
    main()
