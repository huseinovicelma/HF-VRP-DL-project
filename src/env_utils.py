import gurobipy as gp

def create_env(logfile=None, output_flag=True, threads=None, mip_gap=None, presolve=None):

    env = gp.Env(empty=True)

    env.setParam("OutputFlag", 1 if output_flag else 0)

    if logfile:
        env.setParam("LogFile", logfile)

    if threads is not None:
        env.setParam("Threads", threads)

    if mip_gap is not None:
        env.setParam("MIPGap", mip_gap)

    if presolve is not None:
        env.setParam("Presolve", presolve)

    env.start()
    return env
