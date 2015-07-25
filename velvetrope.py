#!/usr/bin/env python

import sys
import subprocess as sp
import psutil
import time
import signal
import argparse
import shlex
import threading
from collections import deque

running = []

def get_free_memory():
    m = psutil.virtual_memory()
    return m.available

def shutdown(signal, frame):
    """ Handler for the SIGINT signal. Sets the ``exit_flag`` to shutdown
    """
    print 'Caught interrupt, shutting down.'
    for cmd, p in running:
        p.kill()
    exit_flag.set()

def parse_mem_arg( arg ):
    units = arg.lower()[-1]
    int_part = int(arg[:-1])
    if units == 'm':
        return int_part * 1024**2
    elif units == 'g':
        return int_part * 1024**3

parser = argparse.ArgumentParser(prog="velvetrope.py", description="run max_processes processes at a time from stdin, bounce and reque when memory reserve reached")
parser.add_argument('--max_processes', type=int, required=True, help='maximum number of processes to run concurrently')
parser.add_argument('--mem_reserve', required=True, help='free memory threshold to maintain in m or g, ex: 1024m, 1g')
parser.add_argument('--interval',type=int,default=5, help='polling interval in seconds - allows RAM to equilibrate between starting/killing jobs, default: 5')

args = parser.parse_args()
max_processes = args.max_processes
try:
    mem_reserved = parse_mem_arg( args.mem_reserve )
except:
    raise Exception("mem_reserved should be specified in m or g, ex: 1024m")
poll_interval = args.interval

cmd_list = deque()

#read list of commands from stdin
for line in sys.stdin:
    cmd_list.append( line.strip() )

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)
exit_flag = threading.Event()
while not exit_flag.isSet():
    running = [ x for x in running if x[1].poll()==None ]
    mem_free = get_free_memory( ) 
    if len(running) < max_processes and mem_free > mem_reserved and len(cmd_list) > 0:
        cmd = cmd_list.popleft()
	print cmd
        p = sp.Popen( shlex.split(cmd) )
        running.append( (cmd, p) )
    if len(running) == 0 and len(cmd_list) == 0:
        exit_flag.set()
    if mem_free < mem_reserved and len(running) > 1:
        #kill and requeue most recent task
        cmd, p = running.pop()
	print "hit memory limit, killing and requeing:\n %s" % cmd
        p.kill()
        cmd_list.append( cmd )
    time.sleep( poll_interval )
