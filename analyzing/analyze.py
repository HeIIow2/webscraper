import json
import re

class Node:
    def __init__(self, name: str, weight=1.0):
        self.name = name
        self.frequency = weight

        self.connections = {}

    def add_frequency(self, weight=1.0):
        self.frequency += weight

    def add_connections(self, connections_list: list):
        #connections_list = list(dict.fromkeys(connections_list))
        for connection, weight in connections_list:
            if connection in self.connections:
                self.connections[connection] += weight
            else:
                self.connections[connection] = weight

    def get_csv(self):
        if self.frequency != self.connections[self.name]:
            print(f"FUCK {self.frequency} {self.connections[self.name]}")

        csv_strings = []

        self.connections = dict(sorted(self.connections.items(), key=lambda item: item[1], reverse=True))

        if list(self.connections)[0] != self.name:
            # print(f"fuck {self.name}")
            pass

        for connection in self.connections:
            csv_strings.append(f"{self.name}, {connection}, {self.connections[connection]}")

        return "\n".join(csv_strings)

labels = {}
label_frequencies = {}

def save_labels(label_list: list):
    for label, weight in label_list:
        # for the sake of having a complete frequency list
        if label in label_frequencies:
            label_frequencies[label] += 1
        else:
            label_frequencies[label] = 1

        if label in labels:
            labels[label].add_frequency(weight=weight)
        else:
            labels[label] = Node(label, weight=weight)
        labels[label].add_connections(label_list)

def finished():
    global label_frequencies

    label_frequencies_ = dict(sorted(label_frequencies.items(), key=lambda item: item[1], reverse=True))
    
    label_frequencies = {}
    
    blacklist = []
    with open("blacklist", "r", encoding="utf-8") as blacklist_file:
        for elem in blacklist_file.read().split("\n"):
            blacklist.append(elem.split(",")[0])
            
    print(blacklist)
    
    for key in label_frequencies_:
        new_key = key.replace(",", " ")
        if label_frequencies_[key] > 99 and new_key not in blacklist:
            label_frequencies[new_key] = label_frequencies_[key]

    csv_strings = []
    for label in labels:
        csv_strings.append(labels[label].get_csv())

    with open("connections.csv", "w", encoding="utf-8") as connections_file:
        connections_file.write("\n".join(csv_strings))

    graph_strings = []
    csv_strings = ["Id, Frequency"]
    label_index = []
    for label_label in list(label_frequencies):
        if label_frequencies[label_label] > 1:
            label_index.append(label_label)
            csv_strings.append(f"{label_label}, {label_frequencies[label_label]}")

    with open("frequency.csv", "w", encoding="utf-8") as connections_file:
        connections_file.write("\n".join(csv_strings))

    graph_strings.append(f",{', '.join(label_index)}")
    for label in label_index:
        next_graph_string = label
        label_class = labels[label]

        for possible_label_connection in label_index:
            if possible_label_connection in label_class.connections:
                possible_label_class = labels[possible_label_connection]

                total1 = label_class.frequency
                total2 = possible_label_class.frequency
                if total2 > total1:
                    total1, total2 = total2, total1
                connection = label_class.connections[possible_label_connection]
                factor = float(total1) / float(total2)
                raw_weight = connection * factor
                weight = raw_weight / total1

                # print(f"total1 {total1};\ntotal2 {total2};\nfactor {factor};\nconnection {connection};\nraw_weight {raw_weight};\nweight {weight};\n")

                next_graph_string += f", {weight}"
            else:
                next_graph_string += ", 0"

        graph_strings.append(next_graph_string)

    # for graph_string in graph_strings:
    #     print(graph_string)

    with open("graph.csv", "w", encoding="utf-8") as graph_file:
        graph_file.write("\n".join(graph_strings))
