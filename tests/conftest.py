import os
import tempfile

# Для тестов используем отдельную временную базу SQLite,
# чтобы не трогать настоящую базу PostgreSQL.
test_db_path = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = "sqlite:///" + test_db_path