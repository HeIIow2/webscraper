import json
import os.path
from datetime import datetime

import read_data
import extract_keywords
import compute_edges

DATA_PATH = "data"
ANALYZED_PATH = "analyzed"
GRAPH_PATH = "graph_matricies"

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

SAVE_FREQUENCY = 10
RESET_KEYWORDS = True
DATE_FORMAT = "%d.%m.%Y"


if __name__ == "__main__":
    if RESET_KEYWORDS:
        with open(os.path.join(ANALYZED_PATH, "keywords.json"), "w", encoding="utf-8") as f:
            json.dump([], f)

    data_iter = iter(read_data.Data(MAGAZINES, DATA_PATH=DATA_PATH))
    keyword_buffer = []

    timeout = -1
    for i, (date, data) in enumerate(data_iter):
        print(f"-------------{date}--------------")
        print("extracting keywords")
        keywords = extract_keywords.get_keywords(magazines=MAGAZINES, data=data, keywords_per_article=KEYWORDS_PER_ARTICLE, header_importance_factor=HEADER_IMPORTANCE_FACTOR, min_text_header_ratio=MIN_TEXT_HEADER_RATIO)
        for magazine in keywords:
            print(magazine)
            for key in keywords[magazine]:
                #print("; ".join([element[0] for element in key]))
                compute_edges.save_labels(magazine, key)
            keyword_buffer.append({"date": datetime.strftime(date, DATE_FORMAT), "magazin": magazine, "keywords": keywords[magazine]})

        if not i % SAVE_FREQUENCY:
            print("saving keywords")
            with open(os.path.join(ANALYZED_PATH, "keywords.json"), "r", encoding="utf-8") as f:
                current_keywords = json.load(f)
            current_keywords.extend(keyword_buffer)
            with open(os.path.join(ANALYZED_PATH, "keywords.json"), "w", encoding="utf-8") as f:
                json.dump(current_keywords, f)

        if i > timeout != -1:
            break

    print("saving keywords")
    with open(os.path.join(ANALYZED_PATH, "keywords.json"), "r", encoding="utf-8") as f:
        current_keywords = json.load(f)
    current_keywords.extend(keyword_buffer)
    with open(os.path.join(ANALYZED_PATH, "keywords.json"), "w", encoding="utf-8") as f:
        json.dump(current_keywords, f)

    compute_edges.finished(GRAPH_PATH)
