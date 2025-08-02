import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, inspect, pool, text

from alembic import context
from app.auth.models import SuperAdmin  # noqa
from app.database.base import Base

# Import all models here
from app.organization.models import Organization  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set up logger
logger = logging.getLogger("alembic.env")
logger.setLevel(logging.DEBUG)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Print debug information
    logger.info("Models in metadata: %s", [table.name for table in target_metadata.sorted_tables])

    # Get the database URL
    config_section = config.get_section(config.config_ini_section)
    url = config_section.get("sqlalchemy.url")
    logger.info("Database URL: %s", url)

    # Configure the engine with AUTOCOMMIT mode
    config_section["sqlalchemy.isolation_level"] = "AUTOCOMMIT"

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Print existing tables
        inspector = inspect(connection)
        existing_tables = inspector.get_table_names()
        logger.info("Existing tables in database: %s", existing_tables)

        # Disable foreign key checks during migration
        connection.execute(text("SET session_replication_role = 'replica';"))

        try:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True,
                transaction_per_migration=True,
            )

            logger.info("Starting migration")
            with context.begin_transaction():
                context.run_migrations()
            logger.info("Migration completed")

        finally:
            # Re-enable foreign key checks
            connection.execute(text("SET session_replication_role = 'origin';"))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
