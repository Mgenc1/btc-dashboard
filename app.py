from dash import Dash, dcc, html
import plotly.graph_objects as go
from binance import ThreadedWebsocketManager
import pandas as pd

# Dash uygulaması
app = Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=5000)  # 5 saniyede bir güncelle
])

# WebSocket ile veri çekme
twm = ThreadedWebsocketManager()
twm.start()
twm.start_symbol_ticker_socket(symbol='BTCUSDT', callback=lambda msg: update_graph(msg))

# Grafik güncelleme fonksiyonu
def update_graph(msg):
    # Veriyi işle ve grafiği güncelle
    # (Örnek: Son fiyatı ekle)
    pass
app = Dash(__name__)
server = app.server  # Bu satırı ekleyin

if __name__ == '__main__':
    app.run_server(debug=True)