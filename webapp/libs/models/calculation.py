from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, Boolean, Text, DateTime, Float, LargeBinary
from sqlalchemy.orm import relationship
import sqlalchemy
import datetime


Base = declarative_base()


class Calculation(Base):
    """ Вычисления """
    __tablename__ = 'calculation'
    id = Column('calculation_id', Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text())
    params_template = Column(Text())
    updated = Column(DateTime, onupdate=datetime.datetime.now)
    graphs = relationship('Graph', order_by='desc(Graph.created)', cascade='all, delete-orphan')

    def __init__(self, title, description, params_template):
        Base.__init__(self)
        self.title = title
        self.description = description
        self.params_template = params_template

    def href(self):
        if self.id and self.id == 2:
            return '/calculation/item_points/?calculation_id=%s' % self.id
        elif self.id and self.id == 3:
            return '/calculation/item_images/?calculation_id=%s' % self.id
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
    __tablename__ = 'graph'
    id = Column('graph_id', Integer, primary_key=True)
    calculation_id = Column(Integer, ForeignKey('calculation.calculation_id'), nullable=False)
    title = Column(String(255), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now)
    finished = Column(Boolean, default=False)
    params = Column(Text, nullable=False)
    data = relationship('Data', order_by='Data.point_x, Data.created', cascade='delete', lazy='select')

    def __init__(self, calculation_id, title, params):
        Base.__init__(self)
        self.calculation_id = calculation_id
        self.title = title
        self.params = params
        self.finished = False

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
            except sqlalchemy.exc.InvalidRequestError:
                pass
        return r

    def last_image(self, session):
        r = None
        if self.id:
            r = session.query(Data) \
                .filter(Data.graph_id == self.id) \
                .order_by(Data.created.desc()) \
                .first()
        return r


class Data(Base):
    """ Данные для графика. Могут быть двух типов: Point и Image. """
    __tablename__ = 'data'
    id = Column('data_id', Integer, primary_key=True)
    graph_id = Column(Integer, ForeignKey('graph.graph_id'), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)

    # Point
    point_x = Column(Float)
    point_y = Column(Float)

    # Image
    image_width = Column(Integer)
    image_height = Column(Integer)

    def __init__(self, graph_id,
                 point_x=None, point_y=None,
                 image_width=None, image_height=None):
        Base.__init__(self)
        # TODO: Need to verify data types and constraints
        self.graph_id = graph_id
        self.point_x = point_x
        self.point_y = point_y
        self.image_width = image_width
        self.image_height = image_height

    def is_image(self):
        return self.image_width and self.image_height

    def href(self):
        return '/calculation/graph_image/?data_id=%s' % self.id if self.is_image() else None

    @staticmethod
    def list(session, graph_id):
        r = None
        if graph_id:
            # Точки сортируем по x, картинки по created
            r = session.query(Data)\
                .filter(Data.graph_id == graph_id) \
                .order_by(Data.point_x, Data.created)\
                .all()
        return r

    @staticmethod
    def get(session, data_id):
        r = None
        if data_id:
            try:
                r = session.query(Data).get(data_id)
            except sqlalchemy.exc.InvalidRequestError:
                pass
        return r
