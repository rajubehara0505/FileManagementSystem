"""
This is the server application.

"""
import os
import datetime
import time

class Server:
    """
      This is the server class.
      Attributes:
        username (str) : user ID of the user
        password (str) : password for the user
        root_directory (str) : root directory path
        current_directory (str) : current working directory path
        client_request (str): stores the client requests
    """
    def __init__(self):
        """
        This is the constructor for the Server class
        """
        self.username = None
        self.password = None
        self.root_directory = os.getcwd()
        self.current_directory = ''
        self.client_request = ''
        self.client = object

    def search_user(self, user_name:str)->str:
        """
        This method checks for the user if already in the system.
        Args:
            user_name (str): username of the user

        Returns:
            str: returns whether the user exists or not in the system
        """
        try:
            user_log = str(f'{self.root_directory}\\users_registry.txt')
            with open(user_log,'r') as open_file:
                usersdetails = open_file.readlines()
            users = []
            for user in usersdetails:
                user_split = user.strip().split(",",1)
                users.append(user_split[0])
            print(users)
            if user_name in users:
                return 'member in the system'
            return 'Not a member'
        except:
            return 'error occured'

    def register(self)->str:
        """This method registers new users in to the system.
        """
        divided_client_request = self.client_request.split(' ', 3)
        username = divided_client_request[1]
        password = divided_client_request[2]
        status = self.search_user(username)
        if status == 'member in the system':
            return status
        file_name = str(f'{self.root_directory}\\users_registry.txt')
        with open(file_name, 'a+') as append_file:
            user_data = str(f'{username},{password}\n')
            append_file.writelines(user_data)
            append_file.close()
        self.start_user_commands()
        self.client.create_folder(username)
        return status

    def fetch_password(self, user_name:str) -> str:
        """
        The method that returns the password, if exists,
        to the corresponding username from the server.

        Args:
            user_name (str): username of the user

        Returns:
            [str]: password of the corresponding user if exists.
        """

        with open('users_registry.txt','r') as users_log:
            users = users_log.readlines()
            print(users)
        user_names = []
        user_passwords = []
        for line in users:
            line_split = line.strip().split(",",1)
            user_names.append(line_split[0])
            user_passwords.append(line_split[1])
        for j in range(0, len(user_names)):
            if user_name == user_names[j]:
                user_credentials = user_passwords[j]
                return user_credentials
        user_credentials = 'failed'
        return user_credentials

    def start_user_commands(self):
        """
        This method invokes the logincommands class after the successful login of the user.

        """
        self.client = LoginCommands(self.root_directory,self.current_directory,
                                    self.username,self.password)

    def add_to_loginlog(self, directory:str, file_name:str, username:str):
        """
        This method adds the user into the loginlog to make sure
        no one logins with the same credentials during the user login.
        Args:
            directory (str): location of the loginlog file
            file_name (str): loginlog file
            input1 (str): username
        """

        file_name = str(f'{directory}\\{file_name}')
        with open(file_name,'a+') as loginlog:
            user_data = [username, "\n"]
            loginlog.writelines(user_data)
            loginlog.close()

    def login(self, divided_client_request:list)->str:
        """
        This method login the user into the system.

        Args:
            divided_client_request (list): This is the divided request i.e,
                                           command and arguments, received from the client.
        Returns:
            [str]: returns whether the login is success or failure
        """
        username = divided_client_request[1]
        with open('users_loggedin.txt') as loggedinusers_file :
            if username in loggedinusers_file.read():
                return 'User already loggedin'
        password = divided_client_request[2]
        response = self.fetch_password(username)
        if response == 'failed':
            return 'failed'
        if response==password:
            cwd = os.path.join(self.root_directory, username)
            self.current_directory = cwd
            self.username = username
            self.password = password
            self.start_user_commands()
            self.add_to_loginlog(self.root_directory,'users_loggedin.txt',self.username)
            return 'successfully logged in'
        return 'failed'

    def user_requests(self, divided_client_request:list)->str:
        """This is the method where the user_request are analyzed and respective function calls occur.

        Args:
            divided_client_request (list): This is the divided client request to process the command.

        Returns:
            str: status of each request is processed and returned.
        """

        request = divided_client_request[0]
        if self.username is None:
            if request == 'login':
                try:
                    response = self.login(divided_client_request)
                except:
                    response = 'Login Error'
                return response
            elif request == 'register':
                try:
                    response = self.register()
                except:
                    response = 'Register Error'
                return response
            return 'failed'
        if request == 'list':
            try:
                response = self.client.list_files()
            except:
                response = 'error occured'
            return response

        elif request == 'change_folder':
            try:
                folder_name = divided_client_request[1]
                response = self.client.change_folder(folder_name)
            except:
                response = 'Failed'
            return response

        elif request == 'read_file':
            try:
                file_name = divided_client_request[1]
                response = self.client.read_file(file_name)
            except IndexError:
                response = self.client.read_file(None)
            except:
                response = 'error occured'
            return response

        elif request == 'write_file':
            try:
                file_name = divided_client_request[1]
                file_entry = divided_client_request[2]
                response = self.client.write_file(file_name, file_entry)
            except IndexError:
                response = self.client.write_file(file_name)
            except:
                response = 'error occured'
            return response

        elif request == 'create_folder':
            try:
                folder_name = divided_client_request[1]
                response = self.client.create_folder(folder_name)
            except:
                response = 'error occured'
            return response
        else:
            return 'Invalid argument'

    def divide(self, client_request:str)->str:
        """This method splits the client request and process

        Args:
            client_request (str): This is the client request recieved from the client.

        Returns:
            str: response to the client from the server.
        """

        self.client_request = client_request
        divided_client_request = self.client_request.split(' ', 2)
        print('client_request split: ', divided_client_request)
        result = self.user_requests(divided_client_request)
        print('client_request split reply: ', result)
        return result

    def eraselog(self):
        """
        This function removes the username from the loginlog when the user quits from the system
        """
        with open("users_loggedin.txt", "r") as file_input:
            file_lines = file_input.readlines()
            with open("users_loggedin.txt", "w") as output:
                for line in file_lines:
                    if line.strip("\n") != self.username:
                        output.write(line)


class LoginCommands:
    """
    This is the LoginCommands class which contains the commands
    that a user can issue after successful login.
    """

    def __init__(self, root_directory, current_directory, username, password):
        """This is the constructor for the LoginCommands class"""
        self.username = username
        self.password = password
        self.root_directory = root_directory
        self.current_directory = current_directory
        self.read_file_name = None
        self.index = 0

    def dir_reverse(self, val:str)->str:
        """
        This method reverses the given string.
        Args:
            val (str): string that needs to be reversed.

        Returns:
            str: reverded string
        """
        return val[::-1]
    def change_folder(self, folder_name:str)->str:
        """
        This method changes the location of the current working directory
        if the given path exists.
        Args:
            folder_name (str): Location to which the directory has to be changed

        Returns:
            str: Status regarding the changing of the directory.
        """
        root_path = self.dir_reverse(self.root_directory)
        reference = root_path.find('\\')+1
        end_of_the_line = self.dir_reverse(root_path[reference:])
        try:
            if folder_name == '..':
                step_back = self.dir_reverse(self.current_directory)
                reference = step_back.find('\\')+1
                new_path = self.dir_reverse(step_back[reference:])
                if new_path == end_of_the_line:
                    return 'access denied'
                self.current_directory = new_path
                reply = f'Directory changed to {self.current_directory}'
                return reply
            if self.current_directory == self.root_directory:
                if folder_name == self.username:
                    step_forward = os.path.join(self.current_directory, folder_name)
                    self.current_directory = step_forward
                    reply = 'Directory changed to '+self.current_directory
                    return reply
                return 'file not found'
            step_forward = os.path.join(self.current_directory, folder_name)
            if os.path.isdir(step_forward):
                self.current_directory = step_forward
                reply = 'Directory changed to '+self.current_directory
                return reply
            return 'file not found'
        except:
            reply = 'something went wrong'
            return reply
        return 'error'

    def list_files(self):
        """
        Details of all the files which are present in the
        current working directory are shown with the help of this method.
        """
        total_data = ''
        path = self.current_directory
        sub_folders_name = [ f.name for f in os.scandir(path) if f.is_dir() ]
        for sub_folder_name in sub_folders_name:
            total_data = total_data + str(sub_folder_name)
        for root,files in os.walk(path):
            for file_list in files:
                file_list=os.path.join(root,file_list)
                file_size = os.path.getsize(file_list)
                createdate = time.ctime(os.path.getctime(file_list))
                rev = self.dir_reverse(file_list)
                reference = rev.find('\\')
                folder_name = self.dir_reverse(rev[:reference])
                sub_listoffiles = f'{folder_name}, Size:{file_size},Created date:{createdate}\n'
                total_data = total_data + sub_listoffiles
        return total_data

    def read_file(self, file_name:str=None)->str:
        """
        This method reads the content in the file 100 characters per a call.
        Args:
            file_name (str, optional): Name of the file whose content neeeds to be read.
            Defaults to None.

        Returns:
            str: status regarding the reading of the file.
        """

        if file_name is None:
            if self.read_file_name is not None:
                response = f'Reading {self.read_file_name} is finished'
                self.read_file_name = None
                return response
            response = 'Mention the file name that needs to be read in the arguments'
            return response
        file_path = os.path.join(self.current_directory, file_name)
        try:
            if os.path.exists(file_path):
                if self.read_file_name == file_name:
                    boundary = self.index+100
                    with open(file_path,'r') as file:
                        entire_file = file.read()
                    if boundary >= len(entire_file):
                        response = f'{entire_file[self.index:len(entire_file)]}file read complete.'
                        self.index = 0
                        return response
                    response = str(entire_file[self.index:boundary])
                    self.index = self.index+100
                    return response
                self.read_file_name = file_name
                with open(file_path,'r') as file:
                    response = file.read(100)
                    self.index = 100
                    return response
            response = 'file cannot be found in the current directory'
            return response
        except PermissionError:
            response = 'Requested file to read is a folder'
            return response
        except:
            response = 'error occured'
            return response

    def write_file(self, file_name:str, file_entry:str=None)->str:
        """
        This method helps in creating a new file or appends the text into an existing file.
        If no text is given for entry then the text in the file will be cleared.

        Args:
            file_name (str): Name of the file where the text entry has to be done.
            file_entry (str, optional): Text that needs to be entered. Defaults to None.

        Returns:
            str: status regarding the text entry into a file.
        """

        file_path = os.path.join(self.current_directory, file_name)
        if file_entry is None:
            with open(file_path,'w') as write_file:
                write_file.close()
            response = 'File cleared'
            return response
        with open(file_path,'a') as write_file:
            file_entry = [file_entry, "\n"]
            write_file.writelines(file_entry)
            write_file.close()
        response = 'file entry successful'
        return response

    def create_folder(self, folder_name:str)->str:
        """
        This method creates a folder in the present working directory of the user.

        Args:
            folder_name (str): Name of the that needs to be created.

        Returns:
            str: status regarding the folder creation.
        """
        try:
            folder_path = os.path.join(self.current_directory, folder_name)
            os.mkdir(folder_path)
        except FileExistsError:
            return 'folder already exists'
        except:
            return 'failed to create the folder'
        return 'folder created'






