
import csv
csv_file = "temp_db.csv"

header = ["ID", "user", "url"]
def get_id():
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader)
            max_id =0
            for row in reader:
                max_id =max(max_id, int(row[0]))
            return max_id+1
    except FileNotFoundError:
        return 1
    
def create_csv():
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8"):
            file_exist = True
    except FileNotFoundError:
        file_exist = False
    if not file_exist:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)


def add_data(name, url):

    create_csv()

    id = get_id()
    print(name)
    with open(csv_file, mode="a", newline="",encoding="utf-8" ) as file:
        update_file = csv.writer(file)
        update_file.writerow([id, name, url])




# add_data("Jaw", "dasdasdasdsad")


