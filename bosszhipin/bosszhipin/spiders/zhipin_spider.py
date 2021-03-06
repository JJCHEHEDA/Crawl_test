#-*- coding:utf-8 -*-

import scrapy
import time
from bosszhipin.items import BosszhipinItem

class ZhipinSpider(scrapy.Spider):
    name = 'bosszhipin'

    allowed_domains = ['www.zhipin.com']
    positionUrl = 'http://www.zhipin.com/c101020100/h_101020100/?query=php'
    curPage = 1
    
    headers = {
        'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43\
c0-aad4-37fce8e3ff39",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleW\
ebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,imag\
e/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
        'cache-control': "no-cache",
        'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
        }

                                                                      
    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
# with open('php.txt', 'w') as f:
#            f.write(str(response.body))
        print("request -> " + response.url)
        job_list = response.css('div.job-list > ul > li')
        for job in job_list:
            item = BosszhipinItem()
            job_primary = job.css('div.job-primary')
            item['pid'] = job.css(
                'div.info-primary > h3 > a::attr(data-jobid)').extract_first()
            item["positionName"] = job_primary.css('div.info-primary > h3 > a > div.job-title::text').extract_first()
            item["salary"] = job_primary.css('div.info-primary > h3 > a > span::text').extract_first()
            info_primary = job_primary.css('div.info-primary > p::text').extract()
            item['city'] = info_primary[0].strip()
            item['workYear'] = info_primary[1].strip()
            item['education'] = info_primary[2].strip()
            item['companyShortName'] = job_primary.css('div.info-company > div.company-text > h3 > a::text').extract_first().strip()
            company_infos = job_primary.css('div.info-company > div.company-text > p::text').extract()
            if len(company_infos) == 3:
                item['industryField'] = company_infos[0]
                item['financeStage'] = company_infos[1]
                item['companySize'] = company_infos[2]
            item['time'] = job_primary.css('div.info-publis > p::text').extract_first()
            item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield item

        self.curPage += 1
        if (self.curPage > 1):
            return
        time.sleep(5) 
        yield self.next_request()
                                                                        
    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl + ("&page=%d&ka=page-%d" %
                                 (self.curPage, self.curPage)),
            headers = self.headers,
            callback = self.parse)
