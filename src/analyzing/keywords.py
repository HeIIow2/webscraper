import yake
import os
import json

DATA_PATH = r"D:\web scraping project\webscraper\data"

article_id = 0

def get_keywords(text: str, keyword_count=20):
    kw_extractor = yake.KeywordExtractor()
    language = "de"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=keyword_count, features=None)
    keywords = list(custom_kw_extractor.extract_keywords(text))
    return keywords


def get_data(path_: str, name: str):
    global article_id
    data = []

    url_blacklist = [
        "https://www.bleibgesund.de/datenschutz/",
        "https://www.bleibgesund.de/impressum/",
        "https://www.bleibgesund.de/mediadaten/"
    ]
    header_weight = 10
    text_weight = 1

    print(name)

    with open(path_, "r", encoding="utf-8") as json_file:
        json_ = json.loads(json_file.read())

    for element in json_:
        if element['url'] in url_blacklist:
            continue

        keywords = []

        content = element['content']
        if "headers" in content:
            header_keywords = get_keywords(" ".join(content['headers']), keyword_count=1)
            if len(header_keywords) > 0:
                for i, header_keyword in enumerate(header_keywords):
                    header_keywords[i] = list(header_keywords[i])
                    header_keywords[i][1] = header_keyword[1] * header_weight

            keywords.extend(header_keywords)

        if "text" in content:
            text_keywords = get_keywords(content['text'], keyword_count=10)
            if len(text_keywords) > 0:
                for i, text_keyword in enumerate(text_keywords):
                    text_keywords[i] = list(text_keywords[i])
                    text_keywords[i][1] = text_keyword[1] * text_weight

            keywords.extend(text_keywords)

        def sort(sub_li):
            return list(sorted(sub_li, key=lambda x: x[1], reverse=True))

        keywords = sort(keywords)

        with open("data.csv", "a") as data_file:
            data_file.write(json.dumps({'source': name, 'keywords': keywords}) + "\n")


print(len(os.listdir(DATA_PATH)))

for j, date_dir in enumerate(os.listdir(DATA_PATH)):
    date_path = os.path.join(DATA_PATH, date_dir)
    print(f"##################################     {j}")

    for magazine_name in os.listdir(date_path):
        magazine_path = os.path.join(date_path, magazine_name)

        get_data(magazine_path, magazine_name[:-5])
