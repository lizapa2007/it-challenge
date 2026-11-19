from sqlalchemy.orm import Session

from app.models import Task
from app.stats import calculate_statistics, read_column


def process_task(db: Session, task: Task) -> None:
    """Обрабатывает задание: считает статистику и сохраняет результат или ошибку."""
    task.status = "processing"
    db.commit()

    try:
        values = read_column(task.file_content, task.column_name)
        task.result = calculate_statistics(values)
        task.status = "completed"
    except ValueError as error:
        task.status = "failed"
        task.error = str(error)

    db.commit()