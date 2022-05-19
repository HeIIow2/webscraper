import yake
from urllib.parse import urlparse

HEADER_IMPORTANCE_FACTOR = 0.5

MIN_TEXT_LEN = 10
MIN_TEXT_HEADER_RATIO = 2


kw_extractor = yake.KeywordExtractor(lan="de", top=10)


def get_keywords(magazines: list, data: dict):
    keyword_data = {}
    for magazine in magazines:
        current_data = data[magazine]
        if not len(current_data):
            continue
        temp_keywords = []

        used_paths = []

        for article in current_data:
            article_keywords = []
            if not article["success"]:
                continue

            url = article["url"]
            parse_object = urlparse(url)
            if parse_object.path in used_paths:
                continue
            used_paths.append(parse_object.path)
            if parse_object.path in ["/", "/themen", "/epaper", "/newsletter", "/agb", "/datenschutz", "/impressum",
                                     "/archiv", "/gewinnspiele"]:
                continue
            if "user" in parse_object.path:
                continue
            if "autor" in parse_object.path:
                continue

            article_content = article['content']
            if len(article_content['text']) <= 0:
                continue
            text_len = len(article_content['text'])
            header_len = sum([len(elem) for elem in article_content['headers']])
            header_text_ration = text_len/header_len
            if header_text_ration < MIN_TEXT_HEADER_RATIO:
                continue

            if "headers" in article_content:
                article_keywords.extend(kw_extractor.extract_keywords(" ".join(article_content['headers'])))

            article_keywords.extend(kw_extractor.extract_keywords(article_content['text']))
            article_keywords.sort(key=lambda x: x[1])
            temp_keywords.append(article_keywords)

        if len(temp_keywords):
            keyword_data[magazine] = temp_keywords

    return keyword_data
