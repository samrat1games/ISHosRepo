import time
import sys
import random
import os
import shutil
import subprocess

# --- Константы оформления ---
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"
BOLD = "\033[1m"

def get_size():
    columns, lines = shutil.get_terminal_size()
    return columns, lines

def clear():
    sys.stdout.write("\033[2J\033[H")

def print_at(x, y, text, color=RESET):
    sys.stdout.write(f"\033[{y};{x}H{color}{text}{RESET}")

def center_print(lines, color=RESET, y_offset=0):
    w, h = get_size()
    start_y = max(1, (h - len(lines)) // 2 + y_offset)
    for i, line in enumerate(lines):
        start_x = max(1, (w - len(line)) // 2)
        print_at(start_x, start_y + i, line, color)
    sys.stdout.flush()

# --- Арт-объекты (Исправлены кавычки и экранирование) ---
PENGUIN = [
    "     _nnnn_    ",
    "    dGGGGMMb   ",
    "   @p~qp~~qMb  ",
    "   M|@||@) M|  ",
    "   @,----.JM|  ",
    "  JS^\\__/  qKL ",
    " dZP        qKRb",
    "dZP          qKKb",
    "fZP            SMMb",
    "HZM            MMMM",
    "FqM            MMMM",
    "__| \".        |\\dS\"qML",
    "|    `.       | `' \\Zq",
    "_)      \\.___.,|     .'",
    "\\____   )MMMMMP|   .'",
    "     `-'       `--' hjm"
]

SNAKE = [
    "$$ |  $$ |",
    "$$ |  $$ |",
    "$$$$$$$$ |",
    "$$  __$$ |",
    "$$ |  $$ |",
    "$$ |  $$ |",
    "\\__|  \\__|"
]

ISHOS = [
    r"██ ██████  ██   ██  ██████  ███████ ",
    r"██ ██      ██   ██ ██    ██ ██      ",
    r"██ ███████ ███████ ██    ██ ███████ ",
    r"██      ██ ██   ██ ██    ██      ██ ",
    r"██ ███████ ██   ██  ██████  ███████ "
]

def run_animation():
    clear()
    
    # 1. ПОЯВЛЕНИЕ ПИНГВИНА
    center_print(["[ INITIALIZING CORE ]"], BLUE, -10)
    time.sleep(0.5)
    center_print(PENGUIN, BLUE)
    time.sleep(1.2)

    # 2. ТРАНСФОРМАЦИЯ (Глитч)
    for _ in range(6):
        clear()
        art = PENGUIN if _ % 2 == 0 else SNAKE
        col = BLUE if _ % 2 == 0 else GREEN
        center_print(art, col)
        time.sleep(0.15)
    
    clear()
    center_print(SNAKE, GREEN)
    time.sleep(1.2)

    # 3. ТОТАЛЬНЫЙ ХАОС
    chars = "░▒▓█✘☠☣⚡⚙$#@!&%*()+-<>?/|{}[]"
    colors = [RED, GREEN, YELLOW, BLUE, CYAN, BOLD]
    for _ in range(30):
        w, h = get_size()
        for _y in range(1, h + 1):
            line = "".join(random.choice(colors) + random.choice(chars) for _ in range(w))
            sys.stdout.write(f"\033[{_y};1H{line}")
        sys.stdout.flush()
        time.sleep(0.04)

    # 4. ХАКЕРСКАЯ МАТРИЦА
    clear()
    columns, lines = get_size()
    drops = [random.randint(1, lines) for _ in range(columns)]
    
    for _ in range(60):
        for i in range(len(drops)):
            char = chr(random.randint(33, 126))
            print_at(i + 1, drops[i], char, GREEN)
            if drops[i] > 1:
                print_at(i + 1, drops[i] - 1, random.choice(chars), "\033[2;32m")
            
            drops[i] += 1
            if drops[i] > lines or random.random() > 0.95:
                drops[i] = 1
        sys.stdout.flush()
        time.sleep(0.03)

    # 5. ФИНАЛ ISHOS
    clear()
    center_print(ISHOS, GREEN)
    
    w, h = get_size()
    bar_width = 30
    for i in range(bar_width + 1):
        percent = int((i / bar_width) * 100)
        bar = "█" * i + "░" * (bar_width - i)
        print_at((w - bar_width)//2, (h // 2) + 5, f"LOADING: {bar} {percent}%", GREEN)
        sys.stdout.flush()
        time.sleep(0.05)

    time.sleep(0.5)
    clear()
    
    if os.path.exists("main.py"):
        subprocess.run([sys.executable, "main.py"])
    else:
        print(f"{RED}[ERROR]: main.py not found.{RESET}")

if __name__ == "__main__":
    try:
        sys.stdout.write("\033[?25l") # Скрыть курсор
        run_animation()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h" + RESET + "\033[2J\033[H") # Вернуть курсор