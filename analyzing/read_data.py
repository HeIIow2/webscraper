import json
import analyze as an

with open("data.csv", "r", encoding="utf-8") as data_file:
    lines = data_file.read().split("\n")[:-1]
    
data = []    

for line in lines:
    data.append(json.loads(line))
    
    an.save_labels(data[-1]["keywords"])
    
an.finished()
    
print(len(data))