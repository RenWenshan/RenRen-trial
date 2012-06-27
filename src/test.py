from multiprocessing import Pool

def f(x):
    return x*x


tasks = []
for i in range(10):
    tasks.append(i)
    
pool = Pool(processes = 4)
print pool.map(f, tasks)
