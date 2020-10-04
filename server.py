import asyncio
import websockets

available_clients = set()


# usual python function which waits until it receives
# message from client, and then echos it.
# it then sends a response
async def response(websocket, path):
    available_clients.add(websocket)
    print("New client added:", path)

    while True:
        try:
            msg = await websocket.recv()
            await broadcast_to_clients(msg)
        except websockets.ConnectionClosed:
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
