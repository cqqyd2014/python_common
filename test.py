from database_common import Database
from db_type_to_sys_type import DbTypeToSysType

db=Database('MS SQLSERVER','localhost','1433','master','sa','Wang1980')
db.getConnection()
print(db.getColumn('spt_fallback_dev'))
db.closeConnection()
