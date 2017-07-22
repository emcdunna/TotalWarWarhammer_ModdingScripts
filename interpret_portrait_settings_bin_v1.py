import sys
import mmap
import string

with open("portrait_settings__core.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(),0)
    letter_set = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "_-" + """/\."""
    sys.stderr.write("Letter set: " + str(letter_set) + "\n")
    newlines = {'0a'}
    reading_chars = False
    for i in range(200):
        ln =  mm.readline()
        #sys.stdout.write(str(ln))
        total_length = len(ln)
        for i in range(total_length):
            char = ln[i]
            if "{0:02x}".format(ord(char)) in newlines:
                sys.stdout.write("\n")
            elif (char not in letter_set) or (char == "") or (char == " "):
                if reading_chars == True:
                    sys.stdout.write("|:>  ")
                reading_chars = False
                sys.stdout.write( "" + "{0:02x}".format(ord(char)) + "" )
            else:
                if reading_chars == False:
                    sys.stdout.write("  <:|")
                reading_chars = True
                sys.stdout.write( char )

a = """
for line in sys.stdin:
    word = ""
    for char in line:
        word = word + char + "\t" + "{0:02x}".format(ord(char)) + "\n"
    print word
""" # this is the old way
