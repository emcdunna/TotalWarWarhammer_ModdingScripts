import sys

def split_line_tsv(line):
    word = ""
    lst = []
    for i in line:
        if i == "\t":
            lst.append(word)
            word = ""
        elif i == "\n":
            pass
        else:
            word += i
    lst.append(word)
    return lst

def two_dig_int(i):
    if i < 10:
        return "0" + str(i)
    else:
        return str(i)

character_skill_node_links = open("character_skill_node_links_tables.tsv",'w')
character_skill_nodes = open("character_skill_nodes_tables.tsv",'w')

for line in sys.stdin:
    inputs = split_line_tsv(line)
    name = inputs[0]
    subculture = inputs[1]
    magic = bool(int(inputs[2]))
    self = bool(int(inputs[3]))
    unique = int(inputs[4])

    key_start = "wh_main_skill_node_"

    cap = []
    cap.append("_battle_")
    cap.append("_campaign_")
    if self == True:
        cap.append("_self_")
    if magic == True:
        cap.append("_magic1_")

    sys.stdout = character_skill_node_links
    for c in cap:
        print key_start + name + c + "02" + "\t0\t" + key_start + name + c + "01\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "03" + "\t0\t" + key_start + name + c + "01\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "04" + "\t0\t" + key_start + name + c + "01\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "05" + "\t0\t" + key_start + name + c + "01\t1\t1\t0\t0\t" + "REQUIRED"

        print key_start + name + c + "06" + "\t0\t" + key_start + name + c + "02\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "06" + "\t0\t" + key_start + name + c + "03\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "06" + "\t0\t" + key_start + name + c + "04\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "06" + "\t0\t" + key_start + name + c + "05\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"

        print key_start + name + c + "07" + "\t0\t" + key_start + name + c + "06\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "08" + "\t0\t" + key_start + name + c + "06\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "09" + "\t0\t" + key_start + name + c + "06\t1\t1\t0\t0\t" + "REQUIRED"
        print key_start + name + c + "10" + "\t0\t" + key_start + name + c + "06\t1\t1\t0\t0\t" + "REQUIRED"

        print key_start + name + c + "11" + "\t0\t" + key_start + name + c + "07\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "11" + "\t0\t" + key_start + name + c + "08\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "11" + "\t0\t" + key_start + name + c + "09\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"
        print key_start + name + c + "11" + "\t0\t" + key_start + name + c + "10\t1\t1\t0\t0\t" + "SUBSET_REQUIRED"

    sys.stdout = character_skill_nodes
    blap = [ ["4","_battle_"], ["5","_campaign_"],]

    if (self == True) and (magic == False):
        blap.append(["2","_self_"])
    elif (magic == True) and (self == False):
        blap.append(["2","_magic1_"])
    elif (magic == True) and (self == True):
        blap.append(["1","_magic1_"])
        blap.append(["2","_self_"])

    for b in blap:
        for i in range(11):
            res = "placeholder_skill" + "\twh_main_skill_node_set_" + name + "\t\t" + b[0]
            res += "\t" + key_start + name + b[1]
            res += two_dig_int(i+1) + "\t"
            res +=  str(i) + "\t" + subculture + "\t0\t"
            if i in {5,10}:
                res += "4"
            else:
                res += "0"
            res += "\tTRUE"
            print res

    for i in range(3):
        res = "placeholder_skill" + "\twh_main_skill_node_set_" + name + "\t\t" + "6"
        res += "\t" + key_start + name + "_innate_"
        res += two_dig_int(i+1) + "\t"
        res +=  str(i) + "\t" + subculture + "\t0\t0\tTRUE"
        print res

    sys.stderr.write(str(unique))
    for i in range(unique):
        res = "placeholder_skill" + "\twh_main_skill_node_set_" + name + "\t\t" + "0"
        res += "\t" + key_start + name + "_unique_"
        res += two_dig_int(i+1) + "\t"
        res +=  str(i) + "\t" + subculture + "\t0\t0\tTRUE"
        print res
