import csv

output = []
with open('all_stocks_5yr.csv',mode="r") as csv_file:
    reader = csv.reader(csv_file)
    
    for row in reader:
        temp = []
        for index,item in enumerate(row):
            if index == len(row)-1:
                temp.insert(0,item)
            else:
                temp.append(item)
        print(temp)
        output.append(temp)
csv_file.close()
print(output)