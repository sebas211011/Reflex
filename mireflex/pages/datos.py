import reflex as rx
from .base import base_page


def data_base() -> rx.Component:
    # Welcome Page (Index)
    data_base_child = rx.container(
        rx.vstack(
            rx.heading(
                "Welcome to Reflex!",
                 size="9"
            ),
            rx.text(
                "aydio",
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
    return base_page(data_base_child)