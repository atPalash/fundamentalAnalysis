from ai import ai_model_interface
from ai.lstm.lstm_predictor import LstmPredictor
from dataFetch.yfinance_live_data import YFinanceLiveData


class LstmModel(ai_model_interface.AiModelInterface):
    def __init__(self, name, config, past_data_count=50, epoch=20, debug=False, debug_count=2):
        super().__init__(name, config, past_data_count, debug, debug_count)
        self.data = None
        self.past_data_count = past_data_count
        self.lstm = None

        self.selected_stocks_config = config['selected_stocks_config']
        self.lstm_config = config['lstm_config']

        self.debug = debug
        self.debug_count = debug_count
        self.epoch = epoch
        if self.debug:
            self.epoch = 5
        self.selected_feature = 'Close'

    def build_model(self):
        self.__initialise_data()
        self.lstm.init_model(selected_stocks_df=self.data, train_test_ratio=0.8, epochs=self.epoch)
        self.lstm.build_model()

    def predict_with_model(self, stock: str):
        self.__initialise_data()
        ticker = stock.upper() + '.NS'
        prediction, trend = self.lstm.predict(
            current_data=self.data[self.selected_feature][ticker][-self.past_data_count * 2:], stock_ns=ticker)
        return prediction, trend

    def __initialise_data(self):
        selected_stocks = self.selected_stocks_config['to_buy'] + self.selected_stocks_config['to_sell']
        selected_stocks = [stock + ".NS" for stock in selected_stocks]

        # fetch data till current
        stock_config = {
            'tickers': selected_stocks,
            'interval': self.lstm_config['yf_interval'],
            'period': self.lstm_config['yf_period']
        }
        yfinance = YFinanceLiveData(stock_config)
        self.data = yfinance.get_tickers_historical_data()

        if self.lstm is None:
            self.past_data_count = self.past_data_count
            self.lstm = LstmPredictor(model_save_folder_path=self.lstm_config['models_folder'],
                                      selected_feature=self.selected_feature,
                                      past_data_point_count=self.past_data_count, selected_stocks=selected_stocks,
                                      debug=self.debug, debug_count=self.debug_count)

    # This will be run by cron daily at the end of day
    # if __name__ == "__main__":
    #     lstmodel = LstmModel()
    #     lstmodel.build_model()

    '''
    try:
        args = sys.argv[1:]

        build_model = False
        if args[0] == "--build_model" and args[1] == "True":
            build_model = True

        cmd = ["ps -ef | grep .*python.*fundamentalAnalysis/lstm_model.py"]
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        model_pid, err = process.communicate()
        # Logger.log(f"do not try to build another model {model_pid.splitlines()}", log_level=LogLevel.Info)
        if len(model_pid.splitlines()) > 3:
            # Logger.log("build model instance already running, no need to start another.", log_level=LogLevel.Error)
            exit()
        else:
            print("start lstm model build")
            # Logger.log("STARTING lstm model build", LogLevel.Info)
            conf_folder = Path("conf")
            user_config = read_config((conf_folder/"user.yml").resolve(strict=True).as_posix())
            selected_stocks_config = read_config((conf_folder/"selected_stocks.yml").resolve(strict=True).as_posix())
            discord_config = read_config((conf_folder/"discord.yml").resolve(strict=True).as_posix())
            lstm_config = read_config((conf_folder/"lstm.yml").resolve(strict=True).as_posix())
            result_folder = Path("result/lstm").resolve(strict=True).as_posix()

            selected_stocks = selected_stocks_config['to_buy'] + selected_stocks_config['to_sell']
            selected_stocks = [stock + ".NS" for stock in selected_stocks]

            # fetch data till current
            stock_config = {
                'tickers': selected_stocks,
                'interval': lstm_config['yf_interval'],
                'period': lstm_config['yf_period']
            }
            yfinance = YFinanceLiveData(stock_config)
            data = yfinance.get_tickers_historical_data()

            past_data_count = 50
            lstm = LstmPredictor(model_save_folder_path=result_folder, selected_feature='Close',
                                 past_data_point_count=past_data_count, selected_stocks=selected_stocks, debug=True,
                                 debug_count=2)
            if build_model:
                lstm.init_model(selected_stocks_df=data[:-past_data_count*2], train_test_ratio=0.8, epochs=20)
                lstm.build_model()
            else:
                lstm.predict(current_data=data[-past_data_count*2:])

            Logger.log(msg="LSTM done", log_level=LogLevel.Debug)
    except Exception as e:
        print(e)
        exit(e)
    '''
