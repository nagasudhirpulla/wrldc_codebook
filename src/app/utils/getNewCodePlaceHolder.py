import datetime as dt


def getNewCodePlaceHolder() -> str:
    nowTime = dt.datetime.now()
    return "WRLDC/{0}/".format(dt.datetime.strftime(nowTime, "%Y/%m"))
