from datetime import datetime
from exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)


def data_processing(team_info: dict):
    world_cups_list = []
    for i in range(1930, 2024, 4):
        world_cups_list.append(i)

    first_cup = datetime.strptime(team_info["first_cup"], "%Y-%m-%d")
    first_cup_year = first_cup.year

    if team_info["titles"] < 0:
        raise NegativeTitlesError()

    if not world_cups_list.__contains__(first_cup_year):
        raise InvalidYearCupError()

    first_cup_year_index = world_cups_list.index(first_cup_year)
    max_titles = len(world_cups_list[first_cup_year_index:])
    if team_info["titles"] > max_titles:
        raise ImpossibleTitlesError()

    return team_info
