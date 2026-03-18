from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Pharma Supply Chain Risk Dashboard"
server = app.server

# ── Import layout and callbacks ─────────────────────────────
import layout      # registers app.layout
import callbacks   # registers all callbacks


if __name__ =="__main__":
    app.run(debug=False, host='0.0.0.0', port=8050)