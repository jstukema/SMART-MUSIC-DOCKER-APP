create:
	alembic revision -m "create_main_tables"

downgrade:
	alembic downgrade base

upgrade:
	alembic upgrade head

all: downgrade upgrade