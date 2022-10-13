# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter, adapter
from sqlalchemy import create_engine, engine, select
from sqlalchemy.orm import sessionmaker


from .models import Author, Keyword, Quote

class RemoveQuotePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'quote' in adapter.keys():
            adapter['quote'] = adapter['quote'].replace('“','').replace('”','').replace('\n','').strip()
        return item

class AddAuthorToDB():

    def process_item(self, item, spider):
        engine = create_engine('sqlite:///test.db')
        Session = sessionmaker(bind=engine)
        adapter = ItemAdapter(item)
        if 'name' in adapter.keys():
            session = Session()
            a = Author(name= adapter['name'], birthday= datetime.strptime(adapter['birthdate'], '%B %d, %Y' ).date(), bio= adapter['bio'][:149])
            try:
                session.add(a)
                session.commit()
                session.close()
            except:
                session.close()
        return item


class AddKeywordToDB():

    def process_item(self, item, spider):
        engine = create_engine('sqlite:///test.db')
        Session = sessionmaker(bind=engine)
        adapter = ItemAdapter(item)
        if 'keywords' in adapter.keys():
            session = Session()
            for word in adapter['keywords']:
                kw = Keyword(word = word)
                try:
                    session.add(kw)
                    session.commit()
                    session.close()
                except:
                    session.close()
        return item


class AddQuoteToDB():

    def process_item(self, item, spider):
        engine = create_engine('sqlite:///test.db')
        Session = sessionmaker(bind=engine)
        adapter = ItemAdapter(item)
        if 'quote' in adapter.keys():
            session = Session()
            for author in adapter['author']:
                try:
                    a = session.execute(select(Author).where(Author.name == author)).scalar_one()
                    q = Quote(quote= adapter['quote'], author_id = a.id)
                    # for word in adapter['keywords']:
                    kws = session.execute(select(Keyword).where(Keyword.word.in_(adapter['keywords']))).all()
                    # print([kw[0] for kw in kws])
                    q.keywords = [kw[0] for kw in kws]
                    session.add(q)
                    session.commit()
                    session.close()
                except Exception as e:
                    print('Error in AddQuoteDB', e, item)
                    session.close()
        return item