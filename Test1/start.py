

"""
    启动Scrapy

"""
from scrapy.cmdline import execute
import os.path as Path
import sys
sys.path.append(Path.dirname(Path.abspath(__file__)))


execute(["scrapy","crawl","Bobbole"])
# execute(["scrapy","crawl","ZZ"])