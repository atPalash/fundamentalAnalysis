import yfinance as yf
from yahoo_fin import stock_info
import plotly.graph_objs as go


class YFinanceLiveData:
    def __init__(self, stock_config: dict, show_fig=False):
        """
        Initiate config with interval and period if historical data is required. Else for latest data just send the
        tickers.
        """
        self.stock_config = stock_config
        self.show_fig = show_fig
        self.data = None

    def get_tickers_historical_data(self):
        """
        Get panda dataframe of historical data of all the tickers.
        """
        self.data = yf.download(tickers=self.stock_config['tickers'], period=self.stock_config['period'],
                                interval=self.stock_config['interval'], progress=False)
        self.data = self.data.fillna(method="ffill")
        return self.data

    def get_tickers_latest_price(self):
        """
        Get the current price of tickers as dict.
        """
        ret = {}
        for tick in self.stock_config['tickers']:
            ret[tick] = stock_info.get_live_price(tick)
        return ret

    def get_ticker_info(self):
        ret = {}
        for tick in self.stock_config['tickers']:
            ret[tick] = yf.Ticker(tick)
        return ret

    def plot_data(self, ticker):
        """
        A Debug plot method
        """
        if self.show_fig:

            if self.data is None:
                self.get_tickers_historical_data()

            # declare figure
            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(x=self.data.index,
                                         open=self.data['Open'][ticker],
                                         high=self.data['High'][ticker],
                                         low=self.data['Low'][ticker],
                                         close=self.data['Close'][ticker], name='market data'))

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