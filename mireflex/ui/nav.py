import reflex as rx
from mireflex.navegation.state import NavState
from mireflex.navegation import routes



def navbar_link(text: str, url: str) -> rx.Component:
        return rx.link(
              rx.text(
                    text,
                    size="4",
                    weight="medium"
                    ), 
                    href=url
        )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="https://cdn-icons-png.flaticon.com/512/831/831378.png ",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("pedro", size="7", weight="bold"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home",routes.HOME),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.text("servicios", size="4", weight="medium"),
                                rx.icon("chevron-down"),
                                weight="medium",
                                variant="ghost",
                                size="3",
                            ),
                        ),
                        rx.menu.content(
                            rx.menu.item("pa aqui"),
                            rx.menu.item("o aqui"),
                            rx.menu.item("o pa aca"),
                        ),
                    ),
                    navbar_link("vente pa aca", routes.DATABASE),
                    justify="end",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="https://cdn-icons-png.flaticon.com/512/831/831378.png",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Pedro", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item(
                              "Home",
                              on_click=NavState.to_home
                              ),
                        rx.menu.sub(
                            rx.menu.sub_trigger("Services"),
                            rx.menu.sub_content(
                                rx.menu.item("Service 1"),
                                rx.menu.item("Service 2"),
                                rx.menu.item("Service 3"),
                            ),
                        ),
                        rx.menu.item("About"),
                        rx.menu.item("Pricing"),
                        rx.menu.item(
                              "Vente pa aca",
                              on_click=NavState.to_data_base
                              ),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )