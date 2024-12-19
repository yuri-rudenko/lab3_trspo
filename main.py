from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Функція для обчислення кроків гіпотези Коллатца для одного числа
def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

# Функція для обробки чисел у потоці
def process_numbers(start, end, lock, total_steps, total_count):
    local_steps = 0
    local_count = 0
    for number in range(start, end):
        local_steps += collatz_steps(number)
        local_count += 1
    
    # Оновлення глобальних змінних через lock
    with lock:
        total_steps[0] += local_steps
        total_count[0] += local_count

# Функція для паралельного обчислення
def parallel_collatz_calculation(max_number=10_000_0, num_threads=4):

    total_steps = [0]
    total_count = [0]
    lock = Lock() 
    chunk_size = max_number // num_threads
    ranges = [(i * chunk_size + 1, min((i + 1) * chunk_size + 1, max_number + 1)) for i in range(num_threads)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(process_numbers, start, end, lock, total_steps, total_count)
            for start, end in ranges
        ]
        # Очікування завершення всіх потоків
        for future in futures:
            future.result()

    # Розрахунок середнього
    avg_steps = total_steps[0] / total_count[0] if total_count[0] > 0 else 0
    print(f"Середня кількість кроків для гіпотези Коллатца: {avg_steps:.2f}")


parallel_collatz_calculation(num_threads=20)
