import sys
import os


def get_datapath(path: str) -> str:
    pre = "."

    if getattr(sys, "frozen", False):
        pre = sys._MEIPASS  # type: ignore

    return os.path.join(pre, path)


def get_appdata(path: str) -> str:
    pre = "."

    if getattr(sys, "frozen", False):
        pre = os.getenv("APPDATA")

    pre = os.path.join(pre, "gnu_abp_app")  # type: ignore

    if not os.path.exists(pre):  # type: ignore
        os.makedirs(pre)  # type: ignore

    return os.path.join(pre, path)  # type: ignore
