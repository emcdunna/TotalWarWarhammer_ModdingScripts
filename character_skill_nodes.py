
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

for line in sys.stdin:
    inputs = split_line_tsv(line)
    name = inputs[0]

    key_start = "wh_main_skill_node_"

    cap = ["","",""]
    cap[0] = "_battle_"
    cap[1] = "_campaign_"
    cap[2] = "_self_"

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
