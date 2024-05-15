import pathlib
import sys
import alembic
from sqlalchemy import engine_from_config, pool

from logging.config import fileConfig
import logging

# we are appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL # noqa

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logging = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migration in 'online' mode
    """
    connectable = config.attributes.get("connection", None)
    config.se_main_option("sqlalchemy.url", str(DATABASE_URL))

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=None
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migration()


def run_migration_offline() -> None:
    """
    Run migration in 'online' mode
    """
    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migration()


if alembic.context.is_offline_mode():
    logging.info("Running migration offline")
    run_migration_offline()
else:
    logging.info("Running migration online")
    run_migrations_online()
