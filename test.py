from database_common import Database
import sys




db=Database('MS SQLSERVER','localhost','1433','master','sa','Wang1980')
db.getConnection()
list1=db.getColumn('spt_monitor')


db.openBatchCursor('spt_monitor',list1)
print(db.getBatchCursorRowCount())

print(db.getBatchCursorRows(2))
print(db.getBatchCursorRows(2))
print(db.getBatchCursorRows(2))
print(db.getBatchCursorRowCount())
db.closeBatchCursor()
db.closeConnection()
