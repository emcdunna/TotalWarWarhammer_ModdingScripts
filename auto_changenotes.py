from total_war_module import *
import xml.etree.ElementTree as ET

#root = ET.fromstring(country_data_as_string)
# root.tag
# root.attrib

SUPPRESS_NO_CHANGE = True
old_gamefiles = dict()
new_gamefiles = dict()

# use this for comparing lines
def compare_dicts(new_d,old_d):
	d1_keys = set(new_d.keys())
	d2_keys = set(old_d.keys())
	intersect_keys = d1_keys.intersection(d2_keys)
	added = d1_keys - d2_keys
	removed = d2_keys - d1_keys
	modified = set()
	same = set()

	for key in intersect_keys:
		new_val = new_d[key]
		old_val = old_d[key]
		if new_val == old_val:
			same = same | {(key,new_val,old_val)}
		else:
			modified = modified | {(key,new_val,old_val)}

	return added, removed, modified, same

# return a dict of dicts of dicts
def parse_xml_file(filename):
	try:
		file_set = dict()
		tree = ET.parse(filename)
		root = tree.getroot()
	
		for child in root: # each child is a "row"
			row_dict = dict()
			rkey = "None"
			for item in child.attrib.items():
				if item[0] == "record_key":
					rkey = item[1]
			for gchild in child: # each gchild is an item in the row
				row_dict[str(gchild.tag)] = gchild.text
		
			if rkey != "None":
				file_set[rkey] = row_dict
				
		return file_set
	except:
		return "ERROR While parsing file"

# prints hierarchical element type		
def print_element(root):
	for child in root:
		print str(child.tag) + "\t" + str(child.attrib)
		for gchild in child:
			print "\t" + str(gchild.tag) + "\t" + str(gchild.text)

xls_buff = ""
xls_file = open("xls_changelog.tsv","w")
for filename in listdir(new_files_directory):
	new_d = parse_xml_file(new_files_directory + filename)
	new_gamefiles[filename] = new_d
	if new_d != "ERROR While parsing file":
		if filename in listdir(old_files_directory):
			file_issues = set()
			
			old_d = parse_xml_file(old_files_directory + filename)
			old_gamefiles[filename] = old_d
			
			new_keys = set(new_d.keys())
			old_keys = set(old_d.keys())
			intersect_keys = new_keys.intersection(old_keys)
			added_lines = new_keys - old_keys 
			removed_lines = old_keys - new_keys
			
			
			buffer = ""
			for akey in added_lines:
				aline = new_d[akey]
				issue = "Added entry: " + str(aline)
				file_issues = file_issues | {issue}
				buffer += "\t" + str(issue) + "\n"
				xls_buff += filename + "\t" + "Added entry:" + "\t" + str(akey) + "\t" + str(aline) +"\n"
				
			for rkey in removed_lines:
				rline = old_d[rkey]
				issue = "Removed entry: " + str(rline)
				file_issues = file_issues | {issue}
				buffer += "\t" + str(issue) + "\n"
				xls_buff += filename + "\t" + "Removed entry:" + "\t" + str(rkey) + "\t" + str(rline) +"\n"
				
			
			cols_added = set()
			cols_removed = set()
			for ikey in intersect_keys:
				try:
					old_line = old_d[ikey]
					new_line = new_d[ikey]		
					added, removed, modified, same = compare_dicts(new_line, old_line)
					
					
					for add in added:
						issue = "Added column: \t" + str(add)
						cols_added = cols_added | {issue}

					for rem in removed:
						issue = "Removed column: \t" + str(rem)
						cols_removed = cols_removed | {issue}
					
					for mod in modified: 
						issue = "Change in \"" + str(ikey) + "\", field: \"" + str(mod[0]) + "\", new value: " + str(mod[1]) + ", old value: " + str(mod[2])
						file_issues = file_issues | {issue}
						buffer += "\t" + str(issue) + "\n"
						xls_buff += filename + "\t" + "Change in " + "\t" + str(ikey) + "\tField: \"" + str(mod[0]) + "\", new value: " + str(mod[1]) + ", old value: " + str(mod[2]) +"\n"
				
				except:
					file_issues = file_issues | {"Error in processing changes"}
					buffer += "\t" + str("Error in processing changes") + "\n"
			
			if buffer != "" or len(cols_added) > 0 or len(cols_removed) > 0:
				print "-" *150
				print "Changes in file: \"" + str(filename) + "\""
				
				for ca in cols_added:
					print "\t" + str(ca)
					xls_buff += filename + "\t" + str(ca) +"\n"
				for cr in cols_removed:
					print "\t" + str(cr)
					xls_buff += filename + "\t" + str(cr) +"\n"
				print buffer
				
				print ""
			else:
				if SUPPRESS_NO_CHANGE == True:
					pass
				else:
					print "No issues with: \"" + str(filename) + "\""
			xls_file.write(xls_buff)
			xls_file.flush()
			xls_buff = ""
	else:
		print new_d + ": \"" + str(filename) + "\""

print "-" *150	
			

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	