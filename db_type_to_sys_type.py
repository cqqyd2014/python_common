
class DbTypeToSysType:
    @staticmethod
    def mssql(par):
        print(par)
        if par == 'datetime':
            return 'DateTime'
        elif par == 'varchar':
            return 'Text'
        elif par == 'decimal':
            return 'Float'
        elif par == 'nvarchar':
            return 'Text'
        elif par == 'smallint':
            return 'Int'
        elif par == 'int':
            return 'Int'
        elif par == 'char':
            return 'Text'
        elif par == 'bit':
            return 'Int'
        elif par == 'tinyint':
            return 'Int'
        elif par == 'numeric':
            return 'Float'
        elif par == 'float':
            return 'Float'
        elif par == 'real':
            return 'Float'
        elif par == 'smalldatetime':
            return 'Date'
        elif par == 'text':
            return 'Text'
        elif par == 'nchar':
            return 'Text'
        elif par == 'ntext':
            return 'Text'
        elif par == 'timestamp':
            return 'Text'
        elif par == 'uniqueidentifier':
            return 'Text'

            


            

            


            

            


            
    
    @staticmethod
    def oracle(par):
        if par == 'datetime':
            return 'DateTime'
        elif par == 'varchar':
            return 'Text'
        elif par == 'decimal':
            return 'Float'
    
