from total_war_module import *

parque = Queue.LifoQueue()
tree = None
tree_list = []

prog_log = open("program_log.txt","w")

for line in sys.stdin:
	lnlst = read_line_as_tsv(line)
	if lnlst[0] == "":
		pass
	elif "END OF" in line:
		prog_log.write(line[0:-1] + "\tParent:" + str(tree) + "\tQ_size:" + str(parque.qsize()) + "\n")
		
		if parque.empty() == True:
			if tree != None:
				prog_log.write("TREE_LST ADD --> " + str(tree) + "\n")
				tree_list.append(tree)
				tree = None
		else:
			tree = parque.get()	
			prog_log.write("NEW parent = " + str(tree) + "\n")
		
	else:	
		if "File not found" in line:
			prog_log.write("FNF: " + line)
		else:
			node = mk_node(line,tree)
			prog_log.write(str(node.type) + "_NODE:" + str(node) + "\tParent:" + str(tree) + "\tQ_size:" + str(parque.qsize()) + "\n")
			if tree == None:
				tree = node
				prog_log.write("Since parent = None, new parent = " + str(node) + "\n")
			else:
				tree.add_child(node)
				prog_log.write("PARENT:" + str(tree) + " gains child:" + str(node) + "\n")
				
				if (node.type == "variantmesh" or node.type == "rigidmodel"):
					parque.put_nowait(tree)
					prog_log.write("Queue.put(" + str(tree) + "), new parent = " + str(node) + "\n")
					tree = node
					


for tree in tree_list:
	process_tree(tree, "")
	sys.stdout.flush()
