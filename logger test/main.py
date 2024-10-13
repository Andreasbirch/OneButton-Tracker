from logger import FileLogger, ConsoleLogger

logger = None


filename = "test.csv"
headers = ["Id", "Name"]

if True:
    logger = FileLogger(filename, headers)
else:
    logger = ConsoleLogger()

logger.log([
    "1",
    "Alice"
], 
[
    "2"])

logger.log(["3"])