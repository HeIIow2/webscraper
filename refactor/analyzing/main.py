from datetime import datetime

import read_data
import extract_keywords

DATA_PATH = "data"
MAGAZINES = [
    "bleib gesund",
    "cosmopolitan",
    "brigitte",
    "elle",
    "jolie",
]
HEADER_IMPORTANCE_FACTOR = 1.5  # The higher the number, the less important it is
MIN_TEXT_HEADER_RATIO = 2       # cars of the text / chars of the header
KEYWORDS_PER_ARTICLE = 10        # The number of keywords to be extracted from each article


if __name__ == "__main__":
    data_iter = iter(read_data.Data(MAGAZINES, DATA_PATH=DATA_PATH))

    timeout = 5
    i = 0
    for date, data in data_iter:
        print(date)
        keywords = extract_keywords.get_keywords(magazines=MAGAZINES, data=data, keywords_per_article=KEYWORDS_PER_ARTICLE, header_importance_factor=HEADER_IMPORTANCE_FACTOR, min_text_header_ratio=MIN_TEXT_HEADER_RATIO)
        for magazine in keywords:
            print(f"-------------{magazine}--------------")
            for key in keywords[magazine]:
                print("; ".join([element[0] for element in key]))


        i += 1
        if i > timeout:
            break
