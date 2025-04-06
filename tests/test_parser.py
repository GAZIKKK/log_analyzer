import pytest
from pathlib import Path
from parser import parse_log_file, LOG_LEVELS


@pytest.fixture
def sample_log(tmp_path: Path) -> Path:
    """Создает временный лог-файл для тестов"""
    log_content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]\n"
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /api/v1/reviews/ [192.168.1.29] - ValueError\n"
        "2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products';\n"
        "2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/auth/login/ 201 OK [192.168.1.97]\n"
    )
    log_file = tmp_path / "sample.log"
    log_file.write_text(log_content)
    return log_file


def test_parse_log_file(sample_log: Path):
    """Тест парсинга лог-файла"""
    result = parse_log_file(sample_log)

    # Проверяем, что парсер извлек только django.request записи
    assert "/api/v1/reviews/" in result
    assert "/api/v1/auth/login/" in result
    assert len(result) == 2  # Только два handler'а

    # Проверяем уровни логирования для /api/v1/reviews/
    assert result["/api/v1/reviews/"]["INFO"] == 1
    assert result["/api/v1/reviews/"]["ERROR"] == 1
    assert result["/api/v1/reviews/"]["DEBUG"] == 0

    # Проверяем уровни логирования для /api/v1/auth/login/
    assert result["/api/v1/auth/login/"]["INFO"] == 1
    assert result["/api/v1/auth/login/"]["ERROR"] == 0


def test_parse_empty_log(tmp_path: Path):
    """Тест парсинга пустого лог-файла"""
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("")
    result = parse_log_file(empty_log)
    assert result == {}