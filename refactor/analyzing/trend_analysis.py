import pandas as pd
import datetime

class Keywords:
    def __init__(self, modularity_path: str, magazine: str):
        self.magazine = magazine
        self.modularity = pd.read_csv(modularity_path)
        unwanted_columns = [
            "Id",
            "timeset"
        ]
        for unwanted_column in unwanted_columns:
            self.modularity.pop(unwanted_column)
        self.modularity.columns = ["Label", "modularity_class"]
        self.modularity = self.modularity.sort_values(by='modularity_class', ascending=True)
        print(self.modularity)

        # get the highest modularity class
        highest_modularity_class = self.modularity.iloc[-1]["modularity_class"]

        # is a list of all the dates
        # represents the x axis
        self.date_list = []

        self.keyword_frequency = {}
        for i in range(0, highest_modularity_class + 1):
            self.keyword_frequency[i] = []

        self.articles_loss = 0
        self.good_articles = 0

    def get_modularity_of(self, keyword: str):
        try:
            return self.modularity.loc[self.modularity['Label'] == keyword]['modularity_class'].values[0]
        except IndexError:
            return -1

    def add_data(self, date: datetime.datetime, articles: list):
        cursor = len(self.date_list)
        if date in self.date_list:
            cursor = self.date_list.index(date)
        else:
            # wenn das datum noch nicht existiert, dann hänge es an
            # und hänge für das jeweilige datum eine frequency an die
            # keyword_frequency an
            self.date_list.append(date)
            for key in self.keyword_frequency:
                self.keyword_frequency[key].append(0)

        for article in articles:
            already_added = []
            for keyword, keyword_importance in article:
                modularity = self.get_modularity_of(keyword)
                if modularity == -1:
                    continue
                # dass es nur ein keyword der gleichen community pro artikel zählen kann.
                if modularity in already_added:
                    continue
                already_added.append(modularity)

                # fügt 1 hinzu da es die anzahl an artikeln über ein bestimmtes Thema
                # zählt.
                self.keyword_frequency[modularity][cursor] += 1

            if len(already_added) == 0:
                self.articles_loss += 1
            else:
                self.good_articles += 1

    def retrieve_data(self):
        print(f"magazine: {self.magazine}; Articles loss: {self.articles_loss} from {self.good_articles} dates")
        return self.date_list, self.keyword_frequency

