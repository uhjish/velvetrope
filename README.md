# Velvet Rope

A greedy parallel execution tool. Given a list of processes to be run, velvetrope will try to maximize cpu and mem usage killing and requeing tasks when mem limit is hit.

	usage: velvetrope.py [-h] --max_processes MAX_PROCESSES --mem_reserve MEM_RESERVE [--interval INTERVAL]

	run max_processes processes at a time from stdin, bounce and reque when memory reserve reached

	optional arguments:
	  -h, --help            show this help message and exit
	  --max_processes MAX_PROCESSES		maximum number of processes to run concurrently
	  --mem_reserve MEM_RESERVE			free memory threshold to maintain in m or g, ex:
                        1024m, 1g
	  --interval INTERVAL   			polling interval in seconds - allows mem usage to 'catch up' between starting/killing jobs, default: 5