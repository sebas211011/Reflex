import reflex as rx
from ..ui.nav import navbar

def base_page(child: rx.Component, *args, **kargs) -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            child,
        ),
        rx.color_mode.button(
            position="bottom-right"
        )
    )