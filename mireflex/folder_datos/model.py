import reflex as rx
from datetime import datetime
import sqlmodel

class Dato(sqlmodel.SQLModel,table=True):
    """Modelo Para Representar Una Tarea"""
    #zzz
    id:int | None=sqlmodel.Field(default=None, primary_key=True)

    title: str
    description: str
    completed: bool = False

    #establecer la fecha
    created_at: datetime = sqlmodel.Field(
        default_factory= datetime.now,
        sa_column= sqlmodel.Column(
        sqlmodel.DateTime(timezone= True),
        server_default= sqlmodel.func.now()
        )
    )