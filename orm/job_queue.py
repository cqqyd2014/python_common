import json


from python_common.common import DateTimeEncoder
from database.orm import Base,Column,String,Integer,Text,DateTime,Boolean

# 任务列表
class JobQueue(Base):
    __tablename__ = "job_queue"
    u_uuid = Column(String(37), primary_key=True)
    u_declare_key = Column(String(256))  # download_data从远程数据库下载数据
    u_body = Column(Text)
    u_publisher_id = Column(String(256))
    u_publish_datetime = Column(DateTime)
    u_no_ack = Column(Boolean)  # 为True的情况，消息一旦接受就认为结束，为False的情况消息需要客户端确认处理完成才结束。
    u_start_datetime = Column(DateTime)  # 开始处理时间
    u_complete_datetime = Column(DateTime)  # 结束处理时间
    u_status = Column(String(16))  # 发布，处理中，处理完成
    u_back_message=Column(Text)

    @staticmethod
    def delete_all(db_session):
        db_session.query(JobQueue).delete()

    def __repr__(self):
        return self.u_uuid+self.u_declare_key+self.u_body

    def to_json(self):
        json_string = {
            'u_uuid': self.u_uuid,
            'u_declare_key': self.u_declare_key,
            'u_body': self.u_body,
            'u_publish_datetime': json.dumps(self.u_publish_datetime, cls=DateTimeEncoder),
            'u_no_ack': self.u_no_ack,
            'u_publisher_id': self.u_publisher_id,
            'u_complete_date': json.dumps(self.u_complete_datetime, cls=DateTimeEncoder),
            'u_status': self.u_status,
            'u_start_datetime': json.dumps(self.u_start_datetime, cls=DateTimeEncoder),
            'u_back_message':self.u_back_message




        }
        return json_string