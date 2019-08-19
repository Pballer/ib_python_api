"""Database models for market data."""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class TickMarketData(Base):
    __tablename__ = 'tick_market_data'

    tickerid = Column(Integer, primary_key=True)
    insert_date = Column(DateTime)
    ticktype = Column(String)
    value = Column(Float)

    def __repr__(self):
        return "<TickMarketData(tickerid='%s', insert_date='%s', ticktype='%s', value='%s')>" % (
                    self.tickerid, self.insert_date, self.ticktype, self.value)


if __name__ == '__main__':
    import datetime
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    mktData = TickMarketData(tickerid=1, insert_date=datetime.datetime.now(), ticktype='BID', value=5.23)
    session.add(mktData)
    session.commit()

    results = session.query(TickMarketData).filter(TickMarketData.tickerid == 1).all()
    print('Query results:', results)
