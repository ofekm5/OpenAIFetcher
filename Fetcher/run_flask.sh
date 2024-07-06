#!/bin/bash

source venv/bin/activate
python -m flask run


alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

#run tests
pytest

