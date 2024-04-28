from abc import ABC, abstractmethod
import os
import datetime

class Datastore(ABC):
    """Ability to store data in specific sink."""
    @abstractmethod
    def save(self, response, filename):
        pass



class LogFiles(Datastore):
    def __init__(self, log_path):
        """Setup log store directory.
        Args:
            log_path: path to store responses.
        """
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        self.log_path = log_path
        
    def save(self, response, filename=None):
        if filename is None:
            filename = datetime.time().strftime('%Y%m%d-%H%M%S-%f_response.json')
        filepath = os.path.join(self.log_path, filename)
        with open(filepath, 'wt') as fp:
            fp.write(response)
            

if __name__ == "__main__":
    ds = LogFiles('./temp/log1.json')
    
