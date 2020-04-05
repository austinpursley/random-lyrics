import random
import string
import verse
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

def random_verse():
    f = open("google-10000-english-usa.txt", "rt")
    google_word_list = f.readlines()
    google_word_list = [w.rstrip() for w in google_word_list]
    cmu_word_list = pronouncing.search(".")
    list_intersect = list(set(cmu_word_list).intersection(google_word_list))
    verse_lines = []
    subscheme_num = random.choice([1, 3])
    for sn in range(0, subscheme_num):
        scheme = rand_rhyme_scheme()
        scheme_traits = define_scheme_traits(list_intersect)
        line_num = len(scheme)
        for ln in range(0, line_num):
            line = scheme[ln]
            sylb_num = scheme_traits[line]['syl']
            rhyme_word = scheme_traits[line]['rhym']
#            new_rw = verse.rhyme_type_random(rhyme_word)
            new_rw_list = verse.perfect_rhyme(rhyme_word)
            if len(new_rw_list) != 0:
                new_rw = random.choice(new_rw_list)
            else:
                new_rw = rhyme_word
            line = generate_line(sylb_num, new_rw, list_intersect)
            verse_lines.append(line)
    print("VERSE:")
    for vl in verse_lines:
        print(vl)
    return

phones = pronouncing.phones_for_word('science')[0]
scnt = pronouncing.syllable_count(phones)
test = verse.rhyme('science',phones=phones, syllable_num=scnt)
print(phones)
print(len(test))
print(len(verse.unique(test)))
# for r in test:
#     print(r)
#     print(pronouncing.phones_for_word(r)[0])


#=====================================================
print("\nGive me random verse!\n")
print("COMPUTER: OKAY RANDOM VERSE COMING UP'\n\n")
verse = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(7, 3)))
for s in range(0,structure_num):
    verse_length = int(max(0, random.gauss(100, 2)))
    for l in range(0, verse_length):
        letter = random.choice(letters)
        verse += letter
print("VERSE:")
print(verse)

#=====================================================
print("\nvery funny. I mean REAL random verse! \n")
verse = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(7, 3)))
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
print("VERSE:")
print(verse)

#=====================================================
print("no! actual words.\n\n")
print("COMPUTER: OKAY USING WORD LIST FROM 'google-10000-english-usa-mod.txt'\n\n")

with open("google-10000-english-usa-mod.txt", "rt") as f:
	google_word_list = [next(f) for x in range(9000)]
google_word_list = [w.rstrip() for w in google_word_list]
verse = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(7, 2)))
for s in range(0, structure_num):
	struct_line_num = int(max(1, random.gauss(5, 2)))
	for l in range(0, struct_line_num):
		word_count = int(max(0, random.gauss(5, 1)))
	for w in range(0,word_count):
		word = random.choice(google_word_list).rstrip()
		verse += word + " "
	verse += "\n"
print("VERSE:")
print(verse)

#=====================================================
print("\nokay, now make it rhyme?")
introduction = ""
chorus = []
bridge = ""
end = ""
# random_verse()

cmu_word_list = pronouncing.search(".")
list_intersect = list(set(cmu_word_list).intersection(google_word_list))
verse_lines = []
subscheme_num = random.choice([1, 3])
for sn in range(0, subscheme_num):
	scheme = rand_rhyme_scheme()
	scheme_traits = define_scheme_traits(list_intersect)
	line_num = len(scheme)
	repeat_num = random.choice([1, 3])
	for rn in range(0, repeat_num):
		for ln in range(0, line_num):
			letter = scheme[ln]
			sylb_num = scheme_traits[letter]['syl']
			rhyme_word = scheme_traits[letter]['rhym']
			new_rw_list = verse.random_general_rhyme(rhyme_word)
			new_rw_list = list(set(list_intersect).intersection(new_rw_list))
			if len(new_rw_list) != 0:
				new_rw = random.choice(new_rw_list)
			else:
				print(rhyme_word + ' is duplicate')
				new_rw = rhyme_word
			line = generate_line(sylb_num, new_rw, list_intersect)
			verse_lines.append(line)
print("VERSE:")
f.closed
for vl in verse_lines:
	print(vl)

