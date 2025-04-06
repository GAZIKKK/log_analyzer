import pytest
from pathlib import Path
import sys
from io import StringIO
from main import main


@pytest.fixture
def sample_log(tmp_path: Path) -> Path:
    log_content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]\n"
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /api/v1/reviews/ [192.168.1.29]\n"
    )
    log_file = tmp_path / "sample.log"
    log_file.write_text(log_content)
    return log_file


def test_main_success(sample_log: Path, capsys):
    """Тест успешного запуска main"""
    args = [str(sample_log), "--report", "handlers"]
    main(args)
    captured = capsys.readouterr()

    assert "Total requests: 2" in captured.out
    assert "/api/v1/reviews/" in captured.out
    assert "DEBUG\tINFO\tWARNING\tERROR\tCRITICAL" in captured.out
    assert "0\t1\t0\t1\t0" in captured.out


def test_main_file_not_found(capsys):
    """Тест ошибки при несуществующем файле"""
    args = ["nonexistent.log", "--report", "handlers"]
    with pytest.raises(SystemExit):
        main(args)
    captured = capsys.readouterr()
    assert "Error: File nonexistent.log does not exist" in captured.out


def test_main_invalid_report(sample_log: Path, capsys):
    """Тест ошибки при неверном типе отчета"""
    args = [str(sample_log), "--report", "invalid"]
    with pytest.raises(SystemExit):
        main(args)
    captured = capsys.readouterr()
    assert "Error: Unknown report type" in captured.out