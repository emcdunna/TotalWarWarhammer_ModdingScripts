import sys
import mmap
import string

new_bin = open("NEW_portrait_settings__core.bin", "wb")

with open("portrait_settings__core.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(),0)
    letter_set = string.ascii_uppercase + string.ascii_lowercase + "0123456789" + "_-" + """/\."""
    sys.stderr.write("Letter set: " + str(letter_set) + "\n")
    NUM_LINES_TOTAL = 1 # default
    line_index = 0
    mm_index = 0
    starting_code = ""
    ending_code = ""
    for char in mm:
        if line_index < NUM_LINES_TOTAL:
            total_length = len(ln)
            reading_chars = False
            k_data = ""
            get_len = False
            total_words = []
            if mm_index == 0:
                len_char = mm[4]
                NUM_LINES_TOTAL = int("{0:02x}".format(ord(len_char)),16)

            new_bin.write(char)
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
                        total_words.append(k_data)
                        if "art_set" in k_data:
                            get_len = False
                            line_index += 1
                        else:
                            get_len = True
                        k_data = ""
                        reading_chars = False
                    else:
                        sys.stderr.write("ERR: line " + str(line_index) + "\n")
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

        mm_index += 1
    print total_words
