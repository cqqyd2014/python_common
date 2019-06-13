from database_common import Database
import sys




db=Database('MS SQLSERVER','localhost','1433','master','sa','Wang1980')
db.getConnection()
list1=db.getColumn('spt_monitor')
print(db.getTopRowCells('spt_monitor',5,list1))
db.closeConnection()
