# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.base import Base  # noqa
from app.models.db import *  # noqa
