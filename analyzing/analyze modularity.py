import datetime
import json
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

data = {}

with open("modularity.csv", "r", encoding="utf-8") as modularity_file:
    elem_list = modularity_file.read().strip("\n").split("\n")
    # print(elem_list)

    for elem in elem_list[1:]:
        elems = elem.split(",")

        if int(elems[4]) not in data:
            data[int(elems[4])] = [{
                'name': elems[0],
                'freq': int(elems[3])
            }]

            continue
        data[int(elems[4])].append({
            'name': elems[0],
            'freq': int(elems[3])
        })

keyword_data = []

with open("data_date.csv", "r") as data_file:
    elem_list = data_file.read().strip("\n").split("\n")
    # print(elem_list)

    for elem in elem_list:
        keyword_data.append(json.loads(elem))

x_axis_ = {}


def to_integer(dt_time_elem):
    dt_time = dt_time_elem['date']
    month, day, year = dt_time.split(".")
    return 10000 * int(year) + 100 * int(month) + int(day)


keyword_data.sort(key=to_integer)

for keyword_date in keyword_data:
    month, day, year = keyword_date['date'].split(".")
    keyword_date['date'] = datetime.date(int(year), int(month), int(day)).strftime("%d/%m/%Y")
    # keyword_date['date'] = to_integer(datetime.date(int(year), int(month), int(day)))
    x_axis_[keyword_date['date']] = 0
    temp_keywords = []
    for keyword in keyword_date['keywords']:
        temp_keywords.append(keyword[0])

    keyword_date["keywords"] = temp_keywords

x_axis_ = list(x_axis_.keys())
print("starting")

analyzed = {}

for modularity_class in data:
    sources = ['elle', 'bleib gesund', 'brigitte', 'meine Familie und ich', 'fuer sie', 'vogue', 'jolie', 'levi',
               'cosmopolitan', 'tom tailor', 'primark', 'gap', 'jack and jones', 'superdry', 'only', 'veromoda',
               'mango', 'metal hammer', 'scotch', 'voque', 'newyorker', 'sephora']

    biggest_key = ""
    biggest_key_freq = 0
    for possible_key in data[modularity_class]:
        if possible_key["freq"] > biggest_key_freq:
            biggest_key_freq = possible_key["freq"]
            biggest_key = possible_key["name"]

    if biggest_key_freq < 20:
        continue

    temp_dict = {}
    summarized_days = 7

    for keyword_date in keyword_data:
        found = False
        for possible_key in data[modularity_class]:
            if possible_key['name'] in keyword_date['keywords']:
                found = True
                break

        date_ = keyword_date['date']

        if date_ not in temp_dict:
            temp_dict[date_] = [0] * (len(sources) + 1)

        if not found:
            continue

        temp_frequencies = temp_dict[date_]
        index_ = sources.index(keyword_date["source"])
        temp_frequencies[index_] += 1
        temp_frequencies[-1] += 1

        temp_dict[date_] = temp_frequencies

    y_values = [[] for x in range(len(sources) + 1)]
    dates = []

    for j, key in enumerate(temp_dict):
        if j % summarized_days == 0:
            dates.append(key)
        for i, val in enumerate(temp_dict[key]):
            if j % summarized_days == 0:
                y_values[i].append(val)
            else:
                y_values[i][-1] += val

    for i in range(0, len(y_values[:-1]) - 1):
        for j in range(len(y_values[:-1]) - 1):
            if np.average(y_values[j]) < np.average(y_values[j + 1]):
                y_values[j], y_values[j + 1] = y_values[j + 1], y_values[j]
                sources[j], sources[j + 1] = sources[j + 1], sources[j]

    plt.plot_date(dates, y_values[-1], linestyle='solid', label="all")
    for i, y_value in enumerate(y_values[:-1]):
        # print(y_value)
        if i < 16:
            source = sources[i]
            plt.plot_date(dates, y_value, linestyle='solid', label=source)
        else:
            plt.plot_date(dates, y_value, linestyle='solid')

    date_labels = []

    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.title(biggest_key)
    plt.tight_layout()
    analyzed[modularity_class] = temp_dict

    path = f"analyzed/{biggest_key}/"
    try:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
    except:
        continue

    plt.savefig(f"{path}{biggest_key}.svg")
    plt.show()

    with open(f"{path}{biggest_key}_keywords", "w") as data_file_:
        for possible_key in data[modularity_class]:
            data_file_.write(possible_key["name"] + "\n")


    with open(f"{path}{biggest_key}.json", "w") as data_file_:
        data_file_.write(json.dumps(temp_dict))

    print(biggest_key, biggest_key_freq)

with open("analyzed.json", "w") as analyzed_file:
    analyzed_file.write(json.dumps(analyzed))
