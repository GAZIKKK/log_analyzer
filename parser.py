from typing import Dict
from pathlib import Path
import re

LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
# Регулярное выражение для извлечения уровня логирования и handler'а
REQUEST_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (\w+) django\.request: (?:GET|POST|PUT|DELETE) (/\S+) \d{3} OK|^.* (\w+) django\.request: Internal Server Error: (/\S+)"
)


def parse_log_file(file_path: Path) -> Dict[str, Dict[str, int]]:
    """Парсит лог-файл и возвращает статистику по handlers"""
    handlers: Dict[str, Dict[str, int]] = {}

    with file_path.open("r") as f:
        for line in f:  # Читаем построчно для экономии памяти
            match = REQUEST_PATTERN.search(line)
            if match:
                # Группы: (уровень для OK, handler для OK, уровень для ошибки, handler для ошибки)
                level_ok, handler_ok, level_err, handler_err = match.groups()

                if level_ok and handler_ok:  # Успешный запрос
                    level = level_ok
                    handler = handler_ok
                elif level_err and handler_err:  # Ошибка
                    level = level_err
                    handler = handler_err
                else:
                    continue

                if level in LOG_LEVELS:
                    if handler not in handlers:
                        handlers[handler] = {lvl: 0 for lvl in LOG_LEVELS}
                    handlers[handler][level] += 1

    return handlers