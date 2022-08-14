import os
import pandas as pd
import json

import custom_json

class Label:
    def __init__(self, magazine: str, GRAPH_PATH="graph_matricies", ANALYZED_PATH="analyzed", modularity_file="{magazine}_modularity.csv", frequency_file="frequency_{magazine}.csv", label_file="{magazine}_label.json", override_description=False, keywords_in_description=1):
        self.magazine = magazine
        self.modularity_path = os.path.join(ANALYZED_PATH, modularity_file.format(magazine=magazine))
        self.label_path = os.path.join(ANALYZED_PATH, label_file.format(magazine=magazine))
        self.frequency_path = os.path.join(GRAPH_PATH, frequency_file.format(magazine=magazine))
        
        self.label_data = {}
        
        if not override_description and os.path.exists(self.label_path):
            with open(self.label_path, "r", encoding="utf-8") as f:
                self.label_data = json.load(f)
                
            return
        
        
        
        self.modularity = pd.read_csv(self.modularity_path)
        unwanted_columns = [
            "Id",
            "timeset"
        ]
        for unwanted_column in unwanted_columns:
            self.modularity.pop(unwanted_column)
        self.modularity.columns = ["Label", "modularity_class"]
        self.modularity = self.modularity.sort_values(by='modularity_class', ascending=True)
        
        self.frequency = pd.read_csv(self.frequency_path)
        
        
        """
        create a dict where the key is the community and the value is a dict containing every keyword
        of the community
        
        Every keyword is represented by a list where the key is the label and the value
        being the frequency of that keyword
        
        at the end every list gets sorted by frequency. While sorting the dict containing
        every label of a community gets converted in a list: [(label1, 10), (label2, 4)]
        """
        
        self.communities = {}
        
        # key is the keyword, value the community. Is temporary
        keyword_map = {}
        for index, row in self.modularity.iterrows():
            label = row['Label']
            community = str(row['modularity_class'])
            
            keyword_map[label] = community
            
            if community not in self.communities:
                self.communities[community] = {}
                
            self.communities[community][label] = 0
            
        for index, row in self.frequency.iterrows():
            # label, frequency
            label = row['label']
            frequency = row['frequency']
            
            if label not in keyword_map:
                continue
            
            community = keyword_map[label]
            self.communities[community][label] = frequency
            
        for community in self.communities:
            self.communities[community] = {"data": sorted(self.communities[community].items(), key=lambda x:x[1], reverse=True)}
            data = self.communities[community]["data"][:keywords_in_description]
            self.communities[community]["description"] = "; ".join([label[0] for label in data])
            
        self.label_data = self.communities
        with open(self.label_path, "w", encoding="utf-8") as f:
            print(self.label_path)
            """
            b = json.dumps(self.label_data)
            #b = b.replace('"##<', "").replace('>##"', "")
            b = fix_json_indent(b, indent=4)
            f.write(b)
            """
            b = custom_json.encode(self.label_data)
            f.write(b)

        self.hierarchy = []

    def set_slope(self, id, slope: float):
        if id in self.hierarchy:
            return

        self.hierarchy.append(id)
        self.label_data[str(id)]["slope"] = slope

    def commit_slopes(self):
        new_data = {}
        for id in self.hierarchy:
            new_data[id] = self.label_data[id]

        for key in self.label_data:
            if key not in self.hierarchy:
                new_data[key] = self.label_data[key]

        with open(self.label_path, "w", encoding="utf-8") as f:

            b = custom_json.encode(new_data)
            f.write(b)


    
    def get_description(self, community):
        return self.label_data[str(community)]["description"]
        