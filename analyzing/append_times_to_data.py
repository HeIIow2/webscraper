import json

# date, index
times = []

with open("time_ind.csv", "r") as time_file:
    raw_times = time_file.read().split("\n")
    
    for raw_time in raw_times:
        if raw_time == "":
            continue
        splitted = raw_time.split(", ")
        times.append((splitted[0], int(splitted[1])))
        
print(times)

with open("data_date.csv", "w") as new_data:
    with open("data.csv", "r") as data_file:
        raw_jsons = data_file.read().split("\n")
        latest_date_ind = 0
        latest_date_elem = times[0]
        for i, raw_json in enumerate(raw_jsons):
            if raw_json == "":
                continue
            if len(times) >= latest_date_ind+2:
                if i >= times[latest_date_ind+1][1]:
                    latest_date_ind += 1
                    latest_date_elem = times[latest_date_ind]
                
            _json = json.loads(raw_json)
            _json["date"] = latest_date_elem[0]
            
            json_str = json.dumps(_json)
            new_data.write(json_str + "\n")