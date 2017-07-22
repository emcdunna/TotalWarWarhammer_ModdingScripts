from total_war_module import *

new_bin = open("NEW_portrait_settings__core.bin", "wb")
in_file_bin = "portrait_settings__core.bin"
prefix = "UI/Portraits/Portholes/"
insert_bef_me = "\x1e\x00wh_main_art_set_emp_karl_franz"


# input file holds new contents to put into the portrait settings file
new_items = 0
insert_binary_string = ""
for line in sys.stdin:
	ln_lst = read_line_as_tsv(line)
	for i in range(2,len(ln_lst)):
		if ln_lst[i] != "none":
			ln_lst[i] = prefix + ln_lst[i] + ".png"
	insert_binary_string += create_binary_line(ln_lst)
	new_items += 1

	
# go through every char in the input file
f_ind = 0
temp_buffer = circle_buff_string(len(insert_bef_me))
with open(in_file_bin, "r+b") as p_settings_bin:
	mm = mmap.mmap(p_settings_bin.fileno(),0)
	for ch in mm:
		# takes care of adjusting the file length parameter
		if f_ind == 4:
			num_portraits = string_hex_to_int(char_to_hex_ascii(ch))
			new_portraits = num_portraits + new_items	
			ch = chr(new_portraits)		
			
		f_ind += 1
		if temp_buffer.is_full() == True:
			new_bin.write(temp_buffer.contents[0])

		temp_buffer.add_char(ch)
		
		if insert_bef_me in str(temp_buffer):
			for ins_ch in insert_binary_string:
				new_bin.write(ins_ch)
			
		# testing code
		print temp_buffer

	for new_ch in temp_buffer.contents:
		new_bin.write(new_ch)	
	
	