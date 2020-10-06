import asyncio
import websockets
import json

available_clients = set()
server_socket = None
SERVER_KEY = "hy^3se%^GbuIoHEd"  # TODO move to env


# usual python function which waits until it receives
# message from client, and then echos it.
# it then sends a response
async def response(websocket, path):
    global server_socket

    auth_data = await websocket.recv()
    auth_data = json.loads(auth_data)

    auth_response = {
        "success": False
    }

    if auth_data["type"] == "server":
        if auth_data["password"] == SERVER_KEY:
            auth_response["success"] = True

    elif auth_data["type"] == "client":
        auth_response["success"] = True

    await websocket.send(json.dumps(auth_response))

    if not auth_response["success"]:
        return

    if auth_data["type"] == "server":
        server_socket = websocket
        print("New Server added")
    else:
        available_clients.add(websocket)
        print("New client added")

    while True:
        try:
            msg = await websocket.recv()
            print(msg)

            if websocket is server_socket:
                await broadcast_to_clients(msg)
            else:
                pass
        except websockets.ConnectionClosed:
            if websocket is server_socket:
                server_socket = None
            else:
                available_clients.remove(websocket)
            print("Terminated")
            break


async def broadcast_to_clients(text):
    for client_socket in available_clients:
        await client_socket.send(text)


start_server = websockets.serve(response, "192.168.0.13", 1234)

loop = asyncio.get_event_loop()
asyncio.ensure_future(start_server)

loop.run_forever()
