import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go


class YFinanceLiveData:
    def __init__(self, stock_config: dict, show_fig=False):
        self.stock_config = stock_config
        self.show_fig = show_fig
        self.data = None

    def get_ticker_data(self):
        self.data = yf.download(tickers=self.stock_config['tickers'], period=self.stock_config['period'],
                                interval=self.stock_config['interval'], progress=False)
        return self.data

    def plot_data(self):
        if self.show_fig:
            # declare figure
            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(x=self.data.index,
                                         open=self.data['Open'],
                                         high=self.data['High'],
                                         low=self.data['Low'],
                                         close=self.data['Close'], name='market data'))

            # Add titles
            fig.update_layout(
                title='Uber live share price evolution',
                yaxis_title='Stock Price (USD per Shares)')

            # X-Axes
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=15, label="15m", step="minute", stepmode="backward"),
                        dict(count=45, label="45m", step="minute", stepmode="backward"),
                        dict(count=1, label="HTD", step="hour", stepmode="todate"),
                        dict(count=3, label="3h", step="hour", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )

            # Show
            fig.show()
