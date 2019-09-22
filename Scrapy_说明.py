a = 1

"""
scrapy startproject AA

在工程目录下
scrapy crawl CocoaChinaSpider




scrapy 支持暂停/恢复功能 (A,B为不同两种)
    开启: JOBDIR  为唯一目录
        A:scrapy crawl somespider -s JOBDIR=crawls/somespider-1
        B:(  setting.py
            JOBDIR='sharejs.com'
            scrapy crawl somespider
            )
    暂停:
        ctrl+c终止采集程序的运行
    再次开启
       A: scrapy crawl somespider -s JOBDIR=crawls/somespider-1

       B: (
            scrapy crawl somespider
          )

开启多个spider
    A:多次调用  scrapy crawl XXX

    B: 脚本
    单个
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings
        process = CrawlerProcess(get_project_settings())
        process.crawl('AVTBSpider')
        process.start()
    多个
        import scrapy
        from scrapy.crawler import CrawlerProcess
        class MySpider1(scrapy.Spider):
            pass
        class MySpider2(scrapy.Spider):
            pass
        process = CrawlerProcess()
        process.crawl(MySpider1)
        process.crawl(MySpider2)
        process.start()
    C:
        1:在工程下创建 commands目录  与spiders同级
        2:添加 __init__.py
        3:添加一个文件crawlall.py    示例:  https://github.com/scrapy/scrapy/blob/master/scrapy/commands/crawl.py
        4:settings  COMMANDS_MODULE = 'APP_NAME.commands'
        5: 运行命令scrapy crawlall

"""

"""
1:Item 为数据的容器 你爬取的数据装载
    类似字典   读取 item["A"] /item["A"]=2121
        dict(item)   /  Item(**{}) 字典直接初始化
        item.fileds    --->{"name":{一定是空字典}....}
        keys()         ---->["name","age"]  有值得属性集合
        items()       ----->{"name":"AA","age":1} 有值得属性集合
    class CocoaChinaItem(Item):
        name =  Filed()   //Filed()  可以保存任意类型的值
        percent = scrapy.Field(serializer=str)   指定保存的类型


        扩展  (该必须结合ItemLoader才会生效)

            from scrapy.loader.processors import MapCompose,Compose,TakeFirst,Identity,Join
            都是对Filed() 值进行附加操作的
            Identity:不多任何操作
            TakeFirst:取数组的第一个非空的值   -> 得到单个值
            Join : 有一个分割参数  表示对数组进行 join操作  "spre".join(arr)   -> 得到单个值

            Compose:  指定多个函数/表达式  Compose(Func1,Func2)
                    Value   Func1(Value)-> Value2 --> Func2(Value2)--> Value3

            MapCompose:指定多个函数/表达式 MapCompose(Func1,Func2)
                    Value [1,2,3] --> 遍历Value -> 调用Func1(one) --> Value1[1,2,3]
                    遍历Value1 -> 调用Func2(one) -->得到最后结果Value2[]




            自定义自己的处理
                class MyDeal(object):
                    def __init__(self,...)
                        接受参数,该方法是可选的
                    def  __call__(self,value..):
                        value是必须的 数组 其他参数自定义
                        过程自己根据需求而定
    example:
     手动处理Item
        class CocoaChinaItem(Item):
            name = scrapy.Field(
                        input_processor=MapCompose(func1,func2),  设置值得时候调用
                        output_processor=Join()                   取值的时候调用
                        )
    动态创建Item
        from scrapy.item import DictItem, Field
        def create_item_class(class_name, field_list):
            fields = {field_name: Field() for field_name in field_list}
            return type(class_name, (DictItem,), {'fields': fields})



2:Selector
    使用最Selector 就可
    def __init__(self, response=None, text=None, type=None, root=None, _root=None, **kwargs):
        text 说明可以对本地文件进行解析
    sel.xpath()
    sel.css()
    sel.re()  得到()适配的内容


3:Request

     scrapy.Request     包装请求
        def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None):
            url:
            callback:请求回调  必须为self.func
            cookies : [{}...] /  {"name":1212....}
                    可以浏览器登入后 手动获取
            meta :  request/resopnse中 可以为包含任何值 下面是scrpy 认可的
                    dont_redirect
                    dont_retry
                    handle_httpstatus_list
                    dont_merge_cookies (see cookies parameter of Request constructor)
                    cookiejar
                    redirect_urls
                    bindaddress

    scrapy.FormRequest  对表单处理的Request
        1:使用from_response类方法创建
        2:参数和Request一致
          增加:formname (string)   指定form 名称
              formxpath (string)  指定标签 并第一个表单被使用
              formcss
              formnumber (integer) 第几个表单被使用 默认为0
              formid              指定表单的ID
              formdata= { },      指定 参数值
              clickdata={},
              dont_click=False,   If True, the form data will be submitted without clicking in any element.



4:Spider 为指定的爬虫基类 必须继承  from scrapy.spider import BaseSpider
    {
        Spider 只是对start_urls进行爬取
    }

    属性:
        name             为唯一必要属性
        allowed_domains  包含spider容许爬取的域名
        start_urls   URL列表
        download_delay :延迟

    方法:
        def start_request()
            1:该方法为可选的  只会调用一次 你要为其创建生成器/或者返回数组
            2:start_request() 和属性 start_urls 都是为提供URL
            3:默认使用列表start_urls  生成Request
            4:你可以在登入某个网站
                def start_requests(self):
                    return [scrapy.FormRequest("http://www.example.com/login",
                               formdata={'user': 'john', 'pass': 'secret'},
                               callback=self.logged_in)]
                def logged_in(self, response):
                    pass

        def parse(response):
            1:这是解析默认的回调方法
            2:parse 负责处理response并返回处理的数据  (Item)  以及(/或)跟进的URL
                1:手动打印结果...
                2:返回item生成器/数组
                3:返回Request对象 生成器/数组  指定解析器  callback = "parse_item"
                  Request 为下载下一页面的请求  callback 为解析下一页面请求
                  (parse_item 可以再返回请求 继续下一页的请求。。。。。)
                    def parse(self, response):
                        sel = Selector(response)
                        item = CsdnblogItem()
                        yield item        最初返回item
                        urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()
                        for url in urls:
                            yield Request(url, callback=self.parse)
                            
        def make_requests_from_url(url)----->Request
        Scrapy.Request()


5:CalrmSpider
    name     :   唯一标示
	download_delay :延迟
	start_urls   : 网页
	rules:[
		Rule(LinkExtractor(restrict_xpaths="//a]")，callback follow)  解析首地址  得到跟进url1
		Rule(1),                                                      加载url1   解析跟进地址 。。。
		Rule(2)
	]
	0,1,2 表示对某个网页的连接的过滤

	---> 如果不指定callback  会调用默认的解析方法  匹配出来的网址作为下一页的链接 并且跟进
	---> 指定 就会自己处理 follow默认是为false
	---> 第一个为解析首页
	     第二个则是解析 跟进的网页
    ---> 如果最后一个Rule 也跟进follow=true 那就就会作为下一页一直跟进

    LinkExtractor   /  SgmlLinkExtractor
		allow   选定URL给定正则表达式
		deny  	这个正则表达式 不匹配的URL必须被排除在外(即不提取)｡它的优先级高于 allow 的参数
		allow_domains  容许的域名  ["example.com"]或str
		deny_domains
		deny_extensions  提取连接时 忽略的扩展  ["pho"...]
		restrict_xpaths   xpath或者xpath列表  选定区域 与allow共同构成filter
		tags (str or list) – 提取链接时要考虑的标记或标记列表｡默认为 ( 'a' , 'area') ｡
		attrs (list) – 提取链接时应该寻找的attrbitues列表(仅在 tag 参数中指定的标签)｡默认为 ('href')｡
		unique (boolean) – 重复过滤是否应适用于提取的链接｡

    Rule:
	   def __init__(self, link_extractor, callback=None, cb_kwargs=None,follow=None, process_links=None, process_request=identity):
		link_extractor:上面Link过滤对象
		callback  : 为回调对象 (一般都要指定 ) 字符串方法名即可

		follow   :指定更具规则得到的连接对象 是否跟进 callback为None时 默认为true

		process_request:是一个callable或string(该spider中同名的函数将会被调用)。 该规则提取到每个request时都会调用该函数。该函数必须返回一个request或者None。 (用来过滤request)
		        process_request ="add_cookie" 在请求完成后会回调函数
				def add_cookie(self, request):
					request.replace(cookies=[
							{'name': 'COOKIE_NAME','value': 'VALUE','domain': '.douban.com','path': '/'},
							]);
				return request
		cb_kwargs: 为回调传递其余参数
		process_links:""  spider同名函数会被调用(在获取链接后调用 主要用于过滤链接)


exam：
    指定初始页       MM-home
    指定rules=[
        RULE(path,callback="tags_url",follow=True)   解析首页 得到跟进的网址  follow 为True 第二个Rule 才会生效
        RUle(1,call="tag_one_url",follow=..)                   解析 更新的网址
    ]

    可 选 重写的方法 def parse_start_url(self,response)   用于爬取起始页面
                            MM-home

    def  tags_url(self,response):
        这里就是解析Rule(0)解析 网址

    def  tag_one_url(self,response)
            第二个Rule解析的网址页面



6:ItemLoader
    from scrapy.loader import ItemLoader
    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
    使用item = CocoaChinaItem() ,resopnse=res  /  selector =  手动截取的Selector( 在这种情况下 必须使用  .//  ./ 等表示当前selector)

    l.add_xpath('name', xpath2) # (2)
    l.add_css('name', css) # (3)
    l.add_value('name', 'test') # (4)
    example:
        for index in range(len(lists)):
            one = lists[index]
            il =  ItemLoader(item=CocoaChinaItem(),selector=one)
            il.add_xpath("name",".//div[@class='clearfix newstitle']/a/text()")
            il.add_xpath("thumbText",".//div[@class='newsinfor']/text()")
            il.add_xpath("time",".//div[@class='clearfix zx_manage']/div[@class='float-l']/span[1]/text()")
            il.add_xpath("category",".//div[@class='clearfix zx_manage']/div[@class='float-l']/span[2]/text()")
            il.add_xpath("source", ".//div[@class='clearfix zx_manage']/div[@class='float-l']/span[3]/text()")
            il.add_value('test',[1,23,4])
            items.append(il.load_item())

    注意这里 使用  .//div[@class='clearfix newstitle']/a[1]/text()/ 得到的item 的 name 属性 也是数组

    结合 Item 扩展来处理结果


7:pipline
    通过setting 里面的配置 将多个管道连接
        item------->----(或者被抛弃)----->------->
        管道1=======管道2=========管道三.......

        管道类都有特定的方法处理过滤Item

    item pipeline简单的类即可
    1:process_item(item, spider) 必须实现的方法  当spider返回item时就会调用
      必须返回item /DropItem错误   如果对自己的item进行筛选 或者抛出错误
    2:open_spider(spider)/close_spider(spider)可选

>>>  文件下载管道
>>>  pipline图片管道
    1:编写Item
        class imageItem(Item):
            image_urls=Field()   必须
            images = scrapy.Field() 必须
            .......
    2:激活下载管道 使用默认
        ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
    3:指定下载路径
        IMAGES_STORE = 'path'
    额外配置
        有效性
            IMAGES_EXPIRES = 90  为保证不重复(90不会重复)
        缩略图生成
            IMAGES_THUMBS = {
                'small': (50, 50),
                'big': (270, 270),
            }
        过滤图片大小
            IMAGES_MIN_HEIGHT = 110
            IMAGES_MIN_WIDTH = 110



    自定义图片管道
        import scrapy
        from scrapy.contrib.pipeline.images import ImagesPipeline
        from scrapy.exceptions import DropItem

        class MyImagesPipeline(ImagesPipeline):
            "
              item:对于自定义Item
              info: 保存着一些下载信息 from scrapy.pipelines.media import MediaPipeline
              如果放弃该item   抛出异常 DropItem("Item contains no images")
            "
            def get_media_requests(self, item, info):
                for image_url in item['image_urls']:
                yield scrapy.Request(image_url)
            "
                一个item完成 后调用
                result保存了item中图片下载信息 （,）
                result保存了item中图片下载信息
                默认返回item 进入下一个管道
            "
            def item_completed(self, results, item, info):
                raise DropItem("sasasa")
                return item


8:下载中间件
    Request 通过中间件 到达下载器
    Response 通过中间件 达到Scrapy引擎  然后在进行回调解析


    Request
    引擎-----|------------|---------------|--------------|--------------------->下载器

         中间| 件1     中间| 件2       中间 |件3     自定义| 中间件      (顺序根据配置而定)
            |             |               |             |
        ----|-------------|---------------|-------------|--------------------->process_request(request, spider)
            |             |               |             |
            |             |           异常|处理          |                       process_exception(request, exception, spider)
            |             |               |             |
        <---|-------------|---------------|-------------|----------------------process_response(request, response, spider)

                                                                              Response




    激活自己的中间件(会与系统默认的合并)  根据顺序排序
     DOWNLOADER_MIDDLEWARES = {
        'myproject.middlewares.CustomDownloaderMiddleware': 543,  顺序
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,  取消系统中间件
     }
    class scrapy.contrib.downloadermiddleware.DownloaderMiddleware
        1:process_request(request, spider)
            必须返回其中之一:
                返回 None 、             继续处理request
                返回一个 Response 对象、  Scrapy将不会调用其他中间件该方法  而是返回调用中间件的process_response()
                返回一个 Request 对象     终止中间件调用 重新请求request
                raise IgnoreRequest 。 则安装的下载中间件的 process_exception() 方法会被调用

        2:process_response(request, response, spider)
            必须返回
                返回一个 Response 对象、      可以与传入的response相同，也可以是全新的对象
                返回一个 Request 对象          重新开始请求
                raise一个 IgnoreRequest 异常。 则安装的下载中间件的 process_exception() 方法会被调用

        3:process_exception(request, exception, spider)
            当中间件发送异常会调用
            必须返回
                返回 None 、       Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception() 方法
                Response 对象、    已安装的中间件链的 process_response() 方法被调用  不会调用其他异常处理方法
                Request 对象。     则返回的request将会被重新调用下载。

9:Spider中间件
Spider-----|--------------|---------------|------------|--------------------->引擎
         中间| 件1     中间| 件2       中间 |件3     自定义|中间件                      (顺序根据配置而定)
            |             |               |             |
        ----|-------------|---------------|-------------|--------------------->spider 解析放回request    process_start_requests(start_requests, spider)
            |             |               |             |                       spider 解析返回item 调用  process_spider_output(response, result, spider)
            |             |           异常|处理          |
            |             |               |             |
        <---|-------------|---------------|-------------|---------------------- resopnse 下发到spider 调用 process_spider_input(response, spider)



    激活自己的中间件(会与系统默认的合并)  根据顺序排序
        SPIDER_MIDDLEWARES = {
          'myproject.middlewares.CustomSpiderMiddleware': 543,
          'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
        }

    编写您自己的spider中间件
        scrapy.contrib.spidermiddleware.SpiderMiddleware
            1:def process_start_requests(self,start_requests, spider)
                该方法以spider 启动的request为参数被调用
                必须返回request
            2:def process_spider_input(self,response, spider)
                当response通过spider中间件时
                应该返回 None  继续下一个中间件处理
                或者抛出一个异常
            3:def process_spider_output(self,response, result, spider)
                当Spider处理response返回result时，该方法被调用
                必须返回包含 Request 、dict 或 Item 对象的可迭代对象(iterable)。

            4:def process_spider_exception(self,response, exception, spider)
                当spider或(其他spider中间件的) process_spider_input() 跑出异常时
                必须要么返回 None ，    继续异常处理
                返回一个包含 Response 、dict 或 Item 对象的可迭代对象(iterable)。
                    中间件链的 process_spider_output() 方法被调用
                    异常处理停止

10:扩展 扩展框架提供一个机制，使得你能将自定义功能绑定到Scrapy。
    http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/extensions.html

11:核心API

    该节文档讲述Scrapy核心API，目标用户是开发Scrapy扩展(extensions)和中间件(middlewares)的开发人员。

12:信号(Signals)

    Scrapy使用信号来通知事情发生。您可以在您的Scrapy项目中捕捉一些信号(使用 extension)来完成额外的工作或添加额外的功能，扩展Scrapy。

"""
"""
                        setting


请求头:
DEFAULT_REQUEST_HEADERS = {
    'accept': 'image/webp,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}

ROBOTSTXT_OBEY=True 默认
    Forbidden by robots.txt 访问拒绝
    因为默认scrapy遵守robot协议，所以会先请求这个文件查看自己的权限
    设置为False 就可解决

管道设置
ITEM_PIPELINES ={
        'myApp.pipelines.CocoaDB':300,  指向你的类  整形值是确定其运行顺序
            0----1000 表示你的item 依次执行对应的 pipelines

        }

全局并发数
CONCURRENT_REQUESTS = 100   调试 选择CPU 80%-90%的并发数
关闭重定向
REDIRECT_ENABLED = False

禁止cookies  如果不需要cookies请关闭
COOKIES_ENABLED = False

禁止对失败的http重试
RETRY_ENABLED = False


减小下载超时
DOWNLOAD_TIMEOUT = 15

关闭重定向
REDIRECT_ENABLED = False


自动下载限速
    AUTOTHROTTLE_ENABLED   开启关闭
    AUTOTHROTTLE_START_DELAY  初始下载延迟(单位:秒)。 5.0
    AUTOTHROTTLE_MAX_DELAY    在高延迟情况下最大的下载延迟(单位秒)。 60.0
    AUTOTHROTTLE_DEBUG                                     False
    DOWNLOAD_DELAY

"""

"""
                                 数据保存
    http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/exporters.html
一:
 1: 创建数据库(utf-8)  表
 2:pipelines
    一般:
        1:创建类继承object即可
        2:创建数据库链接
        3:def process_item(self, item, spider):
          重写该方法 以便调用
        4:创建函数 插入数据库
        5: def close_spider(self, *args, **kwargs):
    自定义:
        1:创建类继承object即可
        2:创建数据库链接
        3:def process_item(self, item, spider):
            保存数据库即可
        4:def close_spider(self, *args, **kwargs):
3:setting
    ITEM_PIPELINES ={
        'myApp.pipelines.CocoaDB':300,  指向你的类
            0----1000 表示你的item 依次执行对于的 pipelines
        }


                  保存到json文件
二:
    1:pipelines 创建并打开文件
    2:def process_item(self, item, spider):
        吧文件写入
    3:setting 指定

三:
    不用编写 pipelines
    scrapy crawl spiderName -o jsonFileName -t json


四:                CVS
                百度即可

   本地文件系统、FTP、S3 (Feed exports)// http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/feed-exports.html



"""

"""
                       数据收集(Stats Collection)
http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/stats.html#topics-stats-usecases
"""

"""
                            发送email
http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/email.html
"""

"""
                            Telnet终端(Telnet Console)
"""

"""
                            调试

    1:Scrapy终端(Shell)
    2:Scrapy终端(Shell)
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
    3:Logging

                            任务的暂停继续


    一个把调度请求保存在磁盘的调度器
    一个把访问请求保存在磁盘的副本过滤器[duplicates filter]
    一个能持续保持爬虫状态(键/值对)的扩展

    保存配置路径:
        不能被不同spider共享   同一个spider的不同jobs/runs也不行

    开启:
        scrapy crawl name -s JOBDIR=crawls/name-1
    暂停:
        Ctrl-C或者发送一个信号
        等待一些请求完成
        再次Ctrl-C 暂停

    继续:
        scrapy crawl name -s JOBDIR=crawls/name-1 接着之前的任务
        scrapy crawl name -s JOBDIR=crawls/name-2 再次重新开启

"""

import scrapy
from scrapy.selector import Selector
from scrapy import Item, Field
from scrapy.spiders import BaseSpider, Spider, CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.loader.processors import TakeFirst
from scrapy.contrib.linkextractors import LinkExtractor
