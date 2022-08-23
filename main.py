from conf.conf_editor import read
from orchestrator.orchestrator import Orchestrator
from utility.logger import LogLevel
from utility.aggregator import singletons

if __name__ == "__main__":
    print("start analysis")
    logger = singletons['logger']
    logger.log("STARTING ANALYSIS", LogLevel.Info)
    configuration = read()

    orchestrator = Orchestrator(user_config=configuration['user_config'], indicator_config=configuration['indicator_config'],
                                selected_stocks_config=configuration['selected_stocks_config'],
                                discord_config=configuration['discord_config'])
    orchestrator.run()
    logger.log(msg="closing analysis", log_level=LogLevel.Debug)
