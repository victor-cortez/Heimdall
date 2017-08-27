import multiprocessing

def worker():
    """worker function"""
    print ('Worker')
    return
def receive():
    n = input(">>>")
if __name__ == '__main__':
    p = multiprocessing.Process(target=worker)
    p.start()
    o = multiprocessing.Process(target=receive)
    o.start()
    for i in range(10):
        p = multiprocessing.Process(target=worker)
        p.start()