
from database.orm import Base,Column,String,Integer

class SystemCode(Base):
    __tablename__ = "system_code"
    code_main = Column(String(64), primary_key=True)
    code_desc = Column(String(256))
    code_code = Column(String(128), primary_key=True, unique=True)
    code_value = Column(String(1024))
    code_type = Column(Integer)  # 1为数字2为文本3为日期4为日期时间（含毫秒）

    def to_json(self):
        json_string = {
            'code_main': self.code_main,
            'code_desc': self.code_desc,
            'code_code': self.code_code,
            'code_value': self.code_value,
            'code_type': self.code_type,

        }
        return json_string

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemCode).delete()

    def saveOfUpdate(self, session):
        db_data = session.query(SystemCode).filter(
            SystemCode.code_main == self.code_main, SystemCode.code_code == self.code_code).one_or_none()
        if db_data == None:
            session.add(self)
        else:
            db_data.code_desc = self.code_desc
            db_data.code_value = self.code_value
            db_data.f_trade = self.f_trade
            db_data.code_type = self.code_type
