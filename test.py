from database_common import Database
import sys


print(sys.path)

db=Database('MS SQLSERVER','localhost','1433','master','sa','Wang1980')
db.getConnection()
print(db.getColumn('spt_fallback_dev'))
db.closeConnection()
