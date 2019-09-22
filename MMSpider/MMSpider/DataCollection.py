

from scrapy.statscollectors import StatsCollector


class UserLoginDataCollection(StatsCollector):
    def __init__(self,crawler):
        super(UserLoginDataCollection,self).__init__(crawler)

    def set_value(self, key, value, spider=None):
        pass


"""

"""