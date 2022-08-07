from orchestrator.orchestrator import Orchestrator
from utility.logger import Logger, LogLevel
from pathlib import Path
import subprocess

if __name__ == "__main__":
    # cmd = ["ps -ef | grep .*python.*fundamentalAnalysis/main.py"]
    # process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
    # stderr=subprocess.PIPE)
    # fundamental_pid, err = process.communicate()
    # Logger.log(f"fundamental analysis running process {fundamental_pid.splitlines()}", log_level=LogLevel.Info)
    # if len(fundamental_pid.splitlines()) > 3:
    #     Logger.log("Fundamental analysis instance already running, no need to start another.", log_level=LogLevel.Error)
    #     exit()
    # else:   
        print("start analysis")
        Logger.log("STARTING ANALYSIS", LogLevel.Info)
        conf_folder = Path("conf")
        user_config = conf_folder/"user.yml"
        user_config = user_config.resolve(strict=True).as_posix()
        indicator_config = conf_folder/"indicator.yml"
        indicator_config = indicator_config.resolve(strict=True).as_posix()
        selected_stocks_config = conf_folder/"selected_stocks.yml"
        selected_stocks_config = selected_stocks_config.resolve(strict=True).as_posix()
        discord_config = conf_folder/"discord.yml"
        discord_config = discord_config.resolve(strict=True).as_posix()

        orchestrator = Orchestrator(user_config=user_config, indicator_config=indicator_config,
                                    selected_stocks_config=selected_stocks_config, discord_config=discord_config)
        orchestrator.run()
        Logger.log(msg="closing analysis", log_level=LogLevel.Debug)


    