from ai.orchestrator import Orchestrator
from utility.logger import Logger, LogLevel
from pathlib import Path
from conf import conf_editor
import subprocess
import sys

if __name__ == "__main__":
    cmd = ["ps -ef | grep .*python.*fundamentalAnalysis/ai_main.py"]
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    ai_pid, err = process.communicate()
    Logger.log(f"ai main is running process {ai_pid.splitlines()}", log_level=LogLevel.Info)
    if len(ai_pid.splitlines()) > 3:
        Logger.log("Fundamental analysis ai instance already running, no need to start another.",
                   log_level=LogLevel.Error)
        exit()
    else:
        print("start fundamental ai")
        Logger.log("STARTING AI ANALYSIS", LogLevel.Info)
        configuration = conf_editor.read()

        args = sys.argv
        orchestrator = Orchestrator()

        if len(args) > 1 and args[1] == '--build':
            orchestrator.build()
            Logger.log(msg="closing model build", log_level=LogLevel.Debug)
