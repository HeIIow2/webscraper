import yake
from urllib.parse import urlparse

HEADER_IMPORTANCE_FACTOR = 3
header_kw_extractor = yake.KeywordExtractor(lan="de", top=1, n=2)
body_kw_extractor = yake.KeywordExtractor(lan="de", top=10)

def get_keywords(magazines: list, data: dict):
    keyword_data = {}
    for magazine in magazines:
        current_data = data[magazine]
        if not len(current_data):
            continue
        temp_keywords = []

        for article in current_data:
            if not article["success"]:
                continue

            url = article["url"]
            parse_object = urlparse(url)
            if parse_object.path in ["/", "/themen", "/epaper", "/newsletter", "/agb", "/datenschutz", "/impressum"]:
                continue
            if "user" in parse_object.path:
                continue
            if "autor" in parse_object.path:
                continue

            article_keywords = []

            article_content = article['content']
            if "headers" in article_content:
                for header in article_content['headers']:
                    for keyword in header_kw_extractor.extract_keywords(header):
                        article_keywords.append((keyword[0]*HEADER_IMPORTANCE_FACTOR, keyword[1]))

            temp_keywords.extend(article_keywords)


        if len(temp_keywords):
            keyword_data[magazine] = temp_keywords

    return keyword_data
