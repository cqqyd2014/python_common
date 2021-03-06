import pymssql
import cx_Oracle
from .db_type_to_sys_type import DbTypeToSysType
import datetime





class Database:
    conn=None

    def formate_col_name(self,col_name):
        if self.db_type=='MS SQLSERVER':
            return '['+col_name+"]"
        if self.db_type=='ORACLE':
            return col_name

    def formate_table_name(self,table_name):
        if self.db_type=='MS SQLSERVER':
            return '['+table_name+"]"
        if self.db_type=='ORACLE':
            return table_name

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
        if self.db_type=='MS SQLSERVER':
            cursor.execute("select name from sysobjects where xtype='u'")
        if self.db_type=='ORACLE':
            cursor.execute('select table_name from user_tables')
        tables=[]
        for row in cursor:
            #print('row = %r' % (row,))
            
            tables.append(row[0])
        cursor.close()
        return tables


    

    def openBatchCursor(self,table_name,cols_list):
        table_name=self.formate_table_name(table_name)
        self.batch_cursor=self.conn.cursor()
        cols_arry=[]
        for i in cols_list:
            if i[2]!='不导入':
                cols_arry.append(self.formate_col_name(i[0]))
        cols=','.join(cols_arry)
        sql="select "+cols+" from "+table_name
        print(sql)
        self.batch_cursor.execute(sql)
    
    def getBatchCursorRowCount(self):
        return self.batch_cursor.rowcount

    def closeBatchCursor(self):
        self.batch_cursor.close()

    def getBatchCursorRows(self,arraysize):
        rows=self.batch_cursor.fetchmany(arraysize)
        new_rows=[]
        for row in rows:
            #print(row)
            new_cols=[]
            for col in row:
                if isinstance(col, str):
                    col = self.dataClean(col)
                if isinstance(col, datetime.datetime):
                    pass
                new_cols.append(col)
            new_rows.append(new_cols)
        return new_rows
        
        


    def getTopRowCells(self,table_name,top_rows,cols_list):
        table_name=self.formate_table_name(table_name)

        cursor = self.conn.cursor(as_dict=True)
        
        cols_arry=[]
        for i in cols_list:
            cols_arry.append(self.formate_col_name(i[0]))
        cols=','.join(cols_arry)
        sql=""
        if self.db_type=='MS SQLSERVER':
            sql="select top "+str(top_rows)+" "+cols+" from "+table_name
        if self.db_type=='ORACLE':
            sql="select "+cols+" from "+table_name+ " where rownum<"+str(top_rows)
        print(sql)
        cursor.execute(sql)
        #print(cursor)
        data_cells=[]
        #print("start")
        for row in cursor:
            #print('aaa')
            data_row=[]
            #print(row)
            for index in cols_list:
                col=row[index[0]]
                
                if isinstance(col, str):
                    #print("转换前"+col)
                    col = self.dataClean(col)
                    #print("转换后"+col)
                if isinstance(col, datetime.datetime):
                    pass
                
                data_row.append(col)
            #print(data_row)
            data_cells.append(data_row)
        cursor.close()
        return data_cells

    def dataClean(self,str):
        str=str.replace(chr(10),"")
        str=str.replace(chr(13),"")
        str=str.replace(chr(44),"")
        str=str.replace(chr(34),"")
        str=str.replace(chr(39),"")
        str=str.replace(chr(32),"")
        return str


    def getColumn(self,table_name):

        '''
        select  b.name colName, c.name colType ,c.length colLength

from sysobjects a inner join syscolumns b
on a.id=b.id and a.xtype='U'
inner join systypes c
on b.xtype=c.xusertype
where a.name='03对手为正贵的对公账号的流水信息'
'''
        #table_name=self.formate_table_name(table_name)
        cursor = self.conn.cursor()
        if self.db_type=='MS SQLSERVER':
            cursor.execute("select  b.name colName, c.name colType ,c.length colLength from sysobjects a inner join syscolumns b on a.id=b.id and a.xtype='U' inner join systypes c on b.xtype=c.xusertype where a.name='"+table_name+"' and c.name not in('binary','varbinary','image')")
        if self.db_type=='ORACLE':
            cursor.execute("select  column_name,data_type,data_length,DATA_PRECISION ,DATA_SCALE from all_tab_columns  where table_name=upper('"+table_name+"') and data_type not in('LONG','RAW','LONG RAW','BLOB','CLOB','NCLOB','BFILE','ROWID','NROWID')")
        columns=[]
        try:
            for row in cursor:
                #print('row = %r' % (row,))

                #col有特殊字符，不能导入
                _clean=self.dataClean(row[0])
                #print("之前")
                #print(row[0])
                #print("之后")
                #print(_clean)
                if _clean!=row[0]:
                    raise Exception("字段含有特殊字符，不能导入")
                
                columns.append([row[0],DbTypeToSysType.mssql(row[1])])
        except:
            columns=[]
        finally:
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
        try:
                
            if self.db_type=='MS SQLSERVER':
                self.conn = pymssql.connect(server=self.db_address,port=self.db_port,user=self.db_username,password=self.db_password,database=self.db_name)
            if self.db_type=='ORACLE':
                self.conn =  cx_Oracle.connect(self.db_username, self.db_password,self.db_address+':'+self.db_port+'/'+self.db_name)
        except (pymssql.InterfaceError,pymssql.OperationalError) as e:
            return "Connect Failed:"+str(e)
        except:
            #print("Unexpected error:", sys.exc_info()[0])
            return "Connect Failed:"+sys.exc_info()[0]
        
        else:
            #print("connected ok")
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
        if self.db_type=='ORACLE':
            cursor=self.conn.cursor()
            cursor.execute("select * from v$version")
            version=cursor.fetchone()[0]
            cursor.close()
            return version


