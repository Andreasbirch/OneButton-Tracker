from datetime import datetime
import os

before = datetime.now()
file_uid = ""
for i in range(100000):
    with open("/Volumes/\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0/boot_out.txt", "r") as file:
        for line in file:
            if line.startswith("UID:"):
                file_uid = line.strip().split(":")[1]
                break

after = datetime.now()
file_read_time = after-before

dir_uid = ""
before = datetime.now()
for i in range(100000):
    dir_uid = next(o for o in os.listdir("/Volumes/\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0/") if o.lower().startswith('.obt'))[4:]
after = datetime.now()
dir_read_time = after - before

print("Read from file. UID: {}, elapsed time: {}".format(file_uid, file_read_time))
print("Read from dir. UID: {}, elapsed time: {}".format(dir_uid, dir_read_time))