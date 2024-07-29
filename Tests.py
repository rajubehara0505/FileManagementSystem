import os
import unittest
from server import Server
from server import LoginCommands

class Test(unittest.TestCase):

    print(os.getcwd())

    def test_login(self):
        """
        Tests for the success and failure cases of registration
        """
        client = Server()
        input_values = [
            ['login','pramod','571'],['login','pramod','571'],['login','jacksparrow','420']
        ]
        expected_output = ['successfully logged in','User already loggedin','failed']
        results = []
        for input_list in input_values:
            results.append(client.login(input_list))
        self.assertListEqual(results, expected_output)

    def test_create_folder(self):
        """
        Tests for various outputs obtained during the creation of folder.
        """
        client = LoginCommands(os.getcwd(), os.getcwd(), 'pramod','571')
        inputs = ['folder1','folder1']
        expected_outputs = ['folder created','folder already exists']
        results = []
        for val in inputs:
            results.append(client.create_folder(val))
        self.assertListEqual(results, expected_outputs)

    def test_write_file(self):
        """
        tests for writing,editing in a file and clearing the file
        """
        client = LoginCommands(os.getcwd(), os.getcwd(), 'pramod','571')
        inputs = [

        ['writefile.txt', 'firstline\n'],
        ['writefile.txt','secondline\n'],['writefile.txt',None]

        ]
        expected_outputs = [
            'file entry successful',
            'file entry successful',
            'File cleared'
        ]
        result = []
        for file_list in inputs:
            result.append(client.write_file(file_list[0], file_list[1]))
        self.assertListEqual(result, expected_outputs)

    def test_change_folder_user(self):
        """
        This method checks various case scenerios of change_folder service.
        """
        current_directory = os.getcwd()
        user_current_directory = os.path.join(os.getcwd(), 'pramod')
        client = LoginCommands(current_directory, user_current_directory, 'pramod','571')
        inputs = [
            'first_folder','secondfolder','..','..','..','jacksparrow'
        ]
        changed_directory = os.path.join(user_current_directory,'first_folder')
        expected_outputs = [
            f'Directory changed to {changed_directory}','file not found',
            f'Directory changed to {user_current_directory}',f'Directory changed to {current_directory}',
            'access denied','file not found'
        ]
        result = []
        for folder_name in inputs:
            result.append(client.change_folder(folder_name))
        self.assertListEqual(result, expected_outputs)

    def test_read_file(self):
        """
        This method checks various case scenarios of read_file service.
        """
        userpath = os.path.join(os.getcwd(), 'pramod')
        client = LoginCommands(os.getcwd(), userpath, 'pramod','571')
        inputs = [None,'secondfile.txt',None]
        expectedvalues = ['Mention the file name that needs to be read in the arguments','This is second file','Reading secondfile.txt is finished']
        result = []
        for file_name in inputs:
            result.append(client.read_file(file_name))
        self.assertListEqual(result, expectedvalues)

if __name__ == '__main__':
    unittest.main()
