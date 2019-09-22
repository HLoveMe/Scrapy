
# pip install fake-useragent
from fake_useragent import UserAgent

class CUserAgentMiddleware(object):

    @classmethod
    def from_settings(cls,settings):
        return cls()

    def __init__(self):
        super(CUserAgentMiddleware,self).__init__()
        self.ua  = UserAgent()

    def process_request(self,request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)
        return None

