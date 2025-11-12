from dash import Dash
from data.loader import load_data
from layout.dashboard_layout import build_layout
from callbacks.dashboard_callbacks import register_callbacks

df = load_data()

app = Dash(__name__)
app.title = "Dashboard GLP"
app.layout = build_layout(df)

register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)