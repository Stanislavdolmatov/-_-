import random
from datetime import timedelta

# Константы
PEAK_HOURS = [(7, 9), (17, 19)]
ROUTE_TIME = 60
ROUTE_VARIATION = 10
DAY_START = 6
DAY_END = 22
WORK_HOURS_A = 8
WORK_HOURS_B = 12
SHIFT_CHANGE_TIME = 15

# Функция для генерации расписания
def greedy_schedule(driver_type):
    schedule = []
    current_time = timedelta(hours=DAY_START)
    max_work_hours = WORK_HOURS_A if driver_type == "a" else WORK_HOURS_B
    work_limit = timedelta(hours=max_work_hours)
    lunch_minimum = timedelta(hours=4)

    # Жадно создаем расписание для водителей
    while current_time < timedelta(hours=DAY_END):
        driver_schedule = []
        start_time = current_time
        total_work_time = timedelta(0)
        lunch_taken = False

        while total_work_time < work_limit and start_time < timedelta(hours=DAY_END):
            route_time = timedelta(minutes=ROUTE_TIME + random.randint(-ROUTE_VARIATION, ROUTE_VARIATION))
            end_time = start_time + route_time

            if end_time > timedelta(hours=DAY_END):
                break

            driver_schedule.append((start_time, end_time))
            total_work_time += route_time + timedelta(minutes=SHIFT_CHANGE_TIME)
            start_time = end_time + timedelta(minutes=SHIFT_CHANGE_TIME)

            # Учитываем обед
            if total_work_time >= lunch_minimum and not lunch_taken:
                if not any(start <= start_time.seconds // 3600 < end for start, end in PEAK_HOURS):
                    start_time += timedelta(hours=1)  # Час на обед
                    lunch_taken = True

        schedule.append(driver_schedule)
        current_time = start_time
    return schedule

# Форматирование расписания
def format_schedule(schedule):
    formatted_schedule = []
    for i, driver_schedule in enumerate(schedule, 1):
        formatted_schedule.append(f"Driver {i}:")
        for start_time, end_time in driver_schedule:
            formatted_schedule.append(f"  {str(start_time)} - {str(end_time)}")
    return "\n".join(formatted_schedule)

# Жадный алгоритм для водителей типа А
print("Generating schedule for driver type A using greedy algorithm...")
schedule_a_greedy = greedy_schedule("a")
print("\nGreedy schedule for driver type A:")
print(format_schedule(schedule_a_greedy))

# Жадный алгоритм для водителей типа Б
print("\nGenerating schedule for driver type B using greedy algorithm...")
schedule_b_greedy = greedy_schedule("b")
print("\nGreedy schedule for driver type B:")
print(format_schedule(schedule_b_greedy))
