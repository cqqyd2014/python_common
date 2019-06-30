from database_common import Database
import sys
from common import BackSystem




db=Database('ORACLE','localhost','1521','orcl','system','Wang1980')
db.getConnection()
list1=db.getColumn('HELP')
print(list1)


#db.openBatchCursor('HELP',list1)
print(db.getTopRowCells('HELP',5,list1))
#print(db.getBatchCursorRowCount())

#print(db.getBatchCursorRows(2))
#print(db.getBatchCursorRows(2))
#print(db.getBatchCursorRows(2))
#print(db.getBatchCursorRowCount())
#db.closeBatchCursor()

db.closeConnection()
#print(BackSystem.getpids_by_name('Common'))
