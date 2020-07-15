'''
@Description: 
@Author: ashen23
@LastEditTime: 2020-07-15 10:30:48
@FilePath: /faker/utils/models.py
@Copyright: © 2020 Ashen23. All rights reserved.
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///config/faker.db?check_same_thread=False')
# engine是2.2中创建的连接
Session = sessionmaker(bind=engine)
# 创建Session类实例
fakerSession = Session()

# 接口参数表
class UrlParamModel(Base):
    __tablename__ = 'parameter'

    id = Column(Integer, primary_key=True)
    value = Column(String(50)) # 参数内容

    url_id = Column(Integer, ForeignKey("urlInfo.id"))
    url = relationship('UrlModel',backref='params')

# 接口信息表
class UrlModel(Base):
    __tablename__ = 'urlInfo'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    url = Column(Text)
    method = Column(String(20))

    param = Column(String(50))
    paramType = Column(String(50))

    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship('GroupModel',backref='urls')

    def toDict(self):
        baseArg = {c.name: getattr(self,c.name, None) for c in self.__table__.columns}
        return dict(baseArg)

# 接口分组表
class GroupModel(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)

    name = Column(String(30))
    icon = Column(String(30))
    desc = Column(String(100))
    baseUrl = Column(String(100))

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship('ProjectModel',backref='groups')

    def toDict(self):
        baseArg = {c.name: getattr(self,c.name, None) for c in self.__table__.columns}
        return dict(baseArg)

# 项目表
class ProjectModel(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    desc = Column(String(100))


def initData():
    Base.metadata.create_all(engine)