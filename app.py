from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
app.title = "YellowPages EG Scraper"

# Set the layout
app.layout = create_layout(app)

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=False)  # Use `app.run()` instead of `app.run_server()`
