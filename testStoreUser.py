import zmq

def main():
    # Create ZeroMQ context
    context = zmq.Context()

    # Create REQ (request) socket
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5459")

    # ---- CHANGE THESE FOR TESTING ----
    #index, username, save, load
    index = 3
    username = "Bella"
    save = False
    load = True
    # ----------------------------------

    # Send login request
    socket.send_json({
        "index": index,
        "username": username,
        "save": save,
        "load": load
    })

    # Receive response
    reply = socket.recv_json()

    print(f"Returned data: {reply}")

if __name__ == "__main__":
    main()
