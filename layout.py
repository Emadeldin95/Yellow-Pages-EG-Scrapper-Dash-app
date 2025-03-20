from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from header import create_header

def create_layout(app):
    return dbc.Container([
        create_header(),

        # ✅ Centered Keyword Input (40% Page Width)
        dbc.Row([
            dbc.Col([], width=3),
            dbc.Col([
                dbc.Input(id="keyword-input", type="text", placeholder="Search for Companies by Keywords",
                          style={"width": "100%", "textAlign": "center", "fontSize": "16px", "padding": "10px"})
            ], width=6),
            dbc.Col([], width=3)
        ], className="mb-4 justify-content-center"),

        # ✅ Fancy Status Indicator & Buttons (Side by Side)
        dbc.Row([
            dbc.Col([
                dbc.Alert(id="status-indicator", color="info", className="text-center", children="Status: Idle | Companies Scraped: 0", style={
                    "fontSize": "18px",
                    "fontWeight": "bold",
                    "borderRadius": "15px",
                    "padding": "10px",
                    "width": "100%"
                })
            ], width=4),

            dbc.Col([
                dbc.Button("Start Scraping", id="start-btn", color="success", className="me-2"),
                dbc.Button("Stop Scraping", id="stop-btn", color="danger", className="me-2"),
                dbc.Button("Download CSV", id="download-btn", color="primary", className="me-2"),
                dcc.Download(id="download-data")  # ✅ Ensures proper file download
            ], width=6, className="text-center")
        ], className="mb-4 justify-content-center align-items-center"),

        # ✅ Data Table
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id="data-table",
                    columns=[
                        {"name": "Company Name", "id": "name"},
                        {"name": "Phone", "id": "phone"},
                        {"name": "Address", "id": "address"},
                        {"name": "Website", "id": "website"},
                    ],
                    data=[],
                    page_size=10,
                    style_table={"width": "100%", "overflowX": "auto"},
                    style_cell={
                        "whiteSpace": "normal",
                        "textAlign": "left",
                        "maxWidth": "20vw",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "wordWrap": "break-word"
                    }
                )
            ], width=12)
        ]),

        # ✅ Auto-refresh Interval
        dcc.Interval(id="interval", interval=5000, n_intervals=0)
    ], fluid=True)
