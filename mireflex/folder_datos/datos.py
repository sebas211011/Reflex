import reflex as rx
import sqlmodel as xd
from datetime import datetime
from typing import List,Optional,Dict
from .model import Dato


class DatoState(rx.state):
    """Estado para nuestra aplicacion de tareas"""

    new_title:str=""
    new_description:str=""

    #lista de tareas
    datos=List[Dict]=[ ]

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
        

    def delete_dato(self,dato_id:int):
        """funcion para borrar datos"""

        try:
            with rx.session() as session:
                dato=session.query(Dato).filter(Dato.id==dato.id).first()

                if dato:
                    session.delete(dato)
                    session.commit()
                    self.load_datos()
        except Exception as e:
            return rx.window_alert(f"No se pudo eliminar la tarea: {str(e)} ")