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
    
## Modifying dDocent

Find the freebayes line in the dDocent script and modify it to use xargs and velvetrope as below:

  ls mapped.*.bed | sed 's/mapped.//g' | sed 's/.bed//g' | shuf | xargs -I % echo "freebayes -L bamlist.list -t mapped.%.bed -v raw.%.vcf -f reference.fasta -m 5 -q 5 -E 3 --experimental-gls --min-repeat-entropy 1 -V --populations popmap -n 10" | velvetrope.py --max_processes 8 --mem_reserve 1024m --interval 5

You should change the max_processes argument to something like n-1 cores on machine
You can set the mem_reserve to some amount of memory you feel would not easily be scarfed up in interval seconds
The velvetrope script checks every interval seconds (5 seconds default) to see if a process slot is free or if free memory has fallen below threshold
If there are process slots and memory free is above threshold, it pulls a command off the queue and runs it
If free memory has fallen below reserve threshold, it kills the newest process and adds it back to the queue

This allows us to utilize the discussed strategy of utilizing max(cpu, ram) as possible for a parallel pipeline

