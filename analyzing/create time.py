import json
import numpy as np
import matplotlib.pyplot as plt


class DATES:
    def __init__(self):
        self.month_lenths = [
            31,
            28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31
        ]

        self.current_day = 23
        self.current_month = 10
        self.current_year = 2021

    def __iter__(self):
        return self

    def __next__(self):
        self.current_day += 1
        if self.current_day > self.month_lenths[self.current_month - 1]:
            self.current_day = 1
            self.current_month += 1
            if self.current_month > 12:
                self.current_month = 1
                self.current_year += 1

        if self.current_month > 3 and self.current_year >= 2022:
            raise StopIteration

        return self.current_day, self.current_month, self.current_year


dates = DATES()


class Element:
    def __init__(self, name: str, frequency: int):
        self.name = name
        self.frequency = frequency

    def __lt__(self, other):
        return self.frequency < other.frequency


class Module:
    def __init__(self, id: int):
        self.id = id
        self.elements = []
        self.total_significance = 0.0

        self.importance_time = {

        }
        self.weight = 0

    def __lt__(self, other):
        return self.total_significance < other.total_significance

    def add_element(self, element: str, frequency: int):
        self.elements.append(Element(element, frequency))

    def get_frequency(self):
        frequencies = []
        for elem in self.elements:
            frequencies.append(elem.frequency)

        return np.average(frequencies)

    def belongs_to(self, name):
        for element in self.elements:
            if name == element.name:
                return True

        return False

    def add_entry(self, significance: float, date: tuple, magazine: str):
        self.total_significance += significance
        self.weight += 1

        if date not in self.importance_time:
            self.importance_time[date] = 0

        self.importance_time[date] = significance

    def get_significance(self, date: tuple):
        if date not in self.importance_time:
            return 0.0

        return self.importance_time[date]

    def get_context(self):
        sorted_list = []
        for element in sorted(self.elements):
            sorted_list.append(element.name)
        return sorted_list


class Modules:
    def __init__(self):
        self.modules = {

        }

    def add_module(self, modularity_class: int, frequency: int, element: str):
        if modularity_class not in self.modules:
            self.modules[modularity_class] = Module(modularity_class)

        self.modules[modularity_class].add_element(element, frequency)

    def add_entry(self, name: str, significance: int, magazine: str, date: tuple):
        if magazine == "metal hammer":
            return

        for i in self.modules:
            module = self.modules[i]
            if module.belongs_to(name):
                break

        self.modules[i].add_entry(significance, date, magazine)

    def get_modules(self):
        return_list = []
        for i, module in list(sorted(list(self.modules.items()))):
            return_list.append(module)
        return return_list


def date_to_tuple(date):
    month, day, year = date.split(".")
    return int(day), int(month), int(year)

def tuple_to_str(date: tuple):
    months = [
        "Januar",
        "Februar",
        "Maerz",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "December"
    ]

    return f"{date[0]}. {months[date[1]-1]} {date[2]}"


modules = Modules()

with open("modularity.csv", "r", encoding="utf-8") as modularity_file:
    modules_list = modularity_file.read().strip("\n").split("\n")

    for raw_module in modules_list[1:]:
        module = raw_module.split(",")
        name = module[0]
        frequency = int(module[3])
        modularity_class = int(module[4])

        modules.add_module(modularity_class, frequency, name)

keyword_data = []

print("read modularity")

with open("data_date.csv", "r") as data_file:
    elem_list = data_file.read().strip("\n").split("\n")
    # print(elem_list)

    for elem in elem_list:
        keyword_data.append(json.loads(elem))

print("read data")

article_frequencies = {

}

for article in keyword_data:
    magazine = article["source"]
    date = date_to_tuple(article["date"])
    keywords = article["keywords"]

    if date not in article_frequencies:
        article_frequencies[date] = 0
    article_frequencies[date] += 1

    for name, significance in keywords:
        modules.add_entry(name, significance, magazine, date)

ADDET_DAYS = 7

print("created instances of classes")

y_values = []
x_values = []
x_labels = []

topics = modules.get_modules()
for module in topics:
    y_values.append([])
    print(module.get_context())

current_index = 0

prev_month = -1
for date in dates:
    day, month, year = date

    if not (day-1) % 7 or prev_month != month:
        prev_month = month
        current_index += 1

        x_labels.append(tuple_to_str(date))
        x_values.append(current_index)
        for i in range(len(y_values)):
            y_values[i].append(0)

    for i, module in enumerate(topics):
        if date in article_frequencies:
            y_values[i][-1] += module.get_significance(date) / article_frequencies[date]
            # y_values[i][-1] += module.get_significance(date)

print("summorized dates")

for y_value in y_values:
    print(x_labels)
    print(y_value)
    plt.plot(x_labels, y_value)

plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
plt.xticks(rotation=45)
plt.title("Data analysis")
plt.tight_layout()

plt.show()
