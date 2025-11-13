from dash import Input, Output
import pandas as pd
import plotly.express as px

def register_callbacks(app, df):
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

        if data_inicio and data_fim:
            di = pd.to_datetime(data_inicio)
            df_ = pd.to_datetime(data_fim)
            dados = dados[(dados["data_coleta"] >= di) & (dados["data_coleta"] <= df_)]

        if regioes_sel:
            dados = dados[dados["regiao"].isin(regioes_sel)]

        if bandeiras_sel:
            dados = dados[dados["bandeira"].isin(bandeiras_sel)]

        
        estado_media = (
            dados.groupby("uf", dropna=True)["valor_venda"]
            .mean().sort_values(ascending=False).reset_index()
        )
        fig_estado = px.bar(estado_media, x="uf", y="valor_venda", title="Preço médio por estado")
        fig_estado.update_xaxes(title_text="Estado")
        fig_estado.update_yaxes(title_text="Preço médio (R$)")

        regiao_tempo = (
            dados.groupby(["data_coleta", "regiao"], dropna=True)["valor_venda"]
            .mean().reset_index().sort_values("data_coleta")
        )
        fig_linha = px.line(regiao_tempo, x="data_coleta", y="valor_venda", color="regiao")
        fig_linha.update_xaxes(title_text="Data de coleta")
        fig_linha.update_yaxes(title_text="Preço médio (R$)")

        bandeira_media = (
            dados.groupby("bandeira", dropna=True)["valor_venda"]
            .mean().sort_values(ascending=False).reset_index()
        )
        fig_bandeira = px.bar(bandeira_media, x="bandeira", y="valor_venda")
        fig_bandeira.update_xaxes(title_text="Bandeira")
        fig_bandeira.update_yaxes(title_text="Preço médio (R$)")

        fig_hist = px.histogram(dados, x="valor_venda", nbins=20)
        fig_hist.update_xaxes(title_text="Preço de venda (R$)")
        fig_hist.update_yaxes(title_text="Contagem")
        fig_box = px.box(dados, x="bandeira", y="valor_venda")
        fig_box.update_xaxes(title_text="Bandeira")
        fig_box.update_yaxes(title_text="Preço de venda (R$)")
        bandeira_count = dados["bandeira"].value_counts().reset_index()
        bandeira_count.columns = ["bandeira", "qtd"]
        fig_pizza = px.pie(bandeira_count, names="bandeira", values="qtd")

        return fig_estado, fig_linha, fig_bandeira, fig_hist, fig_box, fig_pizza
