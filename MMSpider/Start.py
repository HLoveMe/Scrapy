
lambda x:x

if __name__ == "__main__":
    from scrapy.cmdline import execute
    import os.path as Path
    import sys

    sys.path.append(Path.dirname(Path.abspath(__file__)))
    # ProxyIP
    # execute(["scrapy","crawl","ProxyIP"])
    execute(["scrapy", "crawl", "JRSpider"])
    #scrapy crawl JRSpider -s JOBDIR=SpiderState/001

