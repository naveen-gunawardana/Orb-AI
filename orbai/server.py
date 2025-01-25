import asyncio
import websockets

clients = set()

async def websocket_handler(websocket, path):
    """
    Handle WebSocket connections and broadcast messages.
    """
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[WebSocket] Message received: {message}")
            # Broadcast the message to all connected clients
            await asyncio.wait([client.send(message) for client in clients if client != websocket])
    except websockets.ConnectionClosed:
        print("[WebSocket] Connection closed")
    finally:
        clients.remove(websocket)

# Start the WebSocket server
start_server = websockets.serve(websocket_handler, "localhost", 8000)

print("[WebSocket] Server running on ws://localhost:8000")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
