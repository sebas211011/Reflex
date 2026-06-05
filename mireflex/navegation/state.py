import reflex as rx
from . import routes


class NavState(rx.State):

    def to_home(self):
        return rx.redirect(routes.HOME)
    
    def to_data_base(self):
        return rx.redirect(routes.DATABASE)