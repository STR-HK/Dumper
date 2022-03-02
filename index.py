import dumper

db = dumper.Dumper()
db.setDumpPath("./dump")

db.setData("key", "value")
db.setData("a", "value2")

import time

time.sleep(3)

db.dump()
