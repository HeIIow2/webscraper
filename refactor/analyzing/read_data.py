import os
import os.path
from datetime import datetime
import json

DATA_PATH = "data"

if not os.path.exists(DATA_PATH):
    raise Exception(f"cant find data under {DATA_PATH}")


class Data:
    def __init__(self, magazines: list):
        self.magazines = magazines
        self.dates = []
        for date_str in os.listdir(DATA_PATH):
            utc_time = datetime.strptime(date_str, "%m.%d.%Y")
            self.dates.append(utc_time)

        self.cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.cursor >= len(self.dates):
            raise StopIteration

        data = {}
        current_path = os.path.join(DATA_PATH, self.dates[self.cursor].strftime("%m.%d.%Y"))
        for magazine in self.magazines:
            data[magazine] = []
            path = os.path.join(current_path, magazine+".json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data[magazine] = json.load(f)

        self.cursor += 1
        # return here
        return self.dates[self.cursor-1], data
