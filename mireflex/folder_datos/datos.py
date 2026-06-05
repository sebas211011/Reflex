import reflex as rx
import sqlmodel as xd
from datetime import datetime
from typing import List,Optional,Dict
from .model import Dato
from ..pages import base_page

class DatoState(rx.State):
    """Estado para nuestra aplicacion de tareas"""

    new_title:str=""
    new_description:str=""

    #lista de tareas
    datos:List[Dict]=[ ]

    #variable de identificacion
    editing_id:Optional[int]=None

    def load_datos(self):
        """carga las tareas desde la base de datos"""
        try:
            with rx.session() as session:
                #obtener todas las tareas de la base de datos
                db_datos=session.exec(xd.select(Dato)).all()

                #convertir en diccionario
                formatted_datos=[]
                for item in db_datos:
                    dato_dict=item.model_dump()
                    dato_dict["formatted_date"]=(
                        item.created_at.strftime("%d/%m/%Y %H:%M")
                        if item.created_at
                        else ""
                    )

                    formatted_datos.append(dato_dict)
                self.datos=formatted_datos
        except Exception as e:
            print(f"error al cargar datos:{e}")
            self.datos


    def add_datos(self,form_data:dict):
        """Agrega una nueva tarea"""
        title=form_data.get("title","").strip()
        description=form_data.get("description","").strip()

        if not title:
            return rx.window_alert("el titulo no puede estar vacio")
        
        try:
            with rx.session() as session:
                dato=Dato(
                    title=title,
                    description=description if description else None,
                    created_at=datetime.now()
                )
                session.add(dato)
                session.commit()

                #recargar tareas
                self.load_datos()
                
                #Mensaje de confirmacion
                return[
                    rx.call_script("document.getElementById('data_form').reset();"),
                    rx.window_alert("tarea agregada correctamente")
                ]
        except Exception as e:
            return rx.window_alert(f"Error al guardar la tarea:{str(e)}")
     

    def toggle_complete(self,dato_id:int):
        """Marca o desmarca una tarea como completada"""
        try:
            with rx.session() as session:
                statement=xd.select(Dato).where(Dato.id==dato_id)
                dato=session.exec(statement).first()
                if dato:
                    dato.completed=not dato.completed
                    session.add(dato)
                    session.commit()
                    
                    self.load_datos()

        except Exception as e:
            return rx.window_alert(f"Error al actualizar la tarea: {str(e)}")


    def delete_dato(self,dato_id:int):
        """funcion para borrar datos"""

        try:
            with rx.session() as session:
                dato=session.query(Dato).filter(Dato.id==dato_id).first()

                if dato:
                    session.delete(dato)
                    session.commit()
                    self.load_datos()
        except Exception as e:
            return rx.window_alert(f"No se pudo eliminar la tarea: {str(e)} ")
        
    
def dato_item(dato)->rx.Component:
    """Componente para mostrar una tarea individual"""
    return rx.hstack(
        rx.checkbox(
            is_checked=dato.completed,
            on_change=lambda:DatoState.toggle_complete(dato.id),
        ),
        rx.vstack(
            rx.text(
                dato.title,
                text_decoration=rx.cond(
                    dato.completed,
                    "line_through",
                    "none"
                ),
                font_weight='bold'
            ),
            rx.text(
                rx.cond(
                    dato.description != "",
                    dato.description,
                    "Sin descripción"
                ),
                color="gray",
                font_size="1rem"
            ),
            rx.hstack(
                rx.text(
                    "Creado:",
                    color="gray",
                    font_size="1rem"
                ),
                rx.text(
                    dato.formatted_date,
                    color="gray",
                    font_size="1rem"
                ),
                spacing="1"
            ),
            align_items="start",
            width="100%"
        ),
        rx.spacer(),
        rx.button(
            "Eliminar",
            on_click=lambda:DatoState.delete_dato(dato.id),
            color_scheme="red",
            size="1"
        ),
        width="100%",
        border="1px solid",
        border_color="gray.200",
        border_radius="5px",
        padding="3",
        margin_y="2"
    )


def dato_list():
    """Componente para mostrar la lista de tareas"""
    return rx.cond(
        DatoState.datos.length() > 0,
        rx.vstack(
            rx.foreach(
                DatoState.datos,
                dato_item
            ),
            width="100%",
            padding="4"
        ),
        rx.box(
            rx.text(
                "No hay tareas pendientes"
            ),
            padding="4",
            text_align="center",
            color="gray.500",
            spacing='4'
        )
    )


def dato_form():
    """Formulario Para agregar Tareas"""
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder='Titulo',
                name='title',
                width='100%'
            ),
            rx.text_area(
                placeholder='Descripcion',
                name='description',
                width='100%'
            ),
            rx.button(
                "agregar Tarea",
                type="submit",
                color_scheme='teal',
                width='100%'
            ),
            padding="4",
            width='100%',
            spacing='4'
        ),
        on_submit=DatoState.add_datos,
        id='dato_form',
        padding='4',
        width='100%'
    )


def data_base()->rx.Component:
    """pagina de la base de datos"""
    data_child= rx.center(
        rx.vstack(
            rx.fragment(
                rx.heading(
                    'lista de tareas',
                    size='7',
                    margin_y="70px",
                    margin_x='100px',
                    aling='center',
                    color_scheme="green",
                    spacing="0"
                ),
            ),
            rx.divider(),
            dato_form(),
            rx.divider(),
            dato_list(),
            padding="4",
            width="100%",
            max_width="600px",
            border_radius='5px',
            background_color="mint",
            color='white'
        ),
        color_scheme='dark',
        background_color="#121212",
        min_heigth='100vh',
        padding='4',
        center_content=True
    )
    return base_page(data_child)