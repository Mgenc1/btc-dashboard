from dash import Dash, dcc, html, Output, Input
import plotly.graph_objects as go
from binance.client import Client
import pandas as pd
import os

# Binance API anahtarları (ortam değişkenlerinden alıyoruz)
api_key = os.environ.get('IfruJmZdcoKFYaGU80djwrf9T44lAfMX80MQ2CxMNFYt3Abskxsvok5TUXfUOEQv')
api_secret = os.environ.get('a5LrVcYZ2a8QA9w5EkAUKebTfmCW8xdunrOIuwKwyCFcFDPfQOrEw4oGLk8SOd6k')

client = Client(api_key, api_secret)

# Dash uygulaması
app = Dash(__name__)
server = app.server  # Render için gerekli

# Başlangıç verisi
def get_data():
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
    df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close',
                                       'Volume', 'Close Time', 'Quote Asset Volume',
                                       'Number of Trades', 'Taker Buy Base Asset Volume',
                                       'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)
    return df

# Uygulama düzeni
app.layout = html.Div([
    html.H1('BTC/USDT Canlı Fiyat Grafiği'),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=5*1000,  # Her 5 saniyede bir güncelle (5000 milisaniye)
        n_intervals=0
    )
])

# Grafiği güncelleyen callback fonksiyonu
@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals'))
def update_graph_live(n):
    df = get_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Open Time'],
        y=df['Close'],
        mode='lines',
        name='BTCUSDT'
    ))
    fig.update_layout(title='BTC/USDT Canlı Fiyat Grafiği',
                      xaxis_title='Zaman',
                      yaxis_title='Fiyat (USDT)')
    return fig

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)
