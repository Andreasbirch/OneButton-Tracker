import os

class FileLogger():
    folderPath = "data"
    filePath = None
    
    def __init__(self, filename, headers=None):
        if self.folderPath not in os.listdir():
            os.mkdir(self.folderPath)
        
        self.filePath = self.folderPath + os.sep + filename

        if filename not in os.listdir(self.folderPath):
            with open(self.filePath, 'w') as file:
                if headers:
                    file.write(','.join(headers)+"\n")

    def log(self, *rows):
        with open(self.filePath, '+a') as file:
            for row in rows:
                file.write(','.join(row) + "\n")

class ConsoleLogger():
    def log(self, *rows):
        for row in rows:
            if isinstance(row, str):
                print(row)
            else:
                print(', '.join(row))