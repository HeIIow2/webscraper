import json
import os.path
from datetime import datetime

import read_data
import extract_keywords
import compute_edges

import label_community
import trend_analysis
import draw_diagram

RUN_DATA_PREPARATION_FOR_CLUSTERING = False
ANALYZE_TIME = False
DRAW_DIAGRAM = True

DATA_PATH = "data"
ANALYZED_PATH = "analyzed"
GRAPH_PATH = "graph_matricies"
FREQUENCY_FILE = "{magazine}_modularity.csv"
LABEL_FILE = "{magazine}_label.json"
ANALYZED_TIMES_FILE = "{magazine}_analyzed_time.json"
DIAGRAM_FILE = "{magazine}_trend.svg"
MODULARITY_FILE = "{magazine}_modularity.csv"

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
RESET_KEYWORDS = False
DATE_FORMAT = "%d.%m.%Y"

# The number of days, which are summed up per measurement
SUMMARIZED_DAYS = 7
NUMBER_OF_COMMUNITIES = 5


OVERIDE_LABEL_DESCRIPTION = False
KEYWORDS_IN_DESCRIPTION = 1


if __name__ == "__main__":
    if RUN_DATA_PREPARATION_FOR_CLUSTERING:
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
                keyword_buffer.append({"date": datetime.strftime(date, DATE_FORMAT), "magazine": magazine, "keywords": keywords[magazine]})

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
        exit(0)

    # trend analysis
    if ANALYZE_TIME:
        print("starting trend analysis")
        with open(os.path.join(ANALYZED_PATH, "keywords.json"), "r", encoding="utf-8") as f:
            keywords = json.load(f)

        # hier werden alle instanzen der Klasse Keyword (trend_analysis.py) gespeichert, die dem magazin zugeordnet werden
        processing_map = {}

        for magazine in MAGAZINES:
            path = os.path.join(ANALYZED_PATH, f"{magazine}_modularity.csv")
            if not os.path.exists(path):
                continue
            processing_map[magazine] = trend_analysis.Keywords(path, magazine)

        for entry in keywords:
            magazine = entry["magazine"]
            if magazine not in processing_map:
                continue
            date = datetime.strptime(entry["date"], DATE_FORMAT)
            keywords = entry["keywords"]

            according_class = processing_map[magazine]
            according_class.add_data(date, keywords)

        for magazine in processing_map:
            dates, data = processing_map[magazine].retrieve_data(os.path.join(ANALYZED_PATH, f"{magazine}_analyzed_time.json"), DATE_FORMAT)
            with open(os.path.join(ANALYZED_PATH, ANALYZED_TIMES_FILE.format(magazine=magazine)), "r") as f:
                dates, data = json.load(f)


    if DRAW_DIAGRAM:     
        for magazine in MAGAZINES:
            analyzed_times_path = os.path.join(ANALYZED_PATH, ANALYZED_TIMES_FILE.format(magazine=magazine))
            if not os.path.exists(analyzed_times_path):
                continue
                
            with open(analyzed_times_path, "r") as f:
                dates, data = json.load(f)
                
            magazine_labels = label_community.Label(magazine, GRAPH_PATH=GRAPH_PATH, ANALYZED_PATH=ANALYZED_PATH, modularity_file=MODULARITY_FILE, label_file=LABEL_FILE, override_description=OVERIDE_LABEL_DESCRIPTION, keywords_in_description=KEYWORDS_IN_DESCRIPTION)
                
            draw_diagram.draw_diagram(magazine_labels, magazine, dates, data, os.path.join(ANALYZED_PATH, DIAGRAM_FILE.format(magazine=magazine)),
                                      added_days=SUMMARIZED_DAYS, number_of_communities=NUMBER_OF_COMMUNITIES)