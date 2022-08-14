import json
import numpy as np
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

plt.gcf().subplots_adjust(bottom=0.25, right=0.75)
figure(figsize=(16, 5))

LABEL_COUNT = 10
CONTEXT_NUMBER = 3

BLACKLIST = [
    "metal hammer",
    "mango",
    "only",
    "newyorker",
    "jack and jones",
    "scotch",
    "primark",
    "levi",
    "veromoda",
    "superdry",
    "tom tailor",
    "gap"
]


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

        if self.current_month > 2 and self.current_year >= 2022:
            raise StopIteration

        return self.current_day, self.current_month, self.current_year


dates = DATES()


class Element:
    def __init__(self, name: str):
        self.name = name
        self.significance = 0.0

    def __lt__(self, other):
        return self.significance < other.significance


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

    def add_element(self, element: str):
        self.elements.append(Element(element))

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

    def add_entry(self, significance: float, date: tuple, name: str):
        self.total_significance += significance
        self.weight += 1

        if date not in self.importance_time:
            self.importance_time[date] = 0

        for i, element in enumerate(self.elements):
            if element.name == name:
                self.elements[i].significance += significance
                break

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

    def add_module(self, modularity_class: int, element: str):
        if modularity_class not in self.modules:
            self.modules[modularity_class] = Module(modularity_class)

        self.modules[modularity_class].add_element(element)

    def add_entry(self, name: str, significance: int, magazine: str, date: tuple):

        for i in self.modules:
            module = self.modules[i]
            if module.belongs_to(name):
                break
        else:
            return

        self.modules[i].add_entry(significance, date, name)

    def get_modules(self):
        return_list = []
        for i, module in sorted(self.modules.items()):
            if module.total_significance > 0.2:
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

    return f"{date[0]}. {months[date[1] - 1]} {date[2]}"


modules = Modules()

with open("modularity.csv", "r", encoding="utf-8") as modularity_file:
    modules_list = modularity_file.read().strip("\n").split("\n")

    for raw_module in modules_list[1:]:
        module = raw_module.split(",")
        name = module[0].lower()
        modularity_class = int(module[4])

        modules.add_module(modularity_class, name)

keyword_data = []

print("read modularity")

with open("data_date.csv", "r") as data_file:
    elem_list = data_file.read().strip("\n").split("\n")
    # print(elem_list)

    for elem in elem_list:
        to_add = json.loads(elem)
        if to_add["source"] in BLACKLIST:
            continue
        for i, keyword in enumerate(to_add["keywords"]):
            to_add["keywords"][i][0] = keyword[0].lower()
        keyword_data.append(to_add)

print("read data")

article_frequencies = {

}

article_significances = {

}

for article in keyword_data:
    magazine = article["source"]
    date = date_to_tuple(article["date"])
    keywords = article["keywords"]

    if date not in article_frequencies:
        article_frequencies[date] = 0
        article_significances[date] = 0
    article_frequencies[date] += 1

    for name, significance in keywords:
        article_significances[date] += significance
        modules.add_entry(name, significance, magazine, date)

ADDET_DAYS = 7

print("created instances of classes")

topics = modules.get_modules()

graph_modules = []
y_values_list = []
x_labels = []

for module in topics:
    y_values_list.append([])
    graph_modules.append(module)
    print(module.get_context())

current_index = 0

prev_month = -1
latest_date = None
for date in dates:
    day, month, year = date

    if not (day - 1) % 7 or prev_month != month:
        if latest_date is not None:
            y_values_list[i][-1] = y_values_list[i][-1] / article_frequencies[latest_date]
        prev_month = month
        current_index += 1

        x_labels.append(tuple_to_str(date))
        for i in range(len(y_values_list)):
            y_values_list[i].append(0)

    for i, module in enumerate(topics):
        if date in article_frequencies:
            y_values_list[i][-1] += module.get_significance(date)
            latest_date = date
            # y_values[i][-1] += module.get_significance(date)

print("summorized dates")


def create_graph(x_axis: list, y_axis_list: list, module_instances: list):
    title = "Trend Analysis"
    if len(module_instances) > 1:
        plt.title(title)
        for i, y_axis in enumerate(y_axis_list):
            if i < LABEL_COUNT:
                plt.plot(x_axis, y_axis, label=", ".join(module_instances[i].get_context()[0:CONTEXT_NUMBER]))
                continue
            plt.plot(x_axis, y_axis)
        plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    else:
        plt.title(", ".join(module_instances[0].get_context()[0:CONTEXT_NUMBER]))
        plt.plot(x_axis, y_axis_list[0])
        title = module_instances[0].get_context()[0]

        with open("graphs/kontext.txt", "a", encoding="utf-8") as kontext_file:
            kontext_file.write(", ".join(module_instances[0].get_context()) + "\n")

    plt.xticks(rotation=90)
    plt.tight_layout()
    title = title.replace(' ', '_').replace('"', '')
    plt.savefig(f"graphs/{title}.svg")
    plt.show()


with open("graphs/kontext.txt", "w") as kontext_file:
    pass

create_graph(x_labels, y_values_list, graph_modules)

for j in range(len(y_values_list)):
    try:
        create_graph(x_labels, [y_values_list[j]], [graph_modules[j]])
    except Exception as e:
        print(e)

"""
Exportiere die Liste mit ; als Trennzeichen
und die float values das komma mit ,
"""

def export_list_to_csv_row(list: list, description: str, delimiter: str = ";", decimal_separator: str = ","):
    description = description.replace('"', '').replace(',', '').replace(';', '')
    string_list = [description]
    for elem in list:
        string_list.append(str(elem).replace(".", decimal_separator))
    return delimiter.join(string_list) + "\n"

german_csv = export_list_to_csv_row(x_labels, "Datum")
english_csv = export_list_to_csv_row(x_labels, "Date", delimiter=",", decimal_separator=".")

for i, y_list in enumerate(y_values_list):
    german_csv += export_list_to_csv_row(y_list, graph_modules[i].get_context()[0])
    english_csv += export_list_to_csv_row(y_list, graph_modules[i].get_context()[0], delimiter=",", decimal_separator=".")

with open("german.csv", "w", encoding="utf-8") as german_file:
    german_file.write(german_csv)

with open("english.csv", "w", encoding="utf-8") as english_file:
    english_file.write(english_csv)
