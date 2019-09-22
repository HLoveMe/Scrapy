
import scrapy
from scrapy.selector import Selector
from scrapy import Item, Field
from scrapy.spiders import BaseSpider, Spider, CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.loader.processors import TakeFirst
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse
from scrapy.loader.processors import MapCompose,Compose,TakeFirst,Identity,Join
from scrapy.signals import *
from scrapy.xlib.pydispatch import dispatcher

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.regex import RegexLinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
"""
    创建Scrapy流程
    爬虫类的编写
    数据解析
    Request
    Item
    ItemLoader
    piplines
        扩展Piplines 持久化工具 快速保存到json、csv、XML
    模拟用户登入
    中间件
    数据收集器
    限速：
    DjangiItem:
    信号
    CoreAPI
    扩展功能
    任务的开启 暂停
    Error:错误

    setting 配置
    css选择器
    url拼接
    html tag 移除
    PipeLines / Spider / Middleware创建
    反爬虫
    验证码识别
    动态页面爬取
    URL去重
    Telnet终端：
"""

"""
    1:创建Scrapy (scrapy startproject ScrapyName)
        {
            items 处理数据模型
            middlewares 中间件
            piplines  处理数据存储
            settings scrapy配置
            spiders 为爬虫路径
                {
                    __init.py
                    Name.py 这是一个爬虫文件
                }
        }
    2:创建爬虫
        > scrapy genspider  Name startURLSTR
        > scrapy genspider -t crawl XXX  URL
        > 直接在spiders 创建python Name.py 继承集体的Spider类
        >

    3:运行
        》在工程目录下 命令行： scrapy crawl 爬虫名称
        》建立start.py 快速启动  支持Pycharm 断点
            from scrapy.cmdline import execute
            import os.path as Path
            import sys
            sys.path.append(Path.dirname(Path.abspath(__file__)))
            execute(["scrapy","crawl","SpdlerNAME"])

    4:调试
        》使用运行中的 第二中方法进行断点调试
        》命令行  scrapy shell URL

    5:爬虫类编写
        爬虫类得到的数据为原始数据，并不是JS执行之后的数据
        动态数据 selenium 编写下载中间件
    6:Item编写
    7:数据库保存




    开始爬虫1 --->Spider2 ----> Parse4 (yeild Item | Request)
                                     Item-->Piplines---->数据库
                                     Request--->4





    爬虫类
        from scrapy.spiders import BaseSpider, Spider, CrawlSpider, Rule
        //解析网页 提取需要的内容
        基类spiders{

            name = None
            start_urls   URL列表
            custom_settings = {
                settings是公共的  这个设置是属于自己的
            }
            download_delay :延迟 s
            allowed_domains  = [不需要http://www] 包含spider容许爬取的域名 来之中间件OffsiteMiddleware
            handle_httpstatus_list = []  表明这些状态码 我自己处理  中间件 HttpErrorMiddleware

            self.crawler = crawler   属性
            self.settings = crawler.settings 属性

            def start_request():  可选的
                return 返回 start_urls的Request 集合
                for one in start_url:
                    yeild Scrapy.Rquest(one)
                //return [Request]

            def parse(self, response):
                》得到Request 请求结果
                》数据解析
                》必须 yeild Item / Requst
                    Item Test1Pipeline

                    Request  再次爬取 scrapy.Request(...)
                            URL拼接  ===>直接用在这个urljoin
                            scrapy.Request(url=拼接,callback=解析函数,meta={传递的参数})

            @classmethod 生成Spider
            def from_crawler(cls, crawler, *args, **kwargs):
                spider = cls(*args, **kwargs)
                spider._set_crawler(crawler)
                return spider


        CrawlSpider:
            进行全站爬取
            class ScrapyCrawlSpider():
                rules = [
                    Rule(
                        LinkExtractor(allow=(,)...),
                        callback='callA',
                        follow=False,
                        process_links = "process_linksA"
                        process_request = "process_requestA"
                        ),
                    Rule(LinkExtractor(allow=(,)...),callback='callB',follow=False)
                ]
                def start_request(self):
                    #可重写
                    return Request(self.urls[0])

                def parse_start_url(self,response):
                    #解析 首页 数据数据 得到你需要的Item或者Request
                    return
                def process_result(self,result):
                    #过滤parse_start_url的得到结果
                    return

                //Rule1的回调
                def process_linksA(links):
                    A:首页 R1解析Response 得到的链接 过滤
                    return links
                def process_requestA(request):
                    对R1解析出来的link 的 Rquest 进行下一步配置
                    return request
                def callA(self,response):
                    这个回调是针对匹配的url 请求后的Request进行处理
                    return Item/Request


                //Rule回调


            Rule 为一个爬取规则 会被应用在所有Response选取上
                __init__(link_extractor, 解析Extractor 对象
                        callback=None,   解析Response回调
                            解析 匹配得到网址再次请求的Response
                        cb_kwargs=None,  会在callback回调时 传递
                        follow=None,
                        process_links=None,  在Scrapy解析links 后回调这个方法 返回新的links
                        process_request=identity  在解析到跟进的Request 后  回调

                说明：
                SourceReponse--Rule1--links--Requests----LinkResponses
                                      link --- Request ---LinkResponses(callback)

                                Rule2--links--Requests----LinkResponses
                                       link ---Request ---LinkResponses(callback)

                如果Follow为True   LinkResponses 会被当做 SourceReponse再次执行遍历这个rules


            LinkE:URL提取
                LinkExtractor
                    def __init__(
                                allow=(), "",("",)正则表达式必须满足
                                deny=(), "",("",)正则表达式必须不满足
                                allow_domains=(),（str或list）被容许的域名
                                deny_domains=(), （str或list）容许的域名之外的
                                restrict_xpaths=(), (str或list） 指定提取的范围
                                restrict_css=(),    (str或list） 指定提取的范围
                                tags=('a', 'area'), 指定提取的标签
                                attrs=('href',),  指定提取的属性
                                unique：bool 是否对提取的连接 进行去重
                                process_value：在提取到一个url后 调用返回新的url
                                strip=True
                                ):
                RegexLinkExtractor
                SgmlLinkExtractor


    数据解析
        HtmlResponse 解析
            def parse(self, response):
                response ---> 解析
                > response.selector  得Selector
                > response.xpath(...)  ==  Selector.xpath(...)
                > response.css(...)   ==   Selector.css(....)
                > response.text()
                > respnse.meta  得到传递的参数
                ......

        Selector
            selec = Selector(response)  // response.selector()

            res = selec.xpath(...) => 再次得到Selector对象
            res = selec.css(....)=> 再次得到Selector对象
            得到结果
                res.extract()  =>[结果]
                res.extract_first("Default")


    Request：请求
            》如果开启cookies 整个爬虫的Request都会包含所有cookies

        def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None):
            url:
            callback:请求回调  必须为self.func
                再次解析该Response的函数

            cookies : [{}...] /  {"name":1212....}指定

            //参数传递到该Request的Response
            meta :  request/resopnse中 可以为包含任何值 下面是scrpy 认可的
                    dont_redirect  重定向中间件
                    dont_retry
                    handle_httpstatus_list   错误处理中间件
                    dont_merge_cookies cookies中间件
                    cookiejar       cookies中间件
                    redirect_urls    重定向中间件
                    bindaddress
                    dont_retry       RetryMiddleware
                    自己的取其他名字

            encoding='utf-8',
            priority=0,  //调度优先级
            dont_filter=False, //当多个相同Request 会被过滤
            errback=None, 404/500等错误处理函数
            flags=None):

        scrapy.FormRequest POST
                》给服务器发送数据
                    [scrapy.FormRequest(url="http://www.example.com/post/action",
                                formdata={'name': 'John Doe', 'age': '27'},
                                callback=self.after_post)
                    ]
                》对表单处理的Request
                    scrapy.FormRquest.from_response(
                        response:携带表单的Response
                        formname:
                        formid
                        formxpath: 使用匹配到的第一个表单
                        formcss:  使用匹配到的第一个表单
                        formnumber (integer) 第几个表单被使用 默认为0
                        formdata：{}表单数据

                        //// 还不清楚具体使用
                        clickdata：{}
                        dont_click：boolean

                        1：默认情况下 Scrapy 是模拟第一个元素(<input type="sumbit">)的点击事件，表单就会提交
                        2：如果某些页面不是通过表单自己提交（不存在sumbit 标签）
                            而是通过JS来提交数据 默认行为就不适合 dont_click=True
                    )



    Item 数据处理模型  推荐是使用ItemLoader
        class JobbleBlogItem(scrapy.Item):
            icon = scrapy.Field()
            content = scrapy.Field()

        扩展Item(必须配合ItemLoader才有效)
            class JobbleBlogItem(scrapy.Item):
                name = scrapy.Field(
                    input_processor = Identity()/.../MYCustom(...),  loader设置属性时调用
                    output_processor = Identity()/.../MYCustom(...)  loader得到Item时取值是调用
                )
            from scrapy.loader.processors import MapCompose,Compose,TakeFirst,Identity,Join

            TakeFirst:取数组的第一个非空的值   -> 得到单个值
            Join : 有一个分割参数  表示对数组进行 join操作  "spre".join(arr)   -> 得到单个值

            Compose:  指定多个函数/表达式  Compose(Func1,Func2)
                    Value   Func1(Value)-> Value2 --> Func2(Value2)--> Value3

            MapCompose:指定多个函数/表达式 MapCompose(Func1,Func2)
                    Value [1,2,3] --> 遍历Value -> 调用Func1(one) --> Value1[1,2,3]
                    遍历Value1 -> 调用Func2(one) -->得到最后结果Value2[1，2，3]

            自定义函数
            class MYCustom(object):
                def __init__(self):
                    接受参数,该方法是可选的

                def __call__(self,value,...,loader_context):
                    return XXX


        Item( Feed exports)  配合Pipelie 扩展
            Item(
                serializer:lambda x:x
                在持久化之前调用
            )




    ItemLoader 可选 对item 有更多的处理
        from scrapy.loader import ItemLoader
        def parse(self,response):
            loader = ItemLoader(item=MYItem(),response=response)
            loader.add_css("title","#nav .left p::text")
            loader.add_xpath("icon","xpath")
            loader.add_value("url",response.url)

            _item = loader.load_item();
                》得到的_item属性值全是list

        1:直接使用 ItemLoader 你需要针对Item 的某些属性进行必要扩展
            》格式转 》Date处理 》取第一个数据。。。。

        2:也可以直接AAAALoader继承ItemLoader 进行统一配置 Item 扩展
            class AAAALoader(ItemLoader):
                default_item_class = Item
                default_input_processor = Identity()
                default_output_processor = Identity()
                default_selector_class = Selector

                针对属性
                name_in = Identity()
                name_out =  Join("-H-")

            lo = AAAALoader(item,....)
            it = lo.load_item()

        3:Item Loader Context  这是一个字典  会在这个Loader阶段存在
            修改Context三种方式
                1:  loader = ItemLoader(product)
                    loader.context['unit'] = 'cm'

                2:  loader = ItemLoader(product, unit='cm')
                3:  length_out = MapCompose(parse_length, unit='cm')
            使用
                >系统提供的 processors 你也用不到
                >自己定义的processors def __call__(self,va...,loader_context):pass
                >自己定义的处理函数中 def A(va...,loader_context):pass



    piplines 管道 Item后续处理（数据库保存之类的）
        1:编写Pip
        2:注册Pip  setting 里面配置
        3:说明在下面setting中

        自定义管道
            class Test1Pipeline(object)://继承object 即可
                def __init(self,xx,oo):
                    xx,oo 来之 def from_crawler
                    self.file = open('items.jl', 'w')
                    开始数据库 或者文件
                    pass
                def open_spider(self, spider):
                    self.file = open('items.jl', 'w')
                    开始数据库 或者文件
                    pass
                def process_item(self, item, spider):
                    line = json.dumps(dict(item)) + "\n"
                    self.file.write(line)
                    数据保存
                    //去重
                    //继续执行下一个管道
                    return item
                    //抛弃该Item
                    raise DropItem("Missing price in %s" % item)
                def spider_closed(self, spider):
                    self.file.close()
                    关闭数据库/文件
                    pass

                @classmethod
                def from_crawler(cls, crawler):
                    用于创建该管道
                    return cls(par,crawler.settings.get(...))
                    pass


        自定义管道中如何延迟调处理Item
            def process_item(self, item, spider):
                request = scrapy.Request(url)
                dfd = spider.crawler.engine.download(request, spider)
                dfd.addBoth(self.return_item, item)
                return dfd

            def return_item(self, response, item):
                if response.status != 200:
                    return item
                //其他处理
                return item

        图片下载（不要用默认的 直接继承 编写自己的 ）
            from scrapy.pipelines.images import ImagesPipeline
            1:编写Pipelines
            2:配置piplines
            3:配置下载路径
            class Test1Pipeline(ImagesPipeline):
                "
                    item:对于自定义Item
                    info: 保存着一些下载信息 from scrapy.pipelines.media import MediaPipeline
                    如果放弃该item   抛出异常 DropItem("Item contains no images")
                "
                def get_media_requests(self, item, info):
                    for image_url in item['image_urls']:
                        yield scrapy.Request(image_url)  //需要下载的图片url


                "
                    一个item 下载完成完成 后调用
                    result保存了item中图片下载信息 （,）
                    默认返回item 进入下一个管道
                "
                def item_completed(self, results, item, info):
                    //下载完成  或者 raise DropItem("sasasa")
                    // 进入下一个piplines
                    image_paths = [x['path'] for ok, x in results if ok]
                    if not image_paths:
                        raise DropItem("Item contains no images")
                    item['image_paths'] = image_paths
                    return item


        Pipelines到数据库
            pip install mysqlclient
                class MYSQLPipelines(object):
                    df __init__(self):
                          self.conn = MySQLdb.connect(host="localhost",user="root",password="4634264015",database="BloggBase",charset="utf8")
                          self.cursor = self.conn.cursor()

                    @classmethod
                    def from_crawler(cls, crawler):
                        return cls(...); -->__init__

                    def process_item(self, item, spider):
                        sql,paras = item.get_insert_sql()
                        self.cursor.execute(sql,paras)
                        self.conn.commit()
                        return item
                    def close_spider(self,spider):
                        self.cursor.close()

                class MYSQLPipLines2(object):异步处理
                    //数据异步保存  execute为同步操作
                    from twisted.enterprise import adbapi
                    import MySQLdb
                    import MySQLdb.cursors
                    def __init__(self, dbpool):
                        self.dbpool = dbpool

                    @classmethod
                    def from_crawler(cls, crawler):
                        settings = crawler.settings
                        dbparms = dict(
                            host = settings["MYSQL_HOST"],
                            db = settings["MYSQL_DBNAME"],
                            user = settings["MYSQL_USER"],
                            passwd = settings["MYSQL_PASSWORD"],
                            charset='utf8',
                            cursorclass=MySQLdb.cursors.DictCursor,
                            use_unicode=True,
                        )
                        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
                        return cls(dbpool)

                    def process_item(self, item, spider):
                        #使用twisted将mysql插入变成异步执行
                        query = self.dbpool.runInteraction(self.do_insert, item)
                        query.addErrback(self.handle_error, item, spider) #处理异常

                    def handle_error(self, failure, item, spider):
                        # 处理异步插入的异常
                        print (failure)

                    def do_insert(self, cursor, item):
                        #执行具体的插入
                        #根据不同的item 构建不同的sql语句并插入到mysql中
                        insert_sql, params = item.get_insert_sql()
                        print (insert_sql, params)
                        cursor.execute(insert_sql, params)

        扩展Piplines  不属于Pipelines 只是一个永久化工具
            https://docs.scrapy.org/en/latest/topics/exporters.html?highlight=json#built-in-item-exporters-reference
            from scrapy.exporters import XmlItemExporter
            BaseItemExporter
            XmlItemExporter
            CsvItemExporter
            PickleItemExporter
            PprintItemExporter
            JsonLinesItemExporter
                Item {
                    name = Filed(serializer=xx)
                }
                from scrapy.exporters import JsonLinesItemExporter
                class JsonPickerPipe(object):
                    def __init__(self):
                        self.jsonfile = open("arts.json","wb")
                        self.exporter = JsonLinesItemExporter(self.jsonfile,encoding="utf-8")
                        self.exporter.start_exporting()

                    def process_item(self, item, spider):
                        self.exporter.export_item(item)
                        return item

                    def close_spider(self,spider):
                        self.jsonfile.close()
                        self.exporter.finish_exporting()

                    setting FEED配置


    模拟用户登入
      A：requests(requests模拟登入.py) 确保所有请求都使用同一session(cookies保存一直)
            session = requests.session()
            session.get/post
        登入后保存cookies 然后在开启scrapy

      B: selenium进行登入 通用的
            登入后保存cookies 然后在开启scrapy

      C：scrapy 模拟登入 开启cookies
            会默认在以后的请求中加入cookies
            登入后可以直接 进行下部操作


    中间件
        下载中间件
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




            1:编写中间件
                》请求Request
                》下载Response
            2:seting激活 激活自己的中间件(会与系统默认的合并)

            class CustomDownloaderMiddleware(object):
                1:process_request(self,request, spider)
                    必须返回其中之一:
                        返回 None 、             继续处理request
                        返回一个 Response 对象、  Scrapy将不会调用其他中间件该方法  而是返回调用中间件的process_response()
                        返回一个 Request 对象     终止中间件调用 重新请求request
                        raise IgnoreRequest 。 则安装的下载中间件的 process_exception() 方法会被调用

                2:process_response(self,request, response, spider)
                    必须返回
                        返回一个 Response 对象、      可以与传入的response相同，也可以是全新的对象
                        返回一个 Request 对象          重新开始请求
                        raise一个 IgnoreRequest 异常。 则安装的下载中间件的 process_exception() 方法会被调用

                3:process_exception(self,request, exception, spider)
                    当中间件发送异常会调用
                    必须返回
                        返回 None 、       Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception() 方法
                        Response 对象、    已安装的中间件链的 process_response() 方法被调用  不会调用其他异常处理方法
                        Request 对象。     则返回的request将会被重新调用下载。


            默认的系在中间件  所有都是默认开启的
                cookies处理 scrapy.downloadermiddlewares.cookies.CookiesMiddleware
                        settings : COOKIES_ENABLED = True 是否开启
                        >会在请求中自动加入cookies
                        >Request 中 meta['dont_merge_cookies']将不会携带cookies
                        >meta["cookiejar"] = 1,3,.. 来支持一个Spider 保存多个session,必须在下个Request再次设置meta['cookiejar']


                请求头处理  scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware
                        settings : DEFAULT_REQUEST_HEADERS ={}

                超时中间件 scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware
                          settings  DOWNLOAD_TIMEOUT
                请求认证    scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware
                            Spider {
                                http_user = 'someuser'
                                http_pass = 'somepass'属性
                            }
                缓存中间件  scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware
                            #HTTPCACHE_ENABLED = True
                            #HTTPCACHE_EXPIRATION_SECS = 0
                            #HTTPCACHE_DIR = 'httpcache'
                            #HTTPCACHE_IGNORE_HTTP_CODES = []
                            #HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

                        scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware

                IP代理中间件 scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
                        只需要在每个Request中meta中设置meta["http_proxy"|"https_proxy"] = "http://1.1.1.1：9999" 就可以开启代理（但这IP也是固定一个）
                        https://github.com/kohn/HttpProxyMiddleware 多IP切换代理


                重定向中间件 scrapy.downloadermiddlewares.redirect.RedirectMiddleware
                        Request.meta 的 redirect_urls
                        REDIRECT_ENABLED
                        REDIRECT_MAX_TIMES

                Meta 刷新中间件scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware

                失败重试 scrapy.downloadermiddlewares.retry.RetryMiddleware
                    RETRY_ENABLED
                    RETRY_TIMES
                    RETRY_HTTP_CODES = [100,504,404]
                Robot 中间件 scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware
                        settings ROBOTSTXT_OBEY =False 关闭
                XXX     scrapy.downloadermiddlewares.stats.DownloaderStats

                UserAgent scrapy.downloadermiddlewares.useragent.UserAgentMiddleware
                        如果需要自定义 注册自己  关闭默认 | 自己的>默认的
                        https://github.com/hellysmile/fake-useragent


                Ajax    scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware


        Spider中间件
            Spider-----|--------------|--------2-------|------------|--------------------->引擎
                     中间| 件1     中间| 件2       中间 |件3     自定义|中间件                      (顺序根据配置而定)
                        |             |               |             |
                    ----|-------------|---------------|-------------|--------------------->spider 解析放回request    process_start_requests(start_requests, spider)
                        |             |               |             |                       spider 解析返回item 调用  process_spider_output(response, result, spider)
                        |             |           异常|处理          |
                        |             |               |             |
                    <---|-------------|---------2------|-------------|---------------------- resopnse 下发到spider 调用 process_spider_input(response, spider)



                1:编写中间件
                    》 engin--> Spider回调函数
                    》 spider回调函数 Item/Request的 处理
                2:seting激活 激活自己的中间件(会与系统默认的合并)

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

                    scrapy.contrib.spidermiddleware.depth.DepthMiddleware 处理深度
                    scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware 处理response 错误
                        容许错误Response 自己处理
                        A:HTTPERROR_ALLOWED_CODES
                        B:Request(meta={handle_httpstatus_list:[404,..]})
                        C:class MySpider(CrawlSpider):
                            handle_httpstatus_list = [404]

                    scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware  过滤 域名
                        allowed_domains 容许的域名
                        Request(dont_filter=True)不进行过滤
                    scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware
                        URLLENGTH_LIMIT 限制URL长度





    数据收集  Scrapy 默认|始终都会有一个消息收集器

        便于收集Spider http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/stats.html
        scrapy/statscollectors.py
        from scrapy.statscollectors import StatsCollector
        编写自己的统计信息收集器
        class UserLoginDataCollection(StatsCollector):
            def __init__(self,crawler):
                super(UserLoginDataCollection,self).__init__(crawler)
            def set_value(self, key, value, spider=None):
                pass
        settings配置
            STATS_CLASS ="MMSpider.DataCollection.UserLoginDataCollection"
        调用
            crawl.stats.set/get...

    限速：
        settings
    DjangiItem:
        使用Django 的Item
    信号
        from scrapy import signals
        from scrapy.xlib.pydispatch import dispatcher
        监听信号
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        Crawler下的信号管理者 connect(receiver, signal)


    Scrapy任务
        开启 暂停 恢复
    API:
        Crawler
            settings 的配置管理器。
            signals  crawler的信号管理器。SignalManager
            stats   crawler的统计信息收集器。
            extensions 扩展管理器，跟踪所有开启的扩展。
            spiders spider管理器，加载和实例化spiders。
            engine 执行引擎，协调crawler的核心逻辑

        SignalManager
            connect(receiver, signal) 绑定函数
            send_catch_log(signal, **kwargs) 发送信号
            disconnect(receiver, signal)解除函数
            disconnect_all(signal)

        StatsCollector状态收集器 scrapy.statscol.StatsCollector
            get_value
            set_value
            。。。。
    扩展
        把你的自定义任务功能绑定到scrapy上
        class UserExtendes(object):
            def __init__(self, item_count):
                配合信号
                pass

            @classmethod
            def from_crawler(cls, crawler):
                crawler.signals.connect(Func, signal=signals.spider_opened)
                return cls()
                pass
        EXTENSIONS = {
            'scrapy.contrib.corestats.CoreStats': 500,
            'scrapy.webservice.WebService': 500,
            'scrapy.telnet.TelnetConsole': 500,
            ......你的扩展
        }

        scrapy.contrib.logstats.LogStats 记录统计扩展
        scrapy.contrib.corestats.CoreStats 核心统计扩展
        scrapy.webservice.WebService  Web service 扩展
        scrapy.telnet.TelnetConsole
        scrapy.contrib.memusage.MemoryUsage 内存使用扩展
        scrapy.contrib.memdebug.MemoryDebugger
        scrapy.contrib.closespider.CloseSpider 关闭spider扩展
            CLOSESPIDER_TIMEOUT  如果一个spider在指定的秒数后仍在运行就会被关闭
            CLOSESPIDER_ITEMCOUNT  如果spider爬取Item条目数超过了指定的数
            CLOSESPIDER_PAGECOUNT  如果spider抓取Page超过指定的值
            CLOSESPIDER_ERRORCOUNT  如果spider生成多于该数目的错误
        scrapy.contrib.statsmailer.StatsMailer 会在爬取完成发送提醒邮件

    任务的开启暂停 只能在命令行下进行
        一个把调度请求保存在磁盘的调度器
        一个把访问请求保存在磁盘的副本过滤器[duplicates filter]
        一个能持续保持爬虫状态(键/值对)的扩展
        spider.state 来保存你自己需要序列化的变量

        保存配置路径:
            不能被不同spider共享   同一个spider的不同jobs/runs也不行

        开启:
            scrapy crawl name -s JOBDIR=AA/name-1
        暂停:
            Ctrl-C或者发送一个信号
            等待一些请求完成
            再次Ctrl-C 暂停
            直接两次会直接退出
        继续:
            scrapy crawl name -s JOBDIR=AA/name-1 接着之前的任务
            scrapy crawl name -s JOBDIR=AA/name-2 再次重新开启

    Error:错误
        scrapy.exceptions.DropItem
"""

"""
    settings{
        //是否遵循robots  关闭
        ROBOTSTXT_OBEY = True

        管道配置
        ITEM_PIPELINES = {
            >所有yeild 的item 都会调用所有PipLines
            >顺序为后面数据大小  小(先)--->大(后)
            >在管道中对item进行过滤


            'scrapy.contrib.pipeline.images.ImagesPipeline': 100, 默认的图片下载pipline
            'Test1.pipelines.CustomImagePipLines': 200,//自己的
            'Test1.pipelines.Test1Pipeline': 300,//自己的

        }

        //日志
        LOG_LEVEL= 'DEBUG'

        LOG_FILE ='log.txt'

        //开启cookies
        COOKIES_ENABLED = True

        //图片下载路径
        IMAGES_STORE = ''
        IMAGES_EXPIRES = 30 过期时间T
        IMAGES_THUMBS = {大小限制
           'small': (50, 50),
            'big': (270, 270),
        }
        IMAGES_MIN_HEIGHT = 110
        IMAGES_MIN_WIDTH = 110


        //文件pipe配置
        FILES_STORE = '/path/to/valid/dir'
        FILES_EXPIRES = 120 过期时间T


        // 媒体
        MEDIA_ALLOW_REDIRECTS = True 重定向

        //Download中间件
        DOWNLOADER_MIDDLEWARES = {
            'myproject.middlewares.CustomDownloaderMiddleware': 543,  顺序
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,  取消系统中间件
        }
        //Spider 中间件
        SPIDER_MIDDLEWARES = {
            'myproject.middlewares.CustomSpiderMiddleware': 543,
            'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
        }
        //自动下载限速
        AUTOTHROTTLE_ENABLED:True
        AUTOTHROTTLE_START_DELAY:5  初始下载延迟(单位:秒)。
        AUTOTHROTTLE_MAX_DELAY：70 在高延迟情况下最大的下载延迟(单位秒)。

        全局并发数
        CONCURRENT_REQUESTS = 100   调试 选择CPU 80%-90%的并发数
        关闭重定向
        REDIRECT_ENABLED = False

        //FEED序列化参数
        FEED_URI 必须指定
            ftp://user:password@ftp.example.com/scraping/feeds/%(name)s/%(time)s/%(xx)s.json
            %(time)s 会被当前时间替换
            %(name)s - 被spider的名字覆盖
            %(xx)s  会被spider中变量替换

        FEED_FORMAT格式
            "json"|"jsonlines"|"csv"|"xml"|"pickle"
        FEED_STORAGES
            有默认值
            这里指定含项目支持的额外feed存储端配置
                {'ftp': 'scrapy.contrib.feedexport.FTPFeedStorage',}
        FEED_EXPORTERS
            有默认值
            指定支持的额外输出器
                {'json': 'scrapy.contrib.exporter.JsonItemExporter',}
        FEED_STORE_EMPTY  是否输出空feed(没有item的feed)。  False
        FEED_EXPORT_ENCODING  编码

    }

    css选择器
    css{
        ".a" ".a  .aa"  ".a.b 有a,b两个class"

        "#id"

        "div.class"

        "div a::attr(href)"  "div p::text"

        "::attr(href)"
        "div[name='xxxx']"
    }

    url拼接
        from urllib.parse import urljoin
        url = urljoin("URLStr","part")
            //如果part携带域名 , 不会使用base的主域名
            //URLStr 携带主域名就可 就会和part进行拼接

    Html tag移除
        <div>AAA<p>BBBB</p></div>
        from w3lib.html import remove_tags
            ===>AAABBB

    PipeLines / Spider / Middleware
        @classmethod
        def from_settings(cls,settings):
            settings
            return cls(...)
        @classmethod
        def from_crawler(cls, crawler):
            return cls(....)
        如果重写该方法就会适应该方法来生成Pipeline/Spider 传递配置参数


    反爬虫
        》ip 代理，
        》User-agen随机配置         》 中间件处理
        》注册 携带cookies 和token  》 登入后Scrapy自动会加入
        》限制爬虫爬取数据
        》验证码
        》selenium/phantomjs 模拟浏览器

    验证码识别：
        A:
            重新得到验证码图片
            PIL打开
            要求用户输入
        B：云识别
    动态页面爬取
        A:selenium 开启爬取 需要
            Chrome需要界面浏览器
            PhantomJS无界面浏览器  不稳定
        B:pyvirtualdisplay为无界面浏览器driver 推荐
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1024, 768))
            display.start()
            在使用selenium
        C:scrapy-splash
        D:selenium-grid

        class SeleniumMiddera(object):
            def __ini__():
                seld.broser = Chrome()
                pass
            def process_request(self,request, spider):
                self.broser.get("")
                return HtmlResponse()
                pass
    URL去重：
        scrapy 默认开启了去重

    Telnet终端：
        默认开启Telnet终端 以便Scrapy运行过程中控制Scrapy|查看状态
        TELNETCONSOLE_HOST:127.0.0.1
        TELNETCONSOLE_PORT:[端口范围] 0|None 为动态分配
        http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/telnetconsole.html

"""


