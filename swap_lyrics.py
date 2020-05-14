import random
import itertools
import string
import rhymes_and_more as vm  
import pronouncing
import re
import copy
lyrics = ""

def break_down_list(a_list):
    # https://stackoverflow.com/questions/18406776/split-a-string-into-all-possible-ordered-phrases
    ns = range(1, len(a_list)) # n = 1..(n-1)
    for n in ns: # split into 2, 3, 4, ..., n parts.
        for idxs in itertools.combinations(ns, n):
            yield [' '.join(a_list[i:j]) for i, j in zip((0,) + idxs, idxs + (None,))]

with open("google-10000-english-usa-mod.txt", "rt") as f:
	#gwl_num is the number of words to take from list 
	#smaller number, less obscure words will be
	#Also, removed some words
	gwl_num = 2000 
	google_word_list = [next(f) for x in range(gwl_num)]
	google_word_list = [w.rstrip() for w in google_word_list]

with open("lyrics_short.txt", "rt") as f:
	words = []
	exceptions = ["a", "an", "the", " ", ""]
	lyrics = f.readlines()
	
	lyrics = list(((line.replace("-", " ")).rstrip()) for line in lyrics)
	lyrics = list(re.sub("[^a-zA-Z ']","",line) for line in lyrics)
	line_splits = list(line.split(" ") for line in lyrics)
	new_lyrics = ""
	print("LYRICS (try unique lines only for efficiency):")
	for l in lyrics:	
		print(l)
	#get unique words
	for line in lyrics:
		line = line.replace("-", " ")
		line_split = line.split(" ")
		new_lyrics += line +"\n"
		for w in line_split:
			if w not in words and w not in exceptions:
				words.append(w)
	print("\nFirst we can just try replacing each word with a rhyme\n")
	new_words = []
	for w in words:
		phones = vm.first_phones_for_word(w)
#		print("WORD " + w + " PHONES: " + phones)
		syllable_num = pronouncing.syllable_count(phones)
		sim_words = []		
		step_out_timer = 0
		while len(sim_words) == 0:
			#note: multiple functions you could replace "near_rhyme" with
			sim_words_unfilt = vm.near_rhyme(w, phones=phones, stress=True)
			sim_words_unfilt = list(set(sim_words_unfilt).intersection(google_word_list))
			for sw in sim_words_unfilt:
				phones_sw = vm.first_phones_for_word(sw)
				syllable_num_sw = pronouncing.syllable_count(phones_sw)
				if sw != w:
					if syllable_num_sw == syllable_num:
						sim_words.append(sw)
			step_out_timer += 1
			if step_out_timer > 100:
				sim_words.append(w)
		new_w = random.choice(sim_words)
		new_words.append(new_w)
	
#	print("NEW WORDS:")
#	print(new_words)	
	i = 0	
	for nw in new_words:
		pattern = r"\b%s\b" % words[i]
		new_lyrics = re.sub(pattern, nw, new_lyrics)
#		lyrics = lyrics.replace(words[i], nw)
		i += 1
	print("LYRICS, REPLACED WITH RHYMES:\n")
	print(new_lyrics)

	print("Now try something more interesting... (this will take awhile)\n")
	#getting the phones for lyric lines
	phones_for_lines_split = []
	phones_for_lines = []
	for ls in line_splits:
		p4l = list(pronouncing.phones_for_word(word)[0] for word in ls)
		phones_for_lines.append(p4l)
		phones_split = []
		for p in p4l:
			for s in p.split(" "):
				phones_split.append(s)
		phones_for_lines_split.append(phones_split)	
	new_phones_for_lyrics = []
	new_lyrics = []
	# line by line
	for p4l_split in phones_for_lines_split:
		line_syl_cnt = pronouncing.syllable_count(" ".join(p4l_split))
		#combinations of ways to group phonemes into words
		p4l_combos = list(break_down_list(p4l_split))		
		random.shuffle(p4l_combos)
		new_words_for_line = []
#		print("combo count: ", len(p4l_combos))
#		combo_count = 0
		#p4l is list of phones string for
		for p4l in p4l_combos:
			#word/phones by word/phones
			for phones in p4l:
				#see if we can find new similar word for phones
				new_word = vm.sim_word_for_phones(phones, google_word_list)
				if new_word:
					new_words_for_line.append(new_word)
				else:
					new_words_for_line = []
					break
			if new_words_for_line:
				#want new line to have the same syllables as the old line
				new_line_syl_cnt = 0
				for word in new_words_for_line:
					phones = pronouncing.phones_for_word(word)[0]
					new_line_syl_cnt += pronouncing.syllable_count(phones)
				if new_line_syl_cnt == line_syl_cnt:
#					print("found words for line")
					new_lyrics.append(" ".join(new_words_for_line))
					new_phones_for_line = []
					for w in new_words_for_line:
						new_phones_for_line.append(pronouncing.phones_for_word(w)[0])
					new_phones_for_lyrics.append(new_phones_for_line)
					break
#			combo_count += 1
#			if combo_count == 100:
#				print("looked through 100 combos")
#			elif combo_count == 200:
#				print("200 combos")
#			elif combo_count == 300:
#				print("300 combos...")
#			elif combo_count == 500:
#				print("500")
#			elif combo_count == 1000:
#				print("1000")

	print("************ COMPARE CONTRAST PHONES ************")
	for i, l in enumerate(new_lyrics):
		print("OLD:")
		print(lyrics[i])
		print(phones_for_lines[i])
		print("NEW:")
		print(l)
		print(new_phones_for_lyrics[i])
	print("*************************************************\n")
	print("LYRICS, PHONETIC MIX:\n")
	for l in new_lyrics:
		print(l)
