# cs361-storeUser
## Note: Will split save and load into two microservices with a different payload/send_json as they need different data. Will update after complete.

Have csv file have a header and data formatted like so:
    index,username,items,quests
    1,Poppy,"[""glasses""]","{""Missing Glasses"": ""in_progress"", ""Collect the Children"": ""not_started"", ""Barter with the Baker"": ""not_started""}"
    2,Joe,[],"{""Missing Glasses"": ""not_started"", ""Collect the Children"": ""not_started"", ""Barter with the Baker"": ""not_started""}"
    3,Bella,[],"{""Missing Glasses"": ""completed"", ""Collect the Children"": ""not_started"", ""Barter with the Baker"": ""not_started""}"

Send data to the microservice like so:
    socket.send_json({
        "index": index,
        "username": username,
        "save": save,
        "load": load
    })

Recieve data from microservice like so:
    reply = socket.recv_json()

    print(f"Returned data: {reply}")
