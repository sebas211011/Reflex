import reflex as rx

config = rx.Config(
    app_name="mireflex",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)