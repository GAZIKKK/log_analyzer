import pytest
from reports import format_handlers_report, generate_report


def test_format_handlers_report():
    """Тест форматирования отчета handlers"""
    data = {
        "/api/v1/reviews/": {"DEBUG": 0, "INFO": 2, "WARNING": 0, "ERROR": 1, "CRITICAL": 0},
        "/api/v1/auth/login/": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    }
    report = format_handlers_report(data)

    # Проверяем основные элементы отчета
    assert "Total requests: 4" in report
    assert "/api/v1/auth/login/" in report
    assert "/api/v1/reviews/" in report
    assert "DEBUG\tINFO\tWARNING\tERROR\tCRITICAL" in report
    assert "0\t2\t0\t1\t0" in report  # Для /api/v1/reviews/
    assert "0\t1\t0\t0\t0" in report  # Для /api/v1/auth/login/
    assert "0\t3\t0\t1\t0" in report  # Итоговая строка


def test_generate_report():
    """Тест генерации отчета через generate_report"""
    data = {
        "/api/v1/reviews/": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    }
    report = generate_report("handlers", data)
    assert "Total requests: 1" in report
    assert "/api/v1/reviews/" in report


def test_empty_data_report():
    """Тест отчета с пустыми данными"""
    data = {}
    report = format_handlers_report(data)
    assert "Total requests: 0" in report
    assert "DEBUG\tINFO\tWARNING\tERROR\tCRITICAL" in report
    assert "0\t0\t0\t0\t0" in report  # Итоговая строка