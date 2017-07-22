import sys
import mmap
import string

garbage_code = "403fc5fe4c40d00f4940960a063f01"

# create binary string for single entry, encoding length byte at the beginning
def create_binary_string(word):
	ln = len(word)
	bln = chr(ln)
	z = chr(0)
	return bln + z + word
	 

# create the binary line from a [], holding [art set id, variant filename, mask 1, mask 2, mask 3, ?]
def create_binary_line(info_lst):
	line = ""
	as_id = create_binary_string(info_lst[0])
	line = as_id + garbage_code
	
	for i in range(1,len(info_lst)):
		line += create_binary_line(info_lst[i])
	
	return info_lst

