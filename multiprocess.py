from multiprocessing import Process

def make_task(f):
    return Process(target=f)

def make_tasks(fs):
    return [make_task(f) for f in fs]

def run_tasks(tasks):
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()