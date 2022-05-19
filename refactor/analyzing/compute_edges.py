import os.path


class Node:
    def __init__(self, name: str, weight=1.0):
        self.name = name
        self.frequency = weight

        self.connections = {}

    def add_frequency(self, weight=1.0):
        self.frequency += weight

    def add_connections(self, connections_list: list):
        # connections_list = list(dict.fromkeys(connections_list))
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

            # for the sake of having a complete frequency list
            if label in self.label_frequencies:
                self.label_frequencies[label] += 1
            else:
                self.label_frequencies[label] = 1

            if label in self.labels:
                self.labels[label].add_frequency(weight=weight)
            else:
                self.labels[label] = Node(label, weight=weight)
            self.labels[label].add_connections(label_list)

    def dump_csv(self, path: str):
        label_frequencies = dict(sorted(self.label_frequencies.items(), key=lambda item: item[1], reverse=True))

        for key in label_frequencies:
            new_key = key.replace(",", " ")
            if label_frequencies[key] > 99:
                label_frequencies[new_key] = label_frequencies[key]

        csv_strings = []
        for label in self.labels:
            csv_strings.append(self.labels[label].get_csv())

        with open(os.path.join(path, f"adjacency_{self.name}.csv"), "w", encoding="utf-8") as connections_file:
            connections_file.write("\n".join(csv_strings))

        graph_strings = []
        csv_strings = ["Id, Frequency"]
        label_index = []
        for label_label in list(label_frequencies):
            if label_frequencies[label_label] > 1:
                label_index.append(label_label)
                csv_strings.append(f"{label_label}, {label_frequencies[label_label]}")

        with open(os.path.join(path, f"frequency_{self.name}.csv"), "w", encoding="utf-8") as connections_file:
            connections_file.write("\n".join(csv_strings))

        graph_strings.append(f",{', '.join(label_index)}")
        for label in label_index:
            next_graph_string = label
            label_class = self.labels[label]

            for possible_label_connection in label_index:
                if possible_label_connection in label_class.connections:
                    possible_label_class = self.labels[possible_label_connection]

                    total1 = label_class.frequency
                    total2 = possible_label_class.frequency
                    if total2 > total1:
                        total1, total2 = total2, total1
                    connection = label_class.connections[possible_label_connection]
                    factor = float(total1) / float(total2)
                    raw_weight = connection * factor
                    weight = raw_weight / total1

                    next_graph_string += f", {weight}"
                else:
                    next_graph_string += ", 0"

            graph_strings.append(next_graph_string)

        with open(os.path.join(path, f"matrix_{self.name}.csv"), "w", encoding="utf-8") as graph_file:
            graph_file.write("\n".join(graph_strings))


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
