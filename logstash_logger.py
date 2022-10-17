import logging
import logstash

class Logging:
    def __init__(self, logger_name: str, log_stash_host: str, log_stash_udp_port: int):
        self.logger_name = logger_name
        self.log_stash_host = log_stash_host
        self.log_stash_udp_port = log_stash_udp_port
        
    def get(self):
        logging.basicConfig(
            filename="logfile.log",
            filemode="a",
            format="%(asctime)s,%(msecs)d,%(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d_%H:%M:%S",
            level=logging.INFO,
        )
        self.stderrLogger = logging.StreamHandler()
        logging.getLogger().addHandler(self.stderrLogger)
        self.logger = logging.getLogger(self.logger_name)
        self.logger.addHandler(logstash.LogstashHandler(self.log_stash_host, self.log_stash_udp_port, version=1))
        return self.logger

if __name__ == "__main__":
    log = Logging("sample", "localhost", 5959)
    logger = log.get()
