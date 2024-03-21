import requests
import dash
from dash import dcc, html, Output, Input, State
import plotly.graph_objs as go
import plotly.express as px

url = "https://api.themoviedb.org/3/trending/person/week?language=en-US"
url2 = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
url3 = "https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZmFlZDM4YjAzMWRlMDU0ZTdkYjBjMzAyMzk5NTA5YiIsInN1YiI6IjY1NDY2YjgwMjg2NmZhMDEzOGE2YzljZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ltqjdF7wDRCWDtMgde-V6wXnUshGKSFGB7oG3dNSimE"
}

response = requests.get(url, headers=headers)
data = response.json()['results']
data_people = [person['original_name'] for person in data]
data_popularity = [person['popularity'] for person in data]

response2 = requests.get(url2, headers=headers)
data2 = response2.json()['results']
data_vote = [movies["vote_average"] for movies in data2]
data_popularity2 = [movies['popularity'] for movies in data2]
data_movie = [movies['title'] for movies in data2]


response3 = requests.get(url3, headers=headers)
data3 = response3.json()

if 'results' in data3 and isinstance(data3['results'], list) and len(data3['results']) > 0:
    countries = {}
    total_series = len(data3['results'])

    for result in data3['results']:
        countries.setdefault(result['origin_country'][0], 0)
        countries[result['origin_country'][0]] += 1

    labels = list(countries.keys())
    values = [(count / total_series) * 100 for count in countries.values()]

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig2.update_traces(textinfo='percent', textposition='inside', hole=0.4)
    fig2.update_layout(title_text="- Répartition des séries par pays d'origine :")

else:
    print("Aucune donnée disponible ou format incorrect.")


bar_chart = go.Bar(
    x=data_popularity,
    y=data_people,
    orientation='h',
    marker = dict(color="red"),
)

layout = go.Layout(
    title="- Comparaison de la popularité des acteurs en Novembre 2023 :",
    xaxis=dict(title='Popularité'),
    yaxis=dict(title='Acteurs'),

)
figure = go.Figure(data=[bar_chart], layout=layout)


fig = px.scatter(x=data_popularity2, y=data_vote, text=data_movie)
fig.update_traces(textposition='top center',marker=dict(color='orange'))
fig.update_layout(
    title="- Popularité et note moyenne des dernières sorties de cinéma :",
    xaxis_title="Popularité",
    yaxis_title="Note Moyenne",
)

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Heebo&display=swap',
    {
        'href': 'https://fonts.googleapis.com/css2?family=Heebo&display=swap',
        'rel': 'stylesheet'
    },
    'https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css',

]
your_data = {
    'X': [1, 2, 3, 4, 5],
    'Y': [5, 4, 3, 2, 1]
}

figuredata = {
        'data': [{'x': your_data['X'], 'y': your_data['Y'], 'type': 'scatter', 'mode': 'markers', 'name': 'Nuage de points'}],
        'layout': {'title': f'- Nuage de points mis à jour :', 'xaxis': {'title': 'Axe X'}, 'yaxis': {'title': 'Axe Y'}}
    }

app = dash.Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css'],suppress_callback_exceptions=True)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("PrimeAnalyse", className="text-white"),
        ], className="flex-0"),
        html.Nav(children=[
            html.Ul(children=[
            ], className="list-inline m-0 p-0")
        ], className="flex-2 d-flex justify-content-space-evenly")
    ], className="m-0 p-0 d-flex align-items-center bg-dark", style={'height': '70px', 'font-family': 'Heebo, sans-serif'}),
    html.H1("Analyse et visualisation cinématographique:", style={'text-align': 'center', 'font-family': 'Heebo, sans-serif', 'margin-top' : '2rem'}),
    html.Div(id='selected-graph'),
html.Button('Update', id='update-button', n_clicks=0),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Data.2 : Nuage de points',children=[
                html.Div(dcc.Graph(figure=figuredata, id='nuage-graph'))
            ]),
            dcc.Tab(label='Acteurs', children=[
                html.Div(dcc.Graph(figure=figure, id='acteurs-graph'))
            ]),
            dcc.Tab(label='Films', children=[
                html.Div(dcc.Graph(figure=fig, id='films-graph'))
            ]),
            dcc.Tab(label='Séries', children=[
                html.Div(dcc.Graph(figure=fig2, id='series-graph'))
            ])
        ], style={'display': 'flex', 'justify-content': 'center'})
    ])
])


total_clicks = 0

@app.callback(
    Output('selected-graph', 'children'),
    [Input('update-button', 'n_clicks')],
    [State('acteurs-graph', 'clickData'),
     State('films-graph', 'clickData'),
     State('series-graph', 'clickData'),
     State('nuage-graph', 'clickData')]
)
def update_graph(n_clicks, acteurs_click, films_click, series_click, nuage_click):
    global total_clicks

    if n_clicks is not None:
        total_clicks += 1
        return f"Nombre de clics sur le graphique : {total_clicks}"
    else:
        return "Aucun clic pour le moment."


if __name__ == '__main__':
    app.run_server(debug=True)
