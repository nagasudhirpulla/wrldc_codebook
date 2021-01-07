import json


def getAppConfigFromJson(fName) -> dict:
    with open(fName) as f:
        data = json.load(f)
        return data


class AppConfig:
    __instance: dict = {}

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AppConfig.__instance == None:
            raise Exception("app config is not yet initialized")
        return AppConfig.__instance

    @staticmethod
    def initAppConfig(fName: str):
        # formatting for log stash
        AppConfig.__instance = getAppConfigFromJson(fName)


def initAppConfig(fName: str = "config.json") -> dict:
    AppConfig.initAppConfig(fName)
    return AppConfig.getInstance()


def getConfig() -> dict:
    return AppConfig.getInstance()
