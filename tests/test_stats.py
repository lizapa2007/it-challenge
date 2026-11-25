import pytest

from app.stats import calculate_statistics, read_column


def test_read_column_returns_numbers():
    content = "date,temperature\n2026-11-01,21.5\n2026-11-02,19.8\n"
    assert read_column(content, "temperature") == [21.5, 19.8]


def test_calculate_statistics():
    result = calculate_statistics([21.5, 19.8, 23.0, 22.1])
    assert result == {"count": 4, "min": 19.8, "max": 23.0, "mean": 21.6}


def test_empty_file():
    with pytest.raises(ValueError, match="Файл пустой"):
        read_column("", "temperature")


def test_column_not_found():
    content = "date,temperature\n2026-11-01,21.5\n"
    with pytest.raises(ValueError, match="не найден"):
        read_column(content, "pressure")


def test_not_a_number():
    content = "date,temperature\n2026-11-01,тепло\n"
    with pytest.raises(ValueError, match="не является числом"):
        read_column(content, "temperature")


def test_empty_value():
    content = "date,temperature\n2026-11-01,\n"
    with pytest.raises(ValueError, match="пустое значение"):
        read_column(content, "temperature")


def test_only_header():
    with pytest.raises(ValueError, match="нет строк с данными"):
        read_column("date,temperature\n", "temperature")
        