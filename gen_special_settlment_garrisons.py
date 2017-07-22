import sys

altdorf = ["altdorf",5,12,"emp","vmp","brt"]
kislev = ["kislev",5,12,"emp","vmp","brt","ksl"]
miragliano = ["miragliano",5,12,"emp","vmp","brt","teb"]
black = ["black_crag",5,12,"grn","dwf"]
drakenhof = ["castle_drakenhof",5,12,"emp","brt","vmp"]
couronne = ["couronne",5,12,"emp","brt","vmp"]
karaz_a_karak = ["karaz_a_karak",5,12,"dwf","grn"]
main = [altdorf,kislev,miragliano,black,couronne,drakenhof,karaz_a_karak]

dct = {}
dct["emp"] = "emp.txt"
dct["vmp"] = "vmp.txt"
dct["brt"] = "brt.txt"
dct["ksl"] = "emp.txt"
dct["teb"] = "emp.txt"
dct["grn"] = "grn.txt"
dct["dwf"] = "dwf.txt"

i = 70000
for lst in main:
    for itr in range(lst[1]):
        for off in range(6):
            try:
                fact = lst[3 + off]
            except:
                pass
            else:
                fct_file = open(dct[fact],'r')
                unit_list = []
                for line in fct_file:
                    unit_list.append(line)
                for unt in range(lst[2] + itr):
                    i = i + 1
                    word = "wh_main_special_settlement_" + lst[0] + "_" + str(itr + 1) + "_" + fact
                    sys.stdout.write( word + "\t" + "0\t" + unit_list[unt] )

                    # str(i) + "\t" + 
