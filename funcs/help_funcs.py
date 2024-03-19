def get_rus_category(category):
    d = {"personal": "Личное", "work": "Работа", "study": "Учеба", "day_plans": "Планы на день", "other": "Другое"}
    return d[category]


def isCorrectInput(numbers, len_notes) -> bool:
    for number in numbers:
        if not number.isdigit():
            return False
        elif int(number) < 1 or int(number) > len_notes:
            return False
    return True
