import sys
from typing import List, Dict
from argparse import ArgumentParser
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from parser import parse_log_file
from reports import generate_report, AVAILABLE_REPORTS


def process_file(file_path: Path) -> Dict:
    """Обрабатывает один лог-файл и возвращает данные для отчета"""
    return parse_log_file(file_path)


def main(args: List[str]) -> None:
    # Настройка аргументов CLI
    parser = ArgumentParser(description="Log analyzer for Django applications")
    parser.add_argument("files", nargs="+", help="Paths to log files")
    parser.add_argument("--report", required=True, help="Report type to generate")

    parsed_args = parser.parse_args(args)

    # Проверка существования файлов
    file_paths = [Path(f) for f in parsed_args.files]
    for fp in file_paths:
        if not fp.exists():
            print(f"Error: File {fp} does not exist")
            sys.exit(1)

    # Проверка типа отчета
    if parsed_args.report not in AVAILABLE_REPORTS:
        print(f"Error: Unknown report type. Available: {', '.join(AVAILABLE_REPORTS.keys())}")
        sys.exit(1)

    # Параллельная обработка файлов
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_file, file_paths))

    # Объединение результатов
    combined_data = {}
    for result in results:
        for handler, levels in result.items():
            if handler not in combined_data:
                combined_data[handler] = {}
            for level, count in levels.items():
                combined_data[handler][level] = combined_data[handler].get(level, 0) + count

    # Генерация и вывод отчета
    report = generate_report(parsed_args.report, combined_data)
    print(report)


if __name__ == "__main__":
    main(sys.argv[1:])