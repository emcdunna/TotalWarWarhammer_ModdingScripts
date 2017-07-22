import sys
import mmap
import string
import Queue
import subprocess
import shutil
from os import listdir
import os

variant_mesh_root_dir = """C:/Program Files (x86)/Steam/steamapps/common/Total War WARHAMMER/lorehammer_by_emc/variantmeshes/"""

variant_mesh_dest_dir = """C:/Program Files (x86)/Steam/steamapps/common/Total War WARHAMMER/temporary_generated_files/variantmeshes/"""
mesh_subdir = """variantmeshdefinitions/"""
model_subdir = """wh_variantmodels/"""
vm_f_ext = ".variantmeshdefinition"
rm_f_ext = ".rigid_model_v2"
ws_f_ext = ".wsmodel"
dds_f_ext = ".dds"
letter_set = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "_-" + """/\."""

garbage_code = "403fc5fe4c40d00f4940960a063f01"

xml_f_ext = ".xml"
old_files_directory = """compare_tw_raw_data/"""
new_files_directory = """C:/Program Files (x86)/Steam/steamapps/common/Total War WARHAMMER/assembly_kit/raw_data/db/"""

class circle_buff_string:
	def __init__(self,max_size):
		self.max_size = max_size
		self.contents = ""
	
	def add_char(self,ch):
		if len(self.contents) < self.max_size:
			self.contents += ch
		else:
			self.contents = self.contents[1::] + ch
			
	def __str__(self):
		return self.contents
	
	def is_full(self):
		if len(self.contents) == self.max_size:
			return True
		return False
		
class tree_node:
	def __init__(self,nm,oldnm,parent,ntype):
		self.name = nm
		self.old_name = oldnm
		self.parent = parent
		self.children = []
		self.type = ntype
	def add_child(self,child):
		self.children.append(child)
	def __str__(self):
		return self.name

def read_line_as_tsv(word):
	lst = []
	tmp = ""
	
	for i in word:
		if i == "\t" or i == "\n":
			lst.append(tmp)
			tmp = ""
		else:
			tmp += i
	return lst

def strip_filename(word):
	fname = ""
	bad = {" ",".","\n","\r"}
	for i in word:
		if i in bad:
			return fname
		else:
			fname += i
	return fname
	
def find_file(offset,full_line):
	tmp = ""
	for i in full_line:
		if i == "\t":
			pass
		else:
			tmp += i
	cut_front = tmp[offset::]	
	final = ""
	for c in cut_front:
		if c == ".":
			return final
		else:
			final += c
	return final
		
def find_dds_in_rigid(rm_file):
	result = ""
	result += "rigidmodel\t" + rm_file + "\n"
	try:
		with open(variant_mesh_root_dir + model_subdir + rm_file + rm_f_ext, "r+b") as f:
			mm = mmap.mmap(f.fileno(),0)
			wordset = set()
			START = False 
			tmp = ""
			for seg in mm:
				if seg in letter_set:
					START = True
					tmp += seg
				elif START == True:
					if ".dds" in tmp:
						wordset = wordset | {tmp}
					tmp = ""
					START = False
				elif START == False:
					pass
		
		for word in wordset:
			newword = word[31:-4]
			result += "dds_file\t" + newword + "\n"
		result += "END OF rigidmodel\t(" + rm_file + ")\n"
	except:
		result = "rigidmodel\t" + rm_file + "\tFile not found. \n"
	return result			
		
	
def process_connections(filename):
	result = ""
	result += "variantmesh\t" + filename + "\n"
	try:
		currfile = open(variant_mesh_root_dir + mesh_subdir + filename + vm_f_ext, "r" )
		for fline in currfile:
			fline = fline.lower()
			if vm_f_ext in fline:
				# the line has a vm in it
				vfile = find_file(73,fline)
				result += process_connections(vfile)
				
			if (rm_f_ext in fline) or (ws_f_ext in fline):
				# the line has a rigid model in it
				rfile = find_file(52,fline)
				result += find_dds_in_rigid(rfile)
		
		currfile.close()
		result += "END OF variantmesh\t(" + filename + ")\n"
		return result
	except:
		return result + "FILE NOT FOUND"
		
def mk_node(line,pp):
	lst = read_line_as_tsv(line)
	try:
		onm = lst[1]
	except:
		onm = "Error_not_found"
	try:
		ln = len(lst[2])
		ln2 = len(lst[1])
		new_name = onm[0:(ln2-ln)] + lst[2]
	except:
		new_name = onm

	node = tree_node(new_name,onm,pp,lst[0])
	return node
	
def process_tree(tree_obj, prefix):
	# copy and rename under each specific file type
	if tree_obj.type == "variantmesh":
			copy_and_rename_vm(tree_obj)
			
	if tree_obj.name != tree_obj.old_name:
		
		if tree_obj.type == "rigidmodel":
			copy_and_rename_rm(tree_obj)
		else:
			copy_and_rename_dds(tree_obj)
	
	if tree_obj != None:
		print prefix + str(tree_obj)
		index = 1
		for child in tree_obj.children:
			process_tree(child, prefix + "\t")
			index += 1

def str_replace_all_children(word,node):
	for child in node.children:
		word = word.replace( child.old_name, child.name )
	return word
		
# copy paste text into new file name, replacing reference to a child node's name with the new ones
def copy_and_rename_vm(node):
	rfname = variant_mesh_root_dir + mesh_subdir + node.old_name + vm_f_ext
	wfname = variant_mesh_dest_dir + mesh_subdir + node.name + vm_f_ext
	rfile = open(rfname,"r")
	
	if not os.path.exists(os.path.dirname(wfname)):
		try:
			os.makedirs(os.path.dirname(wfname))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	
	wfile = open(wfname,"w")
	file_str = ""
	for line in rfile:
		file_str += line	
	new_string = str_replace_all_children(file_str,node)
	wfile.write(new_string)
	return None
	
# same as vm, but in binary
def copy_and_rename_rm(node):
	src = variant_mesh_root_dir + model_subdir + node.old_name + rm_f_ext
	dst = variant_mesh_dest_dir + model_subdir + node.name + rm_f_ext
	
	if not os.path.exists(os.path.dirname(dst)):
		try:
			os.makedirs(os.path.dirname(dst))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
				
	f=open(src,"rb")
	s=f.read()
	f.close()
	new_string = str_replace_all_children(s,node)
	wf=open(dst,"wb")
	wf.write(new_string)
	wf.close()
	return None

# just copy paste the files with a new name
def copy_and_rename_dds(node):
	src = variant_mesh_root_dir + model_subdir + node.old_name + dds_f_ext
	dst = variant_mesh_dest_dir + model_subdir + node.name + dds_f_ext
	
	if not os.path.exists(os.path.dirname(dst)):
		try:
			os.makedirs(os.path.dirname(dst))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
				
	try:
		shutil.copy(src,dst)
	except:
		sys.stderr.write("DDS file: " +src + " not found.\n")
	return None

# translates a hex string "0a" to int like 10. 
def string_hex_to_int(word):
	return int(word,16)
	
# translate char to hex *ascii*		
def char_to_hex_ascii(ch):
	return "{0:02x}".format(ord(ch))
		
# create binary string for single entry, encoding length byte at the beginning
def create_binary_string(word):
	ln = len(word)
	bln = chr(ln)
	z = chr(0)
	return bln + z + word
	
# translate hex string to ascii chars
def string_hex_to_string_ascii(word):
	final_str = ""
	i = 0
	tmp = ""
	for l in word:
		tmp += l
		i += 1
		if i == 2:
			final_str += chr(string_hex_to_int(tmp))
			tmp = ""
			i = 0
	return final_str	
	 

# create the binary line from a [], holding [art set id, variant filename, mask 1, mask 2, mask 3, ?]
def create_binary_line(info_lst):
	line = ""
	as_id = create_binary_string(info_lst[0])
	line = as_id + string_hex_to_string_ascii(garbage_code)
	
	for i in range(1,len(info_lst)):
		line += create_binary_string(info_lst[i])
	
	return line
		
		
		
		
		
		

		