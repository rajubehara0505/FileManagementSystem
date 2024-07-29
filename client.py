"""
This is client application.
"""
import asyncio

Log = ''
def req_filter(message:str)->bool:
    """
    Requests that need to be sent to the server are filtered in this method.

    Returns:
        bool: returns boolean value whether to send the request to the server or not.
    """
    split_message = message.split(' ', 1)
    command = split_message[0]
    count_arguments = len(split_message)
    global Log
    if command == 'commands':
        if count_arguments == 1:
            c_file = open('command_guide.txt', 'r')
            content = c_file.read()
            print(content)
            return False
        elif count_arguments == 2:
            argument = split_message[1]
            if argument == 'requested':
                print(Log)
                return False
            print('Invalid command')
            return False
        print('invalid arguments')
        return False
    Log += str('\n'+message)
    return True

def register():
    """
    This method creates a registration form for the user.
    """
    print('\n\n\t\t\tREGISTRATION FORM\n\n')
    user_name = input('Create User Name : ')
    password = input('Create Password : ')
    result = str(f'register {user_name} {password} ')
    return result

def login():
    """
    This method creates a login form for the user.
    """
    print('\n\n\t\t\tLOGIN FORM\n\n')
    user_name = input('Enter your User Name : ')
    password = input('Enter your Password : ')
    result = str(f'login {user_name} {password}')
    return result

async def server_connect():
    """
    This method is responsible for eshtablishing the connection with the user.
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 4567)
    print('\n\n\t\tA Simplified File Management System')
    while True:
        print('1.Register\n2.Login')
        option = int(input('Enter your choice : '))
        if option == 1:
            client_req = register()
            writer.write(client_req.encode())
            data = await reader.read(5000)
            server_res = data.decode()
            print(server_res)
            if server_res == 'Not a member':
                print('New user Created and joined as a member')
                print("Now login")
                option = 2
            elif server_res == 'member in the system':
                print('User Already Exist ')
                print('Try again')
                continue
            else:
                print('Error has Occured, Please Try Again ')
                continue
        if option == 2:
            client_req = login()
            writer.write(client_req.encode())
            data = await reader.read(5000)
            server_res = data.decode()
            print(server_res)
            if server_res == 'successfully logged in':
                print('Login Successful')
                break
            elif server_res == 'failed':
                print('Login Failed\tTry Again')
                continue
            elif server_res == 'incorrect password':
                print('Password incorrect')
                continue
            elif server_res == 'invalid argument':
                print('invalid input ')
                continue
            elif server_res == 'User already loggedin':
                print('user is already loggedin from another client')
                continue
            else:
                print('Error has Occured, Please Try Again ')
                continue
        else:
            print('Invalid Option! Try Again Entering Following Options.. ')

    while True:
        print("Enter 'commands' for help\n")
        print("Enter 'commands requested' for the commands requested till now\n")
        user_req = input('----->')
        if user_req == 'quit':
            writer.write(user_req.encode())
            break
        elif user_req == '':
            continue
        client_req = req_filter(user_req)
        if client_req is True:
            writer.write(user_req.encode())
            data = await reader.read(5000)
            print(f'{data.decode()}')
    print('Close the connection')
    writer.close()

try:
    asyncio.run(server_connect())

except ConnectionRefusedError:
    print('Connection falied')