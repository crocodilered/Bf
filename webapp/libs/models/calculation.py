from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, Boolean, Text, DateTime, Float
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()


class Calculation(Base):
    """ Вычисления """

    __tablename__ = "calculation"
    id = Column('calculation_id', Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text())
    params_template = Column(Text())
    updated = Column(DateTime, onupdate=datetime.datetime.now)
    graphs = relationship("Graph", order_by="desc(Graph.created)", cascade="all, delete-orphan")

    def __init__(self, title, description, params_template):
        Base.__init__(self)
        self.title = title
        self.description = description
        self.params_template = params_template

    def href(self):
        if self.id:
            return "/calculation/c/?calculation_id=%s" % self.id
        else:
            return None

    @staticmethod
    def list(session):
        q = session.query(Calculation)
        return q.order_by(Calculation.title).all()

    @staticmethod
    def get(session, id):
        r = None
        if id:
            try:
                r = session.query(Calculation).get(id)
            except:
                pass
        return r


class Graph(Base):
    """ График """

    __tablename__ = "graph"
    id = Column("graph_id", Integer, primary_key=True)
    calculation_id = Column(Integer, ForeignKey("calculation.calculation_id"), nullable=False)
    title = Column(String(255), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now)
    finished = Column(Boolean, default=False)
    params = Column(Text, nullable=False)
    data = relationship("Data", order_by="Data.x", cascade="all, delete-orphan")

    def __init__(self, calculation_id, title, params):
        Base.__init__(self)
        self.calculation_id = calculation_id
        self.title = title
        self.params = params
        self.finished = False

    def href(self):
        return "/calculation/g/?graph_id=%s" % self.id

    @staticmethod
    def list(session, calculation_id):
        r = None
        if calculation_id:
            q = session.query(Graph)\
                .filter(Graph.calculation_id == calculation_id) \
                .order_by(Graph.created.desc())
            r = q.all()
        return r

    @staticmethod
    def get(session, id):
        r = None
        if id:
            try:
                r = session.query(Graph).get(id)
            except:
                pass
        return r


class Data(Base):

    __tablename__ = "data"
    id = Column("data_id", Integer, primary_key=True)
    graph_id = Column(Integer, ForeignKey('graph.graph_id'), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, graph_id, x, y):
        Base.__init__(self)
        self.graph_id = graph_id
        self.x = x
        self.y = y

    @staticmethod
    def list(session, graph_id):
        r = None
        if graph_id:
            r = session.query(Data)\
                .filter(Data.graph_id == graph_id) \
                .order_by(Data.x)\
                .all()
        return r
