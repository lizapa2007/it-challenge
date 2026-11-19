import csv
import io


def read_column(content: str, column: str) -> list[float]:
    """Читает CSV-текст и возвращает числа из указанного столбца."""
    if not content.strip():
        raise ValueError("Файл пустой")

    reader = csv.DictReader(io.StringIO(content))
    columns = reader.fieldnames or []

    if column not in columns:
        available = ", ".join(columns)
        raise ValueError(f"Столбец '{column}' не найден. Есть столбцы: {available}")

    values = []
    for row in reader:
        raw_value = row[column]
        line = reader.line_num

        if raw_value is None or raw_value.strip() == "":
            raise ValueError(f"Строка {line}: пустое значение в столбце '{column}'")

        try:
            values.append(float(raw_value))
        except ValueError:
            raise ValueError(f"Строка {line}: '{raw_value}' не является числом") from None

    if not values:
        raise ValueError("В файле нет строк с данными, только заголовок")

    return values


def calculate_statistics(values: list[float]) -> dict:
    """Считает количество, минимум, максимум и среднее."""
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 2),
    }