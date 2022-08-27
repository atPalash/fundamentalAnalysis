from conf.conf_editor import read
from utility.logger import LogLevel
from utility.aggregator import get_singletons
from multiprocessing.connection import Listener
from array import array

if __name__ == "__main__":
    print("start analysis")
    configuration = read()

    singletons = get_singletons(configuration=configuration)
    logger = singletons['logger']

    # utility = Utility(configuration=configuration)  # initialise Discord listener. messenger
    # logger = utility.singletons['logger']
    # orchestrator = Orchestrator(user_config=configuration['user_config'], indicator_config=configuration['indicator_config'],
    #                             selected_stocks_config=configuration['selected_stocks_config'],
    #                             discord_config=configuration['discord_config'])
    # orchestrator.run()
    logger.log(msg="closing analysis", log_level=LogLevel.Debug)

    address = ('localhost', 6000)     # family is deduced to be 'AF_INET'

    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            print('connection accepted from', listener.last_accepted)

            conn.send([2.25, None, 'junk', float])

            conn.send_bytes(b'hello')

            conn.send_bytes(array('i', [42, 1729]))