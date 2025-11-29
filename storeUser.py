import csv
import json
import zmq

def loadUser(index, username, filename):
    try:
        with open(filename, newline="", encoding="utf8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["index"]) == index and row["username"] == username:
                    row["items"] = json.loads(row["items"])
                    row["quests"] = json.loads(row["quests"])
                    #If so return the row of the user's data
                    return row
    #If the file can't be found return 0
    except FileNotFoundError:
        return 0
    #If the username and index doesn't exist return none
    return None

def saveUser(updatedRow, filename):
    rows = []
    try:
        #Open the provided file for reading
        with open(filename, newline="", encoding="utf8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    #If the file cant be found return 0
    except FileNotFoundError:
        return 0
    #For each row update items and quests
    found = False
    if not rows:
        return 0
    try: 
        for row in rows:
            if int(row["index"]) == int(updatedRow["index"]):
                row["items"] = json.dumps(updatedRow["items"])
                row["quests"] = json.dumps(updatedRow["quests"])
                found = True
                break
    except Exception as e:
        print("Error json encoding: ", e)
        return 0
    if not found:
        return 0
    #Now try to write back to the csv
    try:
        with open(filename, "w", newline="", encoding="utf8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        return 1
    #If the file cant be found return 0
    except FileNotFoundError:
        return 0

#Make sure the message recieved from user is correct
def validate_info(msg):
    index = msg.get("index")
    username = msg.get("username")
    save = msg.get("save")
    load = msg.get("load")

    if index is None or username is None or save is None or load is None:
        return None, None, None, None, False
    
    return index, username, save, load, True

def main():
    #Create zmq context
    context = zmq.Context()
    #Create a socket at port 5459
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5459")

    print("Store user microservice running on port 5459...", flush=True)

    while True:
        #Recieve the message
        message = socket.recv_json()

        index, username, save, load, valid = validate_info(message)

        #If request is not valid give respond with an error
        if not valid:
            socket.send_json("ERROR user input is wrong")
            continue

        row = loadUser(index, username, "test_userData.csv")
        if load:
            if row:
                socket.send_json(row)
            else:
                socket.send_json("ERROR could not load user data")
            continue
        
        if save:
            bool = saveUser(row, "test_userData.csv")
            if bool:
                socket.send_json("Saved successfully")
            else:
                socket.send_json("ERROR could not save")
            continue

if __name__ == "__main__":
    main()
