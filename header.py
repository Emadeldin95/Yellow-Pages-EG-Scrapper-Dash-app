from dash import html
import dash_bootstrap_components as dbc

def create_header():
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("YellowPages EG Scraper", className="ms-2", style={"fontSize": "24px", "fontWeight": "bold"})
        ]),
        color="dark",
        dark=True,
        className="mb-4"
    )
