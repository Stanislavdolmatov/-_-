import random
from datetime import timedelta, datetime

# Константы
a = int(input())
b = int(input())
PEAK_HOURS = [(7, 9), (17, 19)]  # Часы пик
ROUTE_TIME = 60  # Время на маршрут (в минутах)
ROUTE_VARIATION = 10  # Вариация времени маршрута (в минутах)
DAY_START = 6  # Начало работы
DAY_END = 22  # Конец работы
WORK_HOURS_A = 8  # Рабочие часы для водителей типа А
WORK_HOURS_B = 12  # Рабочие часы для водителей типа Б
LUNCH_MINIMUM = 4  # Минимальное количество часов до обеда
SHIFT_CHANGE_TIME = 15  # Пересменка водителей в минутах
POPULATION_SIZE = 100  # Размер популяции
GENERATIONS = int(input())  # Количество поколений
MUTATION_RATE = 0.1  # Вероятность мутации

# Генерация начального расписания5
def generate_schedule(driver_type):
    schedule = []
    if driver_type == "a":
        max_work_hours = WORK_HOURS_A
    elif driver_type == "b":
        max_work_hours = WORK_HOURS_B
    else:
        raise ValueError("Некорректный тип водителя")

    num_drivers = random.randint(a, b)  # Начальное количество водителей
    for _ in range(num_drivers):
        driver_schedule = []
        current_time = timedelta(hours=DAY_START)
        while current_time < timedelta(hours=DAY_END):
            route_time = timedelta(minutes=ROUTE_TIME + random.randint(-ROUTE_VARIATION, ROUTE_VARIATION))
            end_time = current_time + route_time
            if end_time > timedelta(hours=DAY_END):
                break
            driver_schedule.append((current_time, end_time))
            current_time = end_time + timedelta(minutes=SHIFT_CHANGE_TIME)
        schedule.append(driver_schedule)
    return schedule

# Расчет нагрузки в часы пик и вне их
def calculate_load(schedule):
    peak_load = 0
    off_peak_load = 0
    for driver_schedule in schedule:
        for start_time, end_time in driver_schedule:
            hour = start_time.seconds // 3600
            if any(start <= hour < end for start, end in PEAK_HOURS):
                peak_load += 1
            else:
                off_peak_load += 1
    return peak_load, off_peak_load

# Оценочная функция
def fitness(schedule):
    peak_load, off_peak_load = calculate_load(schedule)
    total_routes = sum(len(driver_schedule) for driver_schedule in schedule)
    return total_routes - abs(peak_load - off_peak_load)

# Скрещивание
def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if random.random() > 0.5 and i < len(parent2):
            child.append(parent2[i])
        else:
            child.append(parent1[i])
    return child

# Мутация
def mutate(schedule):
    if random.random() < MUTATION_RATE:
        driver = random.choice(schedule)
        if driver:
            index = random.randint(0, len(driver) - 1)
            mutated_start = driver[index][0] + timedelta(minutes=random.randint(-10, 10))
            mutated_end = mutated_start + timedelta(minutes=ROUTE_TIME + random.randint(-ROUTE_VARIATION, ROUTE_VARIATION))
            driver[index] = (mutated_start, mutated_end)

# Основной цикл генетического алгоритма
def genetic_algorithm(driver_type):
    population = [generate_schedule(driver_type) for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):
        # Оценка популяции
        population = sorted(population, key=fitness, reverse=True)
        new_population = population[:10]  # Сохраняем топ-10
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:50], 2)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
        population = new_population
        if generation % 10 == 0:
            print(f"Generation {generation}, Best fitness: {fitness(population[0])}")
    return population[0]

# Форматирование расписания
def format_schedule(schedule):
    formatted_schedule = []
    for i, driver_schedule in enumerate(schedule, 1):
        formatted_schedule.append(f"Driver {i}:")
        for start_time, end_time in driver_schedule:
            formatted_schedule.append(f"  {str(start_time)} - {str(end_time)}")
    return "\n".join(formatted_schedule)

# Запуск для водителей типа А
print("Generating schedule for driver type A...")
schedule_a = genetic_algorithm("a")
print("\nOptimal schedule for driver type A:")
print(format_schedule(schedule_a))

# Запуск для водителей типа Б
print("\nGenerating schedule for driver type B...")
schedule_b = genetic_algorithm("b")
print("\nOptimal schedule for driver type B:")
print(format_schedule(schedule_b))