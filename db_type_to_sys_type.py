
class DbTypeToSysType:
    @staticmethod
    def oracle(par):
        if par=="VARCHAR2":
            return 'string'
        if par=="CHAR":
            return 'string'
        if par=="NCHAR":
            return 'string'
        if par=="NVARCHAR2":
            return 'string'
        if par=="DATE":
            return 'string'
        if par=="LONG":
            return 'string'
        if par=="NUMBER":
            return 'float'
        if par=="DECIMAL":
            return 'float'
        if par=="INTEGER":
            return 'long'
        if par=="FLOAT":
            return 'float'
        if par=="REAL":
            return 'float'

    @staticmethod
    def mssql(par):
        if par == 'datetime':
            return 'string'
        elif par == 'varchar':
            return 'string'
        elif par == 'decimal':
            return 'float'
        elif par == 'nvarchar':
            return 'string'
        elif par == 'smallint':
            return 'long'
        elif par == 'int':
            return 'long'
        elif par == 'char':
            return 'string'
        elif par == 'bit':
            return 'long'
        elif par == 'tinyint':
            return 'long'
        elif par == 'numeric':
            return 'float'
        elif par == 'float':
            return 'float'
        elif par == 'real':
            return 'float'
        elif par == 'smalldatetime':
            return 'string'
        elif par == 'text':
            return 'string'
        elif par == 'nchar':
            return 'string'
        elif par == 'ntext':
            return 'string'
        elif par == 'timestamp':
            return 'string'
        elif par == 'uniqueidentifier':
            return 'string'
