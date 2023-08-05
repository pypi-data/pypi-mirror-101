#!python3
"""crude.dev client."""

from typing import List

import random


import typer

from .spark import sparkline


def _test():
    pass


import msgpack

import httpx

api_server_address = "https://api.crude.dev"


def get_values(project: str, topic: str) -> List:
    # r = requests.get(f"{api_server_address}/{project}/{topic}")
    # print(f"r.headers {r.headers}")
    # if not r.ok:
    #     return None

    data = dict(values=[random.random() for r in range(2 ** 10)])
    return data


def plot_topic(project: str, topic: str):
    data = get_values(project, topic)
    print(f"{project}/{topic}:")
    print(sparkline(data["values"]))

# https://pypi.org/project/asciichartpy/


def plot_tree():
    # https://github.com/willmcgugan/rich/blob/master/examples/tree.py
    pass


def main():
    print("crude [help|post|login|auth|account|stats|upgrade]")

    plot_topic("proj", "visits")


if __name__ == "__main__":
    main()
