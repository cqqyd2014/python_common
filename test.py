from database_common import Database

db=Database('MS SQLSERVER','localhost','1433','master','sa','Wang1980')
print(db.testConnection())
