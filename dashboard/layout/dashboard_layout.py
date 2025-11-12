from dash import html, dcc

def build_layout(df):
    regioes = sorted(df["regiao"].dropna().unique())
    bandeiras = sorted(df["bandeira"].dropna().unique())
    data_min = df["data_coleta"].min()
    data_max = df["data_coleta"].max()
    GRID_GAP = "20px"

    return html.Div(
        style={"margin": "20px"},
        children=[
            html.H1("Dashboard de Preços de GLP - 2025", style={"textAlign": "center"}),
            html.P(
                "Explore preços médios de GLP por estado, região e bandeira com base nos dados coletados pela ANP.",
                style={"textAlign": "center"},
            ),

            html.Div(
                className="card",
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))",
                    "gap": GRID_GAP,
                    "marginBottom": "20px",
                },
                children=[
                    html.Div(
                        children=[
                            html.Label("Filtrar por Região"),
                            dcc.Dropdown(
                                id="regiao-filter",
                                options=[{"label": r, "value": r} for r in regioes],
                                multi=True,
                                placeholder="Selecione uma ou mais regiões",
                            ),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.Label("Filtrar por Bandeira"),
                            dcc.Dropdown(
                                id="bandeira-filter",
                                options=[{"label": b, "value": b} for b in bandeiras],
                                multi=True,
                                placeholder="Selecione uma ou mais bandeiras",
                            ),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.Label("Período de Coleta"),
                            dcc.DatePickerRange(
                                id="date-filter",
                                start_date=data_min,
                                end_date=data_max,
                                min_date_allowed=data_min,
                                max_date_allowed=data_max,
                                display_format="DD/MM/YYYY",
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "2fr 1fr",
                    "gap": GRID_GAP,
                },
                children=[
                    html.Div(
                        className="card",
                        children=[
                            html.H3("Preço médio por estado"),
                            dcc.Graph(id="grafico-estado", style={"height": "420px"}),
                        ],
                    ),
                    html.Div(
                        className="card",
                        children=[
                            html.H3("Participação por bandeira"),
                            dcc.Graph(id="grafico-pizza-bandeira", style={"height": "380px"}),
                        ],
                    ),
                ],
            ),

            html.Div(
                className="card",
                style={"marginTop": "20px"},
                children=[
                    html.Div(
                        children=[
                            html.H3("Evolução do preço médio por região"),
                            dcc.Graph(id="grafico-linha-regiao", style={"height": "420px"}),
                        ],
                    ),
                ],
            ),

            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                    "gap": GRID_GAP,
                    "marginTop": "20px",
                },
                children=[
                    html.Div(
                        className="card",
                        children=[
                            html.H3("Preço médio por bandeira"),
                            dcc.Graph(id="grafico-bandeira", style={"height": "380px"}),
                        ],
                    ),
                    html.Div(
                        className="card",
                        children=[
                            html.H3("Distribuição de preços (histograma)"),
                            dcc.Graph(id="grafico-histograma", style={"height": "380px"}),
                        ],
                    ),
                    html.Div(
                        className="card",
                        children=[
                            html.H3("Boxplot por bandeira"),
                            dcc.Graph(id="grafico-box-bandeira", style={"height": "380px"}),
                        ],
                    ),
                ],
            ),
        ],
    )
