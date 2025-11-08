"""
Dashboard de preços de GLP - janeiro/2024
Requisitos:
- 5 tipos de gráficos
- 2 filtros interativos
- títulos e legendas claras
"""

import pandas as pd
from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

#tratando os dados
df = pd.read_csv("datasets/GLP/glp-2024-01.csv", sep=None, engine="python", encoding="utf-8-sig")
df = df.rename(
    columns={
        "Regiao - Sigla": "regiao",
        "Estado - Sigla": "uf",
        "Municipio": "municipio",
        "Revenda": "revenda",
        "Produto": "produto",
        "Data da Coleta": "data_coleta",
        "Valor de Venda": "valor_venda",
        "Valor de Compra": "valor_compra",
        "Bandeira": "bandeira",
    }
)


df["data_coleta"] = pd.to_datetime(df["data_coleta"], format="%d/%m/%Y")

df["valor_venda"] = (
    df["valor_venda"]
    .astype(str)
    .str.replace(".", "", regex=False) 
    .str.replace(",", ".", regex=False)
    .astype(float)
)

df["bandeira"] = df["bandeira"].fillna("Não informada")
df["regiao"] = df["regiao"].fillna("Não informada")

regioes = sorted(df["regiao"].dropna().unique())
bandeiras = sorted(df["bandeira"].dropna().unique())
data_min = df["data_coleta"].min()
data_max = df["data_coleta"].max()

#app
app = Dash(__name__)
app.title = "Dashboard GLP"

app.layout = html.Div(
    style={"margin": "20px"},
    children=[
        html.H1("Dashboard de Preços de GLP - 2024", style={"textAlign": "center"}),
        html.P(
            "Explore preços médios de GLP por estado, região e bandeira com base nos dados coletados pela ANP.",
            style={"textAlign": "center"},
        ),

        #definindo filtros
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginBottom": "20px"},
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
                    style={"minWidth": "200px", "flex": "1"}
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
                    style={"minWidth": "200px", "flex": "1"}
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
                    style={"minWidth": "220px", "flex": "1"}
                ),
            ],
        ),

        #graficos
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    children=[
                        html.H3("Preço médio por estado"),
                        dcc.Graph(id="grafico-estado"),
                    ],
                    style={"flex": "2", "minWidth": "350px"}
                ),
                html.Div(
                    children=[
                        html.H3("Participação por bandeira"),
                        dcc.Graph(id="grafico-pizza-bandeira"),
                    ],
                    style={"flex": "1", "minWidth": "300px"}
                ),
            ],
        ),

        #
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginTop": "20px"},
            children=[
                html.Div(
                    children=[
                        html.H3("Evolução do preço médio por região"),
                        dcc.Graph(id="grafico-linha-regiao"),
                    ],
                    style={"flex": "1", "minWidth": "350px"}
                ),
            ],
        ),

        
        html.Div(
            style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginTop": "20px"},
            children=[
                html.Div(
                    children=[
                        html.H3("Preço médio por bandeira"),
                        dcc.Graph(id="grafico-bandeira"),
                    ],
                    style={"flex": "1", "minWidth": "350px"}
                ),
                html.Div(
                    children=[
                        html.H3("Distribuição de preços (histograma)"),
                        dcc.Graph(id="grafico-histograma"),
                    ],
                    style={"flex": "1", "minWidth": "350px"}
                ),
                html.Div(
                    children=[
                        html.H3("Boxplot por bandeira"),
                        dcc.Graph(id="grafico-box-bandeira"),
                    ],
                    style={"flex": "1", "minWidth": "350px"}
                ),
            ],
        ),
    ],
)


@app.callback(
    [
        Output("grafico-estado", "figure"),
        Output("grafico-linha-regiao", "figure"),
        Output("grafico-bandeira", "figure"),
        Output("grafico-histograma", "figure"),
        Output("grafico-box-bandeira", "figure"),
        Output("grafico-pizza-bandeira", "figure"),
    ],
    [
        Input("regiao-filter", "value"),
        Input("bandeira-filter", "value"),
        Input("date-filter", "start_date"),
        Input("date-filter", "end_date"),
    ],
)
def atualizar_graficos(regioes_sel, bandeiras_sel, data_inicio, data_fim):
    
    dados = df.copy()

    if data_inicio is not None and data_fim is not None:
        dados = dados[(dados["data_coleta"] >= data_inicio) & (dados["data_coleta"] <= data_fim)]

    if regioes_sel and len(regioes_sel) > 0:
        dados = dados[dados["regiao"].isin(regioes_sel)]

    if bandeiras_sel and len(bandeiras_sel) > 0:
        dados = dados[dados["bandeira"].isin(bandeiras_sel)]

    
    estado_media = (
        dados.groupby("uf")["valor_venda"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_estado = px.bar(
        estado_media,
        x="uf",
        y="valor_venda",
        labels={"uf": "Estado", "valor_venda": "Preço médio (R$)"},
        title="Preço médio de GLP por estado",
    )
    fig_estado.update_layout(xaxis_tickangle=-45)

    
    regiao_tempo = (
        dados.groupby(["data_coleta", "regiao"])["valor_venda"]
        .mean()
        .reset_index()
        .sort_values("data_coleta")
    )
    fig_linha = px.line(
        regiao_tempo,
        x="data_coleta",
        y="valor_venda",
        color="regiao",
        markers=True,
        labels={"data_coleta": "Data de coleta", "valor_venda": "Preço médio (R$)", "regiao": "Região"},
        title="Evolução do preço médio por região",
    )

    
    bandeira_media = (
        dados.groupby("bandeira")["valor_venda"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_bandeira = px.bar(
        bandeira_media,
        x="bandeira",
        y="valor_venda",
        labels={"bandeira": "Bandeira", "valor_venda": "Preço médio (R$)"},
        title="Preço médio por bandeira",
    )
    fig_bandeira.update_layout(xaxis_tickangle=-45)

    
    fig_hist = px.histogram(
        dados,
        x="valor_venda",
        nbins=20,
        labels={"valor_venda": "Preço de venda (R$)"},
        title="Distribuição dos preços de venda",
    )

    
    fig_box = px.box(
        dados,
        x="bandeira",
        y="valor_venda",
        points=False,
        labels={"bandeira": "Bandeira", "valor_venda": "Preço de venda (R$)"},
        title="Variação do preço por bandeira",
    )
    fig_box.update_layout(xaxis_tickangle=-45)

    
    bandeira_count = dados["bandeira"].value_counts().reset_index()
    bandeira_count.columns = ["bandeira", "qtd"]
    fig_pizza = px.pie(
        bandeira_count,
        names="bandeira",
        values="qtd",
        title="Participação das bandeiras na amostra",
    )

    return fig_estado, fig_linha, fig_bandeira, fig_hist, fig_box, fig_pizza


#rodando o dash
if __name__ == "__main__":
    app.run(debug=True)
