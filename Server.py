import asyncio
import websockets
import os
from datetime import datetime

# Get port from Render environment variable
PORT = int(os.environ.get('PORT', '10000'))

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

async def append_to_file(log_file_path, data):
    timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    with open(log_file_path, 'a') as f:
        f.write(f'[{timestamp}] {data}\n')

async def handler(websocket, path):
    try:
        user_id = await websocket.recv()
        log_file_path = os.path.join('logs', f'{user_id}.log')
        print(f"Connection established with User ID: {user_id}")
        async for message in websocket:
            await append_to_file(log_file_path, message)
    except websockets.ConnectionClosed:
        print(f"Connection closed for {path}.")
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        print(f"Handler for {path} terminated.")

async def main():
    server = await websockets.serve(
        handler, 
        host='0.0.0.0',
        port=PORT
    )
    print(f"Server started on port {PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down.")