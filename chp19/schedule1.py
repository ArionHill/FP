"""
>>> import shelve
>>> db = shelve.open(DB_NAME)
>>> if CONFERENCE not in db: 
...     load_db(db)
... 
/home/hill/Documents/book/fluent_python/chp19/schedule1.py:16: UserWarning: loading data/schedule1_db
  warnings.warn('loading ' + DB_NAME)
>>> speaker = db['speaker.3471']
>>> type(speaker)
<class 'schedule1.Record'>
>>> speaker.name, speaker.twitter
('Anna Martelli Ravenscroft', 'annaraven')
>>> db.close()
"""
import warnings

import osconfeed

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        # 对象的__dict__属性中存储着对象的属性--前提是类中没有声明__slots__属性.
        # 更新实例的__dict__属性,把值设为一个映射,能快速地在那个实例中创建一堆属性.
        self.__dict__.update(kwargs)


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = Record(**record)