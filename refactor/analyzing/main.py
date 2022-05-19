from datetime import datetime

import read_data

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
    for data in data_iter:
        print(data[0])

        i += 1
        if i > timeout:
            break
