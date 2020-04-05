import random
import string
import verse_mod as vm  
import pronouncing

def rand_rhyme_scheme():
    schemes = []
    # scheme = []
    schemes.append(['A', 'A'])
    schemes.append(['A', 'B', 'A'])
    schemes.append(['A', 'B', 'A', 'B'])
    schemes.append(['A', 'A', 'B', 'B'])
    schemes.append(['A', 'A', 'B', 'A'])
    schemes.append(['A', 'B', 'A', 'C'])
    scheme = random.choice(schemes)
    # ss_num = random.choice([2,3])
    # for s in range(0, ss_num):
    #     rand_subscheme = random.choice(subschemes)
    #     for ss in rand_subscheme:
    #         scheme.append(ss)
    return scheme

def define_scheme_traits(word_list):
    Asyl = int(max(4, random.gauss(6, 1)))
    Arhym  = random.choice(word_list).rstrip()
    Adict = {'syl': Asyl, 'rhym': Arhym}

    Bsyl = int(max(4, random.gauss(Asyl, 1)))
    Brhym  = random.choice(word_list).rstrip()
    Bdict = {'syl': Bsyl, 'rhym': Brhym}

    Csyl = int(max(4, random.gauss(Asyl, 1)))
    Crhym  = random.choice(word_list).rstrip()
    Cdict = {'syl': Csyl, 'rhym': Crhym}

    scheme_traits = {'A': Adict, 'B': Bdict, 'C': Cdict}
    return scheme_traits

def generate_line(syllable_number, rhyme_word, word_list):
    phones = pronouncing.phones_for_word(rhyme_word)
    phone = random.choice(phones)
    rhyme_syllabi_count = pronouncing.syllable_count(phone)
    line_syllabi_count = rhyme_syllabi_count
    line = rhyme_word
    timeout_counter = 0
    # print("in line syllabi count loop")
    while line_syllabi_count != syllable_number:
        over_limit = (line_syllabi_count > syllable_number)
        timeout = (timeout_counter > 100000)
        # print(line_syllabi_count)
        # print(syllable_number)
        # print(timeout_counter)
        # print(timeout_counter > 100000)
        # print(over_limit)
        # print(over_limit and timeout)
        if over_limit is False:
            word = random.choice(word_list).rstrip()
            phones = pronouncing.phones_for_word(word)
            if len(phones) != 0:
                word_syllabi_count = pronouncing.syllable_count(phone)
                line_syllabi_count += word_syllabi_count
                line = word + " " + line
        elif over_limit:
            if timeout:
                return line
            line_syllabi_count = rhyme_syllabi_count
            line = rhyme_word

        timeout_counter += 1
    return line

#=====================================================
print("computer, give me some of your") 
print("finest verse!\n")
print("\n        OKAY VERSE COMING UP\n")

verse = ""
letters = string.ascii_lowercase
line_length = int(max(0, random.gauss(500, 20)))
for l in range(0, line_length):
	verse += random.choice(letters)
verse += '\n'
verse = verse.rstrip()
print("~*~ ~*~ ~*~ ｖｅｒｓｅ ~*~ ~*~ ~*~")
print(verse)
print("~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~")

#=====================================================
print("\nvery funny, how about something") 
print("less random?\n")
print("         LESS RANDOM COMING UP\n")

verse = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(3, 1)))
for s in range(0,structure_num):
    struct_line_num = int(max(1, random.gauss(5, 2)))
    for l in range(0,struct_line_num):
        word_count = int(max(0, random.gauss(5, 1)))
        for w in range(0,word_count):
            # word_length = random.randint(1,12)
            word_length = int(max(0, random.gauss(4, 2)))
            word = ""
            for l in range(0, word_length):
                letter = random.choice(letters)
                word += letter
            verse += word + " "
        verse += "\n"
    verse += "\n"
verse = verse.rstrip()
print("~*~ ~*~ ~*~ ｖｅｒｓｅ ~*~ ~*~ ~*~")
print(verse)
print("~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~")
#=====================================================
print("\nno! actual words.\n")
print("                         OKAY.\n")

#note: google word list in order from most frequently used to least
with open("google-10000-english-usa-mod.txt", "rt") as f:
	#the number of words take from list 
	#smaller number, less obscure words will be
	gwl_num = 1000 
	google_word_list = [next(f) for x in range(gwl_num)]
google_word_list = [w.rstrip() for w in google_word_list]
verse = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(4, 1)))
for s in range(0, structure_num):
	struct_line_num = int(max(1, random.gauss(5, 2)))
	for l in range(0, struct_line_num):
		word_count = int(max(0, random.gauss(5, 1)))
		for w in range(0,word_count):
			word = random.choice(google_word_list).rstrip()
			verse += word + " "
		verse += "\n"
	verse += "\n"
verse = verse.rstrip()
print("~*~ ~*~ ~*~ ｖｅｒｓｅ ~*~ ~*~ ~*~")
print(verse)
print("~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~")
#=====================================================
print("\nokay, now make it rhyme a bit?\n")
print("                         SURE.\n")
introduction = ""
chorus = []
bridge = ""
end = ""
# random_verse()
cmu_word_list = pronouncing.search(".")
list_intersect = list(set(cmu_word_list).intersection(google_word_list))
verse_schemes = []
subscheme_num = int(max(1, random.gauss(3, 1)))
for sn in range(0, subscheme_num):
	scheme = rand_rhyme_scheme()
	scheme_traits = define_scheme_traits(list_intersect)
	line_num = len(scheme)
	repeat_num = random.choice([1, 3])
	for rn in range(0, repeat_num):
		scheme_lines = []
		for ln in range(0, line_num):
			letter = scheme[ln]
			sylb_num = scheme_traits[letter]['syl']
			rhyme_word = scheme_traits[letter]['rhym']
			timeout_cnt = 0
			new_rw_list = []
			while len(new_rw_list) == 0:
				new_rw_list = vm.random_general_rhyme(rhyme_word)
				new_rw_list = list(set(list_intersect).intersection(new_rw_list))
				timeout_cnt += 1
				if timeout_cnt > 10:
					new_rw_list.append(rhyme_word)
			new_rw = random.choice(new_rw_list)
			line = generate_line(sylb_num, new_rw, list_intersect)
			scheme_lines.append(line)
		verse_schemes.append(scheme_lines)

f.closed
verse = ""
for scheme_lines in verse_schemes:
	for l in scheme_lines:
		verse += l + '\n'
	verse += '\n'
verse = verse.rstrip()
print("~*~ ~*~ ~*~ ｖｅｒｓｅ ~*~ ~*~ ~*~")
print(verse)
print("~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~ ~*~")
#=====================================================
print("\ncool, still doesn't make any")
print("sense but it's good enough now.")
print("                          . . .\n")

