from dash import Dash, html, dash_table
import pandas as pd

df = pd.DataFrame([{'Hello':1, "World":2}])

app = Dash()

app.layout = [
    html.Div(children='Hello World'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=5)
]

if __name__ == '__main__':
    app.run(debug=True)
