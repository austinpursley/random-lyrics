import random
import itertools
import string
import verse_mod as vm  
import pronouncing
import re
import copy
lyrics = ""

#https://stackoverflow.com/questions/19368375/set-partitions-in-python/30134039#30134039
def partition(number):
    return {(x,) + y for x in range(1, number) for y in partition(number-x)} | {(number,)}

def slice_by_lengths(lengths, the_list):
    for length in lengths:
        new = []
        for i in range(length):
            new.append(the_list.pop(0))
        yield new
def subgrups(my_list):
    partitions = partition(len(my_list))
    permed = []
    for each_partition in partitions:
        permed.append(set(itertools.permutations(each_partition, len(each_partition))))

    for each_tuple in itertools.chain(*permed):
        yield list(slice_by_lengths(each_tuple, copy.deepcopy(my_list)))

def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu,sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu,sigma)
    return a

def sim_words_for_phones(phones):
    if not phones:
        raise ValueError("phonemes string is empty")
    search_list = vm.wildcard_mix_phones_regex_searches(phones)
    while search_list:
        search = random.choice(search_list)
        rhymes = pronouncing.search("^" + search + "$")
        if rhymes:
            rhymes = vm.unique(rhymes)
            return rhymes
        else:
            search_list.remove(search)
    print("random general match phones: tried all combos, didn't find anything!")
    return []

with open("google-10000-english-usa-mod.txt", "rt") as f:
	#the number of words take from list 
	#smaller number, less obscure words will be
	gwl_num = 2000 
	google_word_list = [next(f) for x in range(gwl_num)]
	google_word_list = [w.rstrip() for w in google_word_list]

#with open("lyrics_short.txt", "rt") as f:
#	words = []
#	exceptions = ["a", "an", "the", " ", ""]
#	content = f.readlines()
#	print("First let's get the unique words from the lyrics\n")
#	for line in content:
#		line = line.replace("-", " ")
#		line_split = line.split(" ")
#		lyrics += line
#		line = line.rstrip()
#		for w in line_split:
#			if w not in words and w not in exceptions:
#				w = re.sub("[^a-zA-Z]","",w)
#				words.append(w)
#	print("WORDS:")	
#	print(words)
#	print("First we can try 'currupting' each word, replacing it with one that is phonetically similiar\n")
#	new_words = []
#	for w in words:
#		phones = vm.first_phones_for_word(w)
##		print("WORD " + w + " PHONES: " + phones)
#		syllable_num = pronouncing.syllable_count(phones)
#		sim_words = []		
#		step_out_timer = 0
#		while len(sim_words) == 0:		
#			sim_words_unfilt = vm.random_match_phones(w, phones)
#			sim_words_unfilt = list(set(sim_words_unfilt).intersection(google_word_list))
#			for sw in sim_words_unfilt:
#				phones_sw = vm.first_phones_for_word(sw)
#				syllable_num_sw = pronouncing.syllable_count(phones_sw)
#				if sw != w:
#					if syllable_num_sw == syllable_num:
#						sim_words.append(sw)
#			step_out_timer += 1
#			if step_out_timer > 100:
#				sim_words.append(w)
#		new_w = random.choice(sim_words)
#		new_words.append(new_w)
#	
#	print("NEW WORDS:")
#	print(new_words)	
#	i = 0	
#	for nw in new_words:
#		pattern = r"\b%s\b" % words[i]
#		lyrics = re.sub(pattern, nw, lyrics)
##		lyrics = lyrics.replace(words[i], nw)
#		i += 1
#	print(lyrics)
		
#		print(" NEW: " + new_w)
#		print("OLD: " + str(syllable_num) + " NEW: " + str(syllable_num_sw))
#		print("OLD: " + str(len(new_sim_words)) + " NEW: " + str(len(sim_words)) + '\n')

	print("Then we can try melting the phonetics of a single line and finding words to match within that\n")

with open("lyrics_short.txt", "rt") as f:
	print("First let's get the unique words from the lyrics\n")
	lines = []
	exceptions = ["a", "an", "the", " ", ""]
	content = f.readlines()
	content = list(((line.replace("-", " ")).rstrip()) for line in content)
	content = list(re.sub("[^a-zA-Z ]","",line) for line in content)
	print(content)
	line_splits = list(line.split(" ") for line in content)
	phones_for_lines = []
	for ls in line_splits:
		phones_for_line_split = list(pronouncing.phones_for_word(word)[0] for word in ls)
		p4l = ""
		for p in phones_for_line_split:
			p4l += p + " " 
		p4l = p4l[:-1] # remove space
		phones_for_lines.append(p4l.split(" "))
#	for n, p in enumerate(partition(phones_for_lines[0]), 1):
#    		print(n, sorted(p))

	print("PHONES FOR LINES")
	print(phones_for_lines[0])
#	for i, phone in enumerate(phones_for_lines[0]):
#		phone_choice = random.choice(["change", "same"])
#		if phone_choice == "change":
#			phones_for_lines[0][i] = ".{1,3}"
#	print (phones_for_lines[0])
	p4l_len = len(phones_for_lines[0])
	search_success = False
	while(search_success == False):
		words_for_line = []
		arbtry_mu = int(p4l_len * 0.66)
		arbtry_sig = int(arbtry_mu * 0.3)
		split_num = int(trunc_gauss(arbtry_mu, arbtry_sig, 1, p4l_len))
		split_positions = list(range(1, p4l_len))
		word_splits = random.sample(split_positions, k=split_num)	
		word_splits.sort()

		if word_splits[0] != 1:
			word_splits.insert(0, 1)
		if word_splits[-1] != p4l_len:
			word_splits.append(p4l_len)
	
		for i in range(0, split_num-1):
			start = word_splits[i]
			end = word_splits[i+1]
			phones = " ".join(phones_for_lines[0][start:end])
			matches = sim_words_for_phones(phones)
			matches = vm.unique(matches)
			random.shuffle(matches)
			if matches:
				for m in matches:
					if m in google_word_list:
						words_for_line.append(m)
						print("break1")
						break		
			else:			
				search_success = False
				print("break2")
				break
		
		if (len(words_for_line)-1) == split_num:
			print("this is true, yo fool")
			search_success = True
	print((len(words_for_line)-1))
	print(split_num)
	print(words_for_line)
	
#	partitions = list(subgrups(list(phones_for_lines[0])))
#	random.shuffle(partitions)
#	for new_phones_for_line in partitions:
#		new_words_for_line = []
#		for phones_for_word in new_phones_for_line:
#			brk = False			
#			phones_str = ""
#			for p in phones_for_word:
#				phones_str += p + " "
#			print(phones_str)
#			phones_str = phones_str[:-1] # remove space
#			print(phones_str)
#			search_combos = vm.wildcard_mix_phones_regex_searches(phones_str)
#			random.shuffle(search_combos)
#			for sch in search_combos:
#				matches = pronouncing.search("^" + sch + "$")
#				if matches:
#					matches = vm.unique(matches)
#					random.shuffle(matches)
#					for m in matches:
#						if m in google_word_list:
#							print("WORD FOUND")
#							print(phones_str)
#							print(sch)
#							new_words_for_line.append(random.choice(matches))
#							brk = True
#							break
#					if brk == True:
#						break
#			if brk == True:
#				break
#	print("FINISH")
#	print(new_words_for_line)
#current issues: bug where breaks out loop too early also partition funciton got from stackexchange takes too long. find a new function or do something a little bit more reasonable.
