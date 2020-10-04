import asyncio
import websockets


# usual python function which waits until it receives
# message from client, and then echos it.
# it then sends a response
async def response(websocket, path):
    print(websocket)
    await websocket.send("Hi client " + path)
    await websocket.send("How are you?")


start_server = websockets.serve(response, "localhost", 1234)
asyncio.get_event_loop().run_until_complete(start_server)
print("hi")
asyncio.get_event_loop().run_forever()
print(start_server)
