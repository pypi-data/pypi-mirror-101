import logging
import paramiko
from paramiko.ssh_exception import AuthenticationException, PasswordRequiredException

logger = logging.getLogger(__name__)

class BaseConnector():
    def __init__(self) -> None:
        pass

    def __login(self):
        '''Connect to device and login'''
        raise NotImplementedError

    def __logout(self):
        '''Logout and close connection'''
        raise NotImplementedError

class SSHConnector(BaseConnector):
    '''SSH connector'''
    def __init__(self, hostname:str, port=22, authentication = 'password',
                 username:str='', password:str='') -> None:
        self.hostname = hostname
        self.port = port
        self.authentication = authentication
        self.username = username
        
        self.password = password
        super().__init__()

    def __login(self):
        '''Connects to host using SSH'''
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        if self.authentication == 'password':
            if self.hostname and self.username:    
                if self.password:
                    self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
                else: 
                    ('Password authentication selected but password not provided or blank')
                    raise PasswordRequiredException
            else:
                logger.error('Hostname or username not provided or blank. \nHostname: {}\nUsername: {}'.format(
                                                self.hostname, self.username))
                raise AuthenticationException
        else:
            raise NotImplementedError

    def __logout(self):
        '''Logout and close session'''
        self.client.close()


    def send_command(self, command: str) -> tuple:
        '''Sends a single command returns tuple with stdin, stdout, stderr'''
        try:
            self.__login()
            stdin, stdout, stderr = self.client.exec_command(command)
            return (stdin, stdout, stderr)
        except Exception as e:
            print(e)
        finally:
            self.__logout()     

class RESTConnector(BaseConnector):
    '''REST connector.'''
    def __init__(self) -> None:
        logger.warning('REST connector needs implementation')
        super().__init__()
    