"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .pages.base import base_page
from .folder_datos.datos import data_base

from rxconfig import config


class State(rx.State):
    """The app state."""

    
def index() -> rx.Component:
    # Welcome Page (Index)
    index_child = rx.container(
        rx.vstack(
            rx.heading(
                "Welcome to Reflex!",
                 size="9"
            ),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        ),
    )
    return base_page(index_child)



app = rx.App()
app.add_page(index)
app.add_page(data_base,route="/data_base")