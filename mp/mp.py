from multiprocessing import Process, Pipe
from time import sleep
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def func(timer: int, text: str, conn):
    print(f'func +{text} start')
    sleep(timer)
    print(f'func +{text} stop')
    conn.send([f'func +{text} results'])
    conn.close()

@timeit
def main():
    processlist = []
    parent_connections = []
    for i in range(10, 1, -1):
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)

        p = Process(target=func, args=(i, f'{i}', child_conn))
        processlist.append(p)
        
    for p in processlist:
        p.start()
    for p in processlist:
        p.join()
    # func(1, '1', None)
    for p in parent_connections:
        print(p.recv())

    
if __name__ == '__main__':
    main()
