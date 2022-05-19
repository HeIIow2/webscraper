import yake
from urllib.parse import urlparse

kw_extractor = yake.KeywordExtractor(lan="de", top=10)


def get_keywords(magazines: list, data: dict, keywords_per_article=10, header_importance_factor=2, min_text_header_ratio=2) -> dict:
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
            if len(article_content['headers']) <= 0:
                header_len = 1
            header_text_ration = text_len/header_len
            if header_text_ration < min_text_header_ratio:
                continue

            if "headers" in article_content:
                for keyword in kw_extractor.extract_keywords(" ".join(article_content['headers'])):
                    article_keywords.append((keyword[0], keyword[1] * header_importance_factor))

            article_keywords.extend(kw_extractor.extract_keywords(article_content['text']))
            article_keywords.sort(key=lambda x: x[1])
            temp_keywords.append(article_keywords[:keywords_per_article])

        if len(temp_keywords):
            keyword_data[magazine] = temp_keywords

    return keyword_data
