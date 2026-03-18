import configparser

# import os
from dataclasses import dataclass
from pathlib import Path

# cwd = os.getcwd()
cwd = Path.cwd()

# TODO: add checks for the config.ini


@dataclass
class Config:
    debug: bool = False
    loglevel: str = "info"
    listen_port: int = 8080
    host_addr: str = "127.0.0.1"
    delivery_server: str = "127.0.0.1"
    cookie_secret: str = "EIT2025ZYU"


def readConfig() -> Config:
    config = configparser.ConfigParser()
    config.read(f"{cwd}/app/config.ini")

    debug = config.getboolean("General", "debug")
    loglevel = config.get("General", "log_level")
    listenport = config.getint("General", "listen_port")
    hostaddr = config.get("General", "host_addr")
    ads = config.get("General", "delivery_server")
    cookie = config.get("General", "cookie_secret")

    return Config(debug, loglevel, listenport, hostaddr, ads, cookie)


def updateConfig(cfg: Config):
    config = configparser.ConfigParser()

    config["General"] = {
        "debug": "True",
        "log_level": "info",
        "listen_port": str(cfg.listen_port),
        "host_addr": cfg.host_addr,
        "delivery_server": cfg.delivery_server,
        "cookie_secret": "EIT2025ZYU",
    }

    with open(f"{cwd}/app/config.ini", "w") as configfile:
        config.write(configfile)


def createConfig():
    config = configparser.ConfigParser()

    config["General"] = {
        "debug": True,
        "log_level": "info",
        "listen_port": 8080,
        "host_addr": "127.0.0.1",
        "delivery_server": "127.0.0.1",
        "cookie_secret": "EIT2025ZYU",
    }
    with open(f"{cwd}/config.ini", "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    # create the default config file if it does not exist
    # if not os.path.isfile(f"{cwd}/config.ini"):
    createConfig()
