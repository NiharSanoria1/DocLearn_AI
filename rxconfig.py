import reflex as rx

config = rx.Config(
    app_name="DocLearn_AI",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)