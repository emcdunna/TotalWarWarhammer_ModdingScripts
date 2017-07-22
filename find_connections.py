from total_war_module import *

for line in sys.stdin:
	data = strip_filename(line)
	total_result = process_connections(data)
	print total_result
	print ""
	
	
	
	
	
	
	
			
	