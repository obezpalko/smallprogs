from consul.base import Timeout
from consul.tornado import Consul
from tornado.gen import coroutine
from tornado.ioloop import IOLoop


class Config(object):
    def __init__(self, loop):
        self.foo = None
        loop.add_callback(self.watch)

    @coroutine
    def watch(self):
        c = Consul(host='sys-consul2c.42.wixprod.net')
        # print(dir(c))
        # index,nodes = c.catalog.nodes()
        # print(index, nodes)
        # asynchronously poll for updates
        index = None
        while True:
            try:
                # index, data = yield c.kv.get('lead', index=index)
                index, data = yield c.catalog.services(index=index)
                # index, data = yield c.health.service(index=index)
                if data is not None:
                    print(index, len(data))
                    self.foo = len(data)
            except Timeout:
                # gracefully handle request timeout
                pass


if __name__ == '__main__':
    loop = IOLoop.instance()
    _ = Config(loop)
    loop.start()