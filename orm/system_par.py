from database.orm import Base,Column,String,Integer


class SystemPar(Base):
    __tablename__ = "system_par"
    par_code = Column(String(64), primary_key=True)
    par_desc = Column(String(128))
    par_value = Column(String(1024))
    par_type = Column(Integer)  # 1为数字2为文本3为日期4为日期时间（含毫秒）

    @staticmethod
    def delete_all(db_session):
        db_session.query(SystemPar).delete()

    @staticmethod
    def get_value(db_session,par_code):
        db_data=db_session.query(SystemPar).filter(SystemPar.par_code==par_code).one_or_none()
        if db_data==None:
            return None
        else:
            return db_data.par_value

    def __repr__(self):
        return self.par_code+"_"+self.par_value

    def to_json(self):
        json_string = {
            'par_code': self.par_code,
            'par_desc': self.par_desc,
            'par_value': self.par_value,
            'par_type': self.par_type

        }
        return json_string

    @staticmethod
    def from_json(json_string):
        return SystemPar(par_code=json_string.get('par_code'), par_desc=json_string.get('par_desc'), par_value=json_string.get('par_value'), par_type=json_string.get('par_type'))
