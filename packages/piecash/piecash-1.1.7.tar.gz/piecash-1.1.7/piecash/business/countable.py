from sqlalchemy import Column, VARCHAR


class Countable:
    id = Column("id", VARCHAR(length=2048), nullable=False)
