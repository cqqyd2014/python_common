
class DbTypeToSysType:
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

            


            

            


            

            


            
    
    @staticmethod
    def oracle(par):
        if par == 'datetime':
            return 'DateTime'
        elif par == 'varchar':
            return 'Text'
        elif par == 'decimal':
            return 'Float'
    
