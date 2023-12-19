import multiprocessing

def worker(procnum):
    '''worker function'''
    print (str(procnum) + ' represent!')
    return procnum


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    print(jobs)