import pymssql


class Database:
    conn=None
    def __init__(self,db_type,db_address,db_port,db_name,db_username,db_password):    #构造函数，类接收外部传入参数全靠构造函数
        self.db_type = db_type
        self.db_address = db_address
        self.db_port = db_port
        self.db_name=db_name
        self.db_username=db_username
        self.db_password=db_password

    def testConnection(self):
        conn_result=self.getConnection()
        if (conn_result=="Connected to database"):
            self.closeConnection()
            return {'tf':True,'message_body':'数据库连接成功','message_type':'success'}
        else:
            return {'tf':False,'message_body':'数据库连接失败：'+conn_result,'message_type':'danger'}

    def getConnection(self):
        try:
                
            if self.db_type=='MS SQLSERVER':
                self.conn = pymssql.connect(server=self.db_address,port=self.db_port,user=self.db_username,password=self.db_password,database=self.db_name)
        except (pymssql.InterfaceError,pymssql.OperationalError) as e:
            return "Connect Failed:"+str(e)
        
        else:
            return "Connected to database"


    def closeConnection(self):
        self.conn.close()
    
    def getVersion(self):
        if self.db_type=='MS SQLSERVER':
            cursor = self.conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version=cursor.fetchone()[0]
            cursor.close()
            return version


