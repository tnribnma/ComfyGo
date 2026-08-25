import sys
from sqlalchemy import text
from app.database import Database
from app.config import settings

COLUMNS_TO_ADD = [
    ("phone",            "VARCHAR(30)"),
    ("website",          "VARCHAR(300)"),
    ("accepts_reservations", "BOOLEAN DEFAULT FALSE"),
    ("wifi",             "BOOLEAN DEFAULT FALSE"),
    ("parking",          "BOOLEAN DEFAULT FALSE"),
    ("live_music",       "BOOLEAN DEFAULT FALSE"),
    ("is_featured",      "BOOLEAN DEFAULT FALSE"),
]


def migrate():
    engine = Database.engine()
    with engine.begin() as conn:
        result = conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'restaurants'"
        ))
        existing = {row[0] for row in result}

        for col_name, col_type in COLUMNS_TO_ADD:
            if col_name not in existing:
                sql = f"ALTER TABLE restaurants ADD COLUMN {col_name} {col_type}"
                print(f"  Adding column: {col_name} ...")
                conn.execute(text(sql))
            else:
                print(f"  Column already exists: {col_name}")

    print("\nMigration complete!")


if __name__ == "__main__":
    print(f"Migrating restaurants table on {settings.PG_DB}...")
    migrate()
