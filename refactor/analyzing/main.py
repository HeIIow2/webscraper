from datetime import datetime

import read_data
import extract_keywords

MAGAZINES = [
    "bleib gesund",
    "cosmopolitan",
    "brigitte",
    "elle",
    "jolie",
]


if __name__ == "__main__":
    data_iter = iter(read_data.Data(MAGAZINES))

    timeout = 5
    i = 0
    for date, data in data_iter:
        print(date)
        print(extract_keywords.get_keywords(magazines=MAGAZINES, data=data))


        i += 1
        if i > timeout:
            break
