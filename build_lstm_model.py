import sys
from lib2to3.pygram import pattern_symbols

from ai.lstm.lstm_predictor import LstmPredictor
from dataFetch.yfinance_live_data import YFinanceLiveData
from utility.reader import read_config
from utility.logger import Logger, LogLevel
from pathlib import Path
import subprocess
import platform

if __name__ == "__main__":
    try:
        args = sys.argv[1:]

        build_model = False
        # if args[0] == "--build_model" and args[1] == "True":
        #     build_model = True

        # cmd = ["ps -ef | grep .*python.*fundamentalAnalysis/build_lstm_model.py"]
        # process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # model_pid, err = process.communicate()
        # Logger.log(f"do not try to build another model {model_pid.splitlines()}", log_level=LogLevel.Info)
        # if len(model_pid.splitlines()) > 3:
        #     Logger.log("build model instance already running, no need to start another.", log_level=LogLevel.Error)
        #     exit()
        # else:
        print("start lstm model build")
        Logger.log("STARTING lstm model build", LogLevel.Info)
        conf_folder = Path("conf")
        user_config = read_config(
            (conf_folder/"user.yml").resolve(strict=True).as_posix())
        selected_stocks_config = read_config(
            (conf_folder/"selected_stocks.yml").resolve(strict=True).as_posix())
        discord_config = read_config(
            (conf_folder/"discord.yml").resolve(strict=True).as_posix())
        lstm_config = read_config(
            (conf_folder/"lstm.yml").resolve(strict=True).as_posix())
        result_folder = Path("result/lstm").resolve(strict=True).as_posix()

        selected_stocks = selected_stocks_config['to_buy'] + \
            selected_stocks_config['to_sell']
        selected_stocks = [stock + ".NS" for stock in selected_stocks]

        # fetch data till current
        stock_config = {
            'tickers': selected_stocks,
            'interval': user_config['yf_interval'],
            'period': user_config['yf_period']
        }
        yfinance = YFinanceLiveData(stock_config)
        data = yfinance.get_tickers_historical_data()
        past_data_count = 50
        lstm = LstmPredictor(model_save_folder_path=result_folder, selected_feature='Close',
                                past_data_point_count=past_data_count, selected_stocks=selected_stocks)
        if build_model:
            lstm.init_model(selected_stocks_df=data,
                                train_test_ratio=0.8, epochs=50)
            lstm.build_model(debug=True)
        else:
            pred = lstm.predict(current_data=data[-past_data_count*2:])
            print(f"prediction: {pred}")
            
        Logger.log(msg="LSTM done", log_level=LogLevel.Debug)
    except Exception as e:
        print(e)
        exit(e)