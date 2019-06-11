from database_common import Database

db=Database('MS SQLSERVER','localho1st','1433','master','sa','Wang1980')
print(db.testConnection())
