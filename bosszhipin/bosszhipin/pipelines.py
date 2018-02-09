# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

print("这里这里")
class BosszhipinPipeline(object):
    def __init__(self):
        #self.dbpool = dbpool
        dbargs = dict(
            host = 'localhost',
            db = 'Crawl',
            user = 'root',
            passwd = 'jjcheheda',
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    #连接数据库
    ''' @classmethod
    def from_settings(cls, settings):
        dbparams=dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = MYSQLdb.cursors.DictCursor,
            use_unicode = False,
        )
        dppool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)'''
        
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        #query.addErrback(self._handle_error, item, spider)
        return item
    
    #写入数据库
    def _conditional_insert(self, tx, item):
        print("写入数据库")
        sql = "insert into scrapy_boss(pid, positionName, salary, city, workYear, education, companyShortName, industryField, financeStage, companySize, time, updated_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (item["pid"], item["positionName"], item["salary"], item["city"], item["workYear"], item["education"], item["companyShortName"], item["industryField"], item["financeStage"], item["companySize"], item["time"], item["updated_at"])
        tx.execute(sql, params)
    ''' 
    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print("-----------")
        print(failue)'''

#保存到文件中的类 
'''class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('info.json', 'w' ,encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    
    #爬虫结束时关闭文件
    def spider_closed(self, spider):
        self.file.close()'''
       
