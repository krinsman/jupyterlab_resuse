__version__="0.1.2"

def mem_limit_calculator(rss, used_mem, total_mem, num_users, cpu_percent):
    if num_users > 0:
        targetPctFraction = 1/num_users
    else:
        targetPctFraction = 1
    return targetPctFraction * total_mem
