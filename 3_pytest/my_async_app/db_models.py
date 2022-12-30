from sqlalchemy import Column, TEXT

from my_async_app.db import Base


class MyTable(Base):
    __tablename__ = 'my_table'

    text_field = Column(TEXT, primary_key=True)
