import os.path
import pandas as pd


class Node:
    def __init__(self, name: str, weight=1.0):
        self.name = name

        self.connections = {}
        self.connections_frequency = {}

    def add_connections(self, connections_list: list):
        for connection, weight in connections_list:
            if connection not in self.connections:
                self.connections[connection] = 0
                self.connections_frequency[connection] = 0
                
            self.connections[connection] += weight
            self.connections_frequency[connection] += 1
                

    def get_connection(self, name):
        if name in self.connections:
            return self.connections[name]
        return 0
    

    def get_csv(self):
        csv_strings = []

        self.connections = dict(sorted(self.connections.items(), key=lambda item: item[1], reverse=True))

        for connection in self.connections:
            csv_strings.append(f"{self.name}, {connection}, {self.connections[connection]}")

        return "\n".join(csv_strings)


class Magazins:
    def __init__(self, name: str):
        self.name = name
        self.labels = {}
        self.label_frequencies = {}

    def process_label_list(self, label_list: list):
        for label, weight in label_list:
            weight = 1.0 - weight

            if label not in self.label_frequencies:
                self.label_frequencies[label] = 0
                self.labels[label] = Node(label, weight=weight)
            
            self.label_frequencies[label] += 1             
            self.labels[label].add_connections(label_list)

    def dump_csv(self, path: str, item_count=2000):
        if len(self.label_frequencies) > item_count:
            item_count = len(self.label_frequencies)

        label_frequencies = dict(sorted(self.label_frequencies.items(), key=lambda item: item[1], reverse=True)[:item_count])

        frequency = pd.DataFrame(label_frequencies.items(), columns=['label', 'frequency'])
        frequency.to_csv(os.path.join(path, f"frequency_{self.name}.csv"))

        csv_strings = ["Id, Frequency"]
        label_index = []
        for label_label in list(label_frequencies):
            if label_frequencies[label_label] > 1:
                label_index.append(label_label)
                csv_strings.append(f"{label_label}, {label_frequencies[label_label]}")

        matrix = pd.DataFrame(index=label_index, columns=label_index)

        for i in label_index:
            for j in label_index:
                class_i = self.labels[i]
                class_j = self.labels[j]
                total1 = self.label_frequencies[class_i.name]
                total2 = self.label_frequencies[class_j.name]
                if total2 > total1:
                    total1, total2 = total2, total1
                connection = class_i.get_connection(j)
                factor = float(total1) / float(total2)
                raw_weight = connection * factor
                weight = raw_weight / total1
                matrix.at[i, j] = weight
        matrix.to_csv(os.path.join(path, f"matrix_{self.name}.csv"))



magazin_map = {
    "all": Magazins("all")
}


def save_labels(magazin: str, label_list: list):
    if magazin not in magazin_map:
        magazin_map[magazin] = Magazins(magazin)

    magazin_map[magazin].process_label_list(list(label_list))
    magazin_map["all"].process_label_list(list(label_list))


def finished(dump_path="graph_matricies"):
    if not os.path.exists(dump_path):
        raise Exception(f"{dump_path} does not exist")

    for magazin in magazin_map:
        magazin_map[magazin].dump_csv(dump_path)
