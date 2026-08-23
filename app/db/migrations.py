"""
Database Migration & Auto-Sync Module

This module runs automatically whenever the server starts or restarts.
It checks for database changes:
1. Creates new tables if they don't exist in the database (CREATE TABLE).
2. Checks existing tables and adds missing columns automatically (ALTER TABLE).
3. Cleans up obsolete columns no longer defined in Python models.
4. Provides simple, clear helper functions for manual table operations.
"""

from sqlalchemy import inspect, text
from sqlmodel import SQLModel

# Import all schemas/models so SQLModel metadata registers all tables
from app.api.schemas.user import User
from app.api.schemas.node import (
    NodeDetails,
    NodeCredential,
    NodeRegisterDetails,
    NodeLifeCycle,
)


def create_all_tables(engine):
    """
    Creates any tables that do not exist yet in the database.
    SQLModel reads model definitions and runs CREATE TABLE IF NOT EXISTS.
    """
    print("[DB Migration] Step 1: Checking for new tables to create...")
    SQLModel.metadata.create_all(engine)
    print("[DB Migration] Step 1 complete: Tables created / verified.")


def add_missing_columns(engine):
    """
    Compares Python SQLModel model definitions with actual database tables.
    1. If a new field is added to a Python model, this function detects it
       and automatically executes: ALTER TABLE <table_name> ADD COLUMN <column_name> <data_type>
    2. If an existing column in Python model allows NULL but DB column is NOT NULL,
       it automatically updates column nullability to NULL.
    """
    print("[DB Migration] Step 2: Checking for new columns and nullability sync in models (ALTER TABLE)...")
    inspector = inspect(engine)

    # Loop through every table defined in SQLModel schemas
    for table_name, table_obj in SQLModel.metadata.tables.items():
        # Check if table exists in database
        if not inspector.has_table(table_name):
            continue

        # Get existing columns from the database
        existing_columns = inspector.get_columns(table_name)
        existing_column_map = {col["name"]: col for col in existing_columns}

        # Check each column defined in Python model
        for column in table_obj.columns:
            col_name = column.name
            if col_name not in existing_column_map:
                # Convert SQLAlchemy column type to SQL type string (e.g. VARCHAR, INT, DATETIME)
                col_type = column.type.compile(engine.dialect)
                
                # Check nullability
                nullable_clause = "NULL" if column.nullable else "NOT NULL"
                
                print(f"[DB Migration] New field '{col_name}' found in model '{table_name}'. Altering table...")
                
                # Simple ALTER TABLE query
                alter_sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col_name}` {col_type} {nullable_clause}"
                
                with engine.connect() as connection:
                    connection.execute(text(alter_sql))
                    connection.commit()
                
                print(f"[DB Migration] Successfully added column '{col_name}' to table '{table_name}'.")
            else:
                # Column exists. Check if Python model allows NULL but database column is NOT NULL
                db_col = existing_column_map[col_name]
                if column.nullable and not db_col.get("nullable", True):
                    col_type = column.type.compile(engine.dialect)
                    print(f"[DB Migration] Column '{col_name}' in table '{table_name}' is set to NOT NULL in DB but model allows NULL. Updating nullability...")
                    try:
                        dialect_name = engine.dialect.name
                        if dialect_name in ("mysql", "mariadb"):
                            alter_sql = f"ALTER TABLE `{table_name}` MODIFY COLUMN `{col_name}` {col_type} NULL"
                        elif dialect_name == "postgresql":
                            alter_sql = f'ALTER TABLE "{table_name}" ALTER COLUMN "{col_name}" DROP NOT NULL'
                        else:
                            alter_sql = f"ALTER TABLE `{table_name}` MODIFY COLUMN `{col_name}` {col_type} NULL"

                        with engine.connect() as connection:
                            connection.execute(text(alter_sql))
                            connection.commit()
                        print(f"[DB Migration] Successfully updated column '{col_name}' in table '{table_name}' to allow NULL.")
                    except Exception as err:
                        print(f"[DB Migration Error] Could not update column '{col_name}' nullability: {err}")

    print("[DB Migration] Step 2 complete: Column synchronization complete.")


def cleanup_obsolete_columns(engine):
    """
    Checks for columns in database tables that are no longer defined in Python models.
    Automatically drops obsolete typo columns (like 'owener_id') so MySQL INSERT statements won't fail.
    """
    print("[DB Migration] Step 3: Cleaning up obsolete/old columns...")
    inspector = inspect(engine)

    for table_name, table_obj in SQLModel.metadata.tables.items():
        if not inspector.has_table(table_name):
            continue

        model_column_names = {column.name for column in table_obj.columns}
        existing_columns = inspector.get_columns(table_name)

        for col in existing_columns:
            col_name = col["name"]
            if col_name not in model_column_names:
                print(f"[DB Migration] Found obsolete column '{col_name}' in table '{table_name}'. Removing obsolete column...")
                try:
                    with engine.connect() as connection:
                        connection.execute(text(f"ALTER TABLE `{table_name}` DROP COLUMN `{col_name}`"))
                        connection.commit()
                    print(f"[DB Migration] Successfully dropped obsolete column '{col_name}' from '{table_name}'.")
                except Exception as err:
                    print(f"[DB Migration] Could not drop column '{col_name}': {err}")

    print("[DB Migration] Step 3 complete: Cleanup finished.")


# =====================================================================
# SIMPLE HELPER FUNCTIONS FOR UNDERSTANDING & MANUAL OPERATIONS
# You can use these simple helper functions anywhere in your project!
# =====================================================================

def create_table_simple(engine, table_name: str, column_definitions: str):
    """
    Simple example of creating a new table with raw SQL.
    """
    sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({column_definitions});"
    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()
    print(f"[Raw SQL] Created table '{table_name}' if it did not exist.")


def add_column_simple(engine, table_name: str, column_name: str, column_type: str):
    """
    Simple example of adding a new column to an existing table using raw SQL.
    """
    sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_type};"
    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()
    print(f"[Raw SQL] Added column '{column_name}' to table '{table_name}'.")


def drop_column_simple(engine, table_name: str, column_name: str):
    """
    Simple example of deleting a column from a table using raw SQL.
    """
    sql = f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`;"
    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()
    print(f"[Raw SQL] Dropped column '{column_name}' from table '{table_name}'.")


def ensure_primary_key_autoincrement(engine):
    """
    Ensures that primary key integer columns (e.g. 'id') have AUTO_INCREMENT in MySQL.
    """
    if engine.dialect.name not in ("mysql", "mariadb"):
        return

    inspector = inspect(engine)
    for table_name, table_obj in SQLModel.metadata.tables.items():
        if not inspector.has_table(table_name):
            continue

        existing_columns = inspector.get_columns(table_name)
        for col in existing_columns:
            col_name = col["name"]
            if (col.get("primary_key") or col_name == "id") and not col.get("autoincrement"):
                print(f"[DB Migration] Enabling AUTO_INCREMENT on '{table_name}.{col_name}'...")
                try:
                    alter_sql = f"ALTER TABLE `{table_name}` MODIFY COLUMN `{col_name}` INT AUTO_INCREMENT"
                    with engine.connect() as connection:
                        connection.execute(text(alter_sql))
                        connection.commit()
                    print(f"[DB Migration] Successfully set AUTO_INCREMENT on '{table_name}.{col_name}'.")
                except Exception as err:
                    print(f"[DB Migration Error] Could not set AUTO_INCREMENT on '{table_name}.{col_name}': {err}")


def run_db_migrations(engine):
    """
    Main migration runner. Called automatically on server startup / restart.
    """
    print("\n" + "=" * 60)
    print("[SERVER RESTART] Checking database changes and running auto-migrations...")
    print("=" * 60)
    try:
        create_all_tables(engine)
        add_missing_columns(engine)
        ensure_primary_key_autoincrement(engine)
        cleanup_obsolete_columns(engine)
        print("[SERVER RESTART] Database schemas are fully up-to-date!\n")
    except Exception as error:
        print(f"[DB Migration Error] Could not complete database sync: {error}\n")


