from typing import Dict, Callable


def format_handlers_report(data: Dict[str, Dict[str, int]]) -> str:
    """Форматирует отчет handlers"""
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    max_handler_len = max((len(h) for h in data.keys()), default=0)

    # Заголовок
    header = f"{'HANDLER':<{max_handler_len}}\t" + "\t".join(levels)
    lines = [header]

    # Данные по handlers
    total = {lvl: 0 for lvl in levels}
    for handler in sorted(data.keys()):
        counts = [str(data[handler].get(lvl, 0)) for lvl in levels]
        line = f"{handler:<{max_handler_len}}\t" + "\t".join(counts)
        lines.append(line)
        for lvl in levels:
            total[lvl] += data[handler].get(lvl, 0)

    # Итоги
    total_line = f"{'':<{max_handler_len}}\t" + "\t".join(str(total[lvl]) for lvl in levels)
    lines.append(total_line)
    total_requests = sum(total.values())

    return f"Total requests: {total_requests}\n\n" + "\n".join(lines)


AVAILABLE_REPORTS: Dict[str, Callable] = {
    "handlers": format_handlers_report
}


def generate_report(report_type: str, data: Dict) -> str:
    """Генерирует отчет указанного типа"""
    return AVAILABLE_REPORTS[report_type](data)