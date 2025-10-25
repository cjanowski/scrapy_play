from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class MtgCard(Base):
    '''
    Database model for MTG cards
    '''
    __tablename__ = 'mtg_cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(String)
    set_name = Column(String)
    price = Column(String)
    condition = Column(String)
    seller = Column(String)
    url = Column(String)
    source = Column(String)
    timestamp = Column(String)
    shipping = Column(String)
    buy_it_now = Column(Boolean)


class MtgScraperPipeline:
    '''
    Pipeline to store scraped items in SQLite database
    '''
    
    def open_spider(self, spider):
        '''
        Initialize database connection when spider opens
        '''
        db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        spider.logger.info(f"Database initialized at: {db_path}")
    
    def close_spider(self, spider):
        '''
        Close database connection when spider closes
        '''
        self.session.commit()
        self.session.close()
        spider.logger.info("Database connection closed")
    
    def process_item(self, item, spider):
        '''
        Process and store each scraped item
        '''
        adapter = ItemAdapter(item)
        
        card = MtgCard(
            card_name=adapter.get('card_name'),
            set_name=adapter.get('set_name'),
            price=adapter.get('price'),
            condition=adapter.get('condition'),
            seller=adapter.get('seller'),
            url=adapter.get('url'),
            source=adapter.get('source'),
            timestamp=adapter.get('timestamp'),
            shipping=adapter.get('shipping'),
            buy_it_now=adapter.get('buy_it_now', False)
        )
        
        self.session.add(card)
        
        return item

