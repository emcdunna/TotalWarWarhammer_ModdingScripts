import sys
import mmap
import string

with open("NEW_portrait_settings__core.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(),0)
    letter_set = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "_-" + """/\."""
    sys.stderr.write("Letter set: " + str(letter_set) + "\n")
    newlines = {'0a'}
    NUM_LINES_TOTAL = 5
    for line_index in range(500):
        if line_index < NUM_LINES_TOTAL:
            starting_code = ""
            ending_code = ""
            ln =  mm.readline()
            #sys.stdout.write(str(ln))
            total_length = len(ln)
            reading_chars = False
            k_data = ""
            get_len = False
            line_words = []
            if line_index == 0:
                curr_line_offset = 1
                len_char = ln[4]
                NUM_LINES_TOTAL = int("{0:02x}".format(ord(len_char)),16)
            else:
                curr_line_offset = 0
            for char in ln:
                if  ( "{0:02x}".format(ord(char)) == "00"):
                     # ignore any "00" data
                     pass
                elif curr_line_offset < 3:
                    starting_code += "{0:02x}".format(ord(char)) + ""
                    curr_line_offset += 1
                else:
                    if (reading_chars == True):
                        if k < len_int:
                            k_data += char
                        elif k == len_int:
                            k_data += char
                            line_words.append([len_int, k_data])
                            if "art_set" in k_data:
                                get_len = False
                            else:
                                get_len = True
                            k_data = ""
                            reading_chars = False
                        else:
                            sys.stderr.write("WHAT??\n")
                        k = k + 1

                    elif (curr_line_offset == 3) or (get_len == True):
                        # length param
                        length_param = "{0:02x}".format(ord(char))
                        len_int = int(length_param, 16)
                        reading_chars = True
                        get_len = False
                        k = 1
                    else:
                        ending_code += "{0:02x}".format(ord(char)) + ""
                    curr_line_offset += 1
            print starting_code + "\t" + str(line_words) + "\t" + ending_code
