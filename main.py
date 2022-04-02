from orchestrator.orchestrator import Orchestrator
from utility.logger import Logger, LogLevel

if __name__ == "__main__":
    Logger.log("STARTING ANALYSIS", LogLevel.Info)
    user_config = "conf/user.yml"
    indicator_config = "conf/indicator.yml"
    selected_stocks_config = "conf/selected_stocks.yml"

    orchestrator = Orchestrator(user_config=user_config, indicator_config=indicator_config,
                                selected_stocks_config=selected_stocks_config)
    orchestrator.run()