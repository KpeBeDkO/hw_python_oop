from dataclasses import dataclass
from typing import Dict, List, Optional, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    SEC_IN_MIN: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения. км.ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__

        return InfoMessage(
            training_type,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        spend_calories = (
            (
                Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + Running.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * self.duration
            * self.MIN_IN_HOUR
        )

        return spend_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    IN_WATER_CONST_1 = 0.035
    IN_WATER_CONST_2 = 0.029
    KM_TO_M = 0.278
    CM_IN_METER = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(
            action,
            duration,
            weight,
        )
        self.height = height

    def get_spent_calories(self) -> float:
        speed_in_m_sec = self.KM_TO_M * self.get_mean_speed()
        height_in_m = self.height / self.CM_IN_METER
        training_time_in_min = self.duration * self.MIN_IN_HOUR
        spend_calories = (
            self.IN_WATER_CONST_1 * self.weight
            + (speed_in_m_sec ** 2 / height_in_m)
            * self.IN_WATER_CONST_2 * self.weight
        ) * training_time_in_min

        return spend_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CONST_SWIM_1 = 1.1
    CONST_SWIM_2 = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(
            action,
            duration,
            weight,
        )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средняя скорость км/ч."""
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

        return mean_speed

    def get_spent_calories(self) -> float:
        spend_calories = (
            (self.get_mean_speed() + self.CONST_SWIM_1)
            * self.CONST_SWIM_2 * self.weight * self.duration
        )

        return spend_calories


def read_package(
    workout_type: str,
    data: List[int]
) -> Optional[Training]:
    code_training_class = CODE_TRAINING.get(workout_type)
    if code_training_class:
        class_instance = code_training_class(*data)
    try:
        return class_instance
    except NameError:
        return print('Пусто')


CODE_TRAINING: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def main(training: Optional[Training]) -> None:
    """Главная функция."""
    if training:
        info = training.show_training_info()
        print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
