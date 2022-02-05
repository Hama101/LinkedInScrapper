import pandas as pd
import json
import os

def get_data_from_csv(path):
    df = pd.read_csv(path)
    #print each row from df
    data = []
    for index, row in df.iterrows():
        print(row)
        #convert each row to json
        json_data = row.to_json()
        #convert json to python dict
        data.append(json.loads(json_data))
        #print each key and value from dict
        for key, value in data[index].items():
            print(key, value)
    #convert dataframe to json using json.dumps
    return data

#loop throw data and see it it have images with it username in images folder
def check_images(data):
    print(len(data))
    for item in data:
        #load all file names to a list from images folder
        files = os.listdir('images')
        #check if username is in the list
        if f"{item['username']}.jpg" in files:
            print(item['username'], 'is in the folder')
        else:
            #delete the item from the data
            data.remove(item)
            print(item['username'], 'is not in the folder')
    print(len(data))
    return data


def csv_to_json(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile , indent=4)


if __name__ == '__main__':
    path = 'data.csv'
    
    data = get_data_from_csv(path)
    data = check_images(data)
    csv_to_json(data)