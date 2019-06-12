import pymssql

from db_type_to_sys_type import DbTypeToSysType


class Database:
    conn=None
    def __init__(self,db_type,db_address,db_port,db_name,db_username,db_password):    #构造函数，类接收外部传入参数全靠构造函数
        self.db_type = db_type
        self.db_address = db_address
        self.db_port = db_port
        self.db_name=db_name
        self.db_username=db_username
        self.db_password=db_password

    def getTables(self):
        #select name from sysobjects where xtype='u'
        cursor = self.conn.cursor()
        cursor.execute("select name from sysobjects where xtype='u'")
        tables=[]
        for row in cursor:
            #print('row = %r' % (row,))
            
            tables.append(row[0])
        cursor.close()
        return tables

    def getColumn(self,table_name):
        '''
        select  b.name colName, c.name colType ,c.length colLength

from sysobjects a inner join syscolumns b
on a.id=b.id and a.xtype='U'
inner join systypes c
on b.xtype=c.xusertype
where a.name='03对手为正贵的对公账号的流水信息'
'''
        cursor = self.conn.cursor()
        cursor.execute("select  b.name colName, c.name colType ,c.length colLength from sysobjects a inner join syscolumns b on a.id=b.id and a.xtype='U' inner join systypes c on b.xtype=c.xusertype where a.name='"+table_name+"' and c.name not in('binary','varbinary','image')")
        columns=[]
        for row in cursor:
            #print('row = %r' % (row,))
            
            columns.append([row[0],DbTypeToSysType.mssql(row[1])])
        cursor.close()
        return columns




    def testConnection(self):
        conn_result=self.getConnection()
        if (conn_result=="Connected to database"):
            self.closeConnection()
            return {'tf':True,'connect_message_body':'数据库连接成功','connect_message_type':'success'}
        else:
            return {'tf':False,'connect_message_body':'数据库连接失败：'+conn_result,'connect_message_type':'danger'}

    

    def getConnection(self):
        print(self.db_type)
        try:
                
            if self.db_type=='MS SQLSERVER':
                self.conn = pymssql.connect(server=self.db_address,port=self.db_port,user=self.db_username,password=self.db_password,database=self.db_name)
        except (pymssql.InterfaceError,pymssql.OperationalError) as e:
            return "Connect Failed:"+str(e)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        
        else:
            print("connected ok")
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


