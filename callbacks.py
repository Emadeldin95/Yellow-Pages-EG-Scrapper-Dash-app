from dash import Input, Output, State, ctx, dcc, html
import dash
import pandas as pd
import os
from scraper import YellowPagesScraper

scraper = YellowPagesScraper()
CSV_FILE_PATH = "scraped_data.csv"  # ✅ Define file path

def register_callbacks(app):
    @app.callback(
        [Output("data-table", "data"), Output("status-indicator", "children")],
        Input("start-btn", "n_clicks"),
        Input("stop-btn", "n_clicks"),
        Input("interval", "n_intervals"),
        State("keyword-input", "value"),
        prevent_initial_call=True
    )
    def handle_scraping(start_clicks, stop_clicks, n_intervals, keyword):
        triggered_id = ctx.triggered_id

        if triggered_id == "start-btn" and keyword:
            scraper.start_scraping(keyword)

        elif triggered_id == "stop-btn":
            scraper.stop_scraping()

        status_data = scraper.get_status()
        status_text = f"Status: {status_data['status']} | Companies Scraped: {status_data['scraped_count']}"

        return scraper.get_data(), status_text

    @app.callback(
        Output("download-data", "data"),
        Input("download-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def download_csv(n_clicks):
        """✅ Saves and downloads the CSV file from scraped data."""
        data = scraper.get_data()
        if not data:
            return None

        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE_PATH, index=False, encoding="utf-8")  # ✅ Save CSV file

        return dcc.send_file(CSV_FILE_PATH)  # ✅ Send the file for download
