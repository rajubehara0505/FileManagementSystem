import asyncio
import signal
from server import Server
#keyboard interupt
signal.signal(signal.SIGINT, signal.SIG_DFL)
#this dictionary contains the no of clients connected to the server
clients_connected = {}

async def client_communication(reader:object, writer:object):
    """This is the method that acts as a connection for the communication between the server and the client.

    Args:
        reader (object): StreamReader object
        writer (object): StreamWriter object
    """

    client_address = writer.get_extra_info('peername')
    clients_connected[client_address[1]] = Server()
    print(f"{client_address} is connected to the server")
    while True:
        data = await reader.read(5000)
        client_req = data.decode().strip()
        command_no = client_req.find(" ")
        client_req_command = client_req[:command_no]
        if client_req == 'quit':
            clients_connected[client_address[1]].eraselog()
            break
        print("Received",client_req_command," request from",client_address)
        #server communication
        server_res = clients_connected[client_address[1]].divide(client_req)
        print(f"Server Response: {server_res}")
        writer.write(server_res.encode())
        await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    """
    This is the main method for the server creation program.
    """
    server_ip = '127.0.0.1'
    port = 4567
    logfile = open('users_loggedin.txt', 'w')
    logfile.close()
    server = await asyncio.start_server(client_communication, server_ip, port)

    server_address = server.sockets[0].getsockname()
    print(f'Serving on {server_address}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
