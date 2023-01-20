from sqlalchemy import Column, TEXT

from db import Base


class MyTable(Base):
    __tablename__ = 'my_table'

    text_field = Column(TEXT, primary_key=True)
