from database_common import Database
import sys
from common import BackSystem




db=Database('MS SQLSERVER','localhost','1433','0002','sa','Wang1980')
db.getConnection()
list1=db.getColumn('01对手为正贵的对公流水')

print(list1)
db.openBatchCursor('01对手为正贵的对公流水',list1)
print(db.getBatchCursorRowCount())

print(db.getBatchCursorRows(2))
print(db.getBatchCursorRows(2))
print(db.getBatchCursorRows(2))
print(db.getBatchCursorRowCount())
db.closeBatchCursor()
db.closeConnection()
print(BackSystem.getpids_by_name('Common'))
