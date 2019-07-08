import random
import string
import pronouncing
import itertools

def rhyme_scheme():
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

def scheme_line_traits(word_list):
    Asyl = int(max(4, random.gauss(6, 1)))
    Arhym  = random.choice(word_list).rstrip()
    Adict = {'syl': Asyl, 'rhym': Arhym}

    Bsyl = int(max(4, random.gauss(6, 1)))
    Brhym  = random.choice(word_list).rstrip()
    Bdict = {'syl': Bsyl, 'rhym': Brhym}

    Csyl = int(max(4, random.gauss(6, 1)))
    Crhym  = random.choice(word_list).rstrip()
    Cdict = {'syl': Csyl, 'rhym': Crhym}

    schm_traits = {'A': Adict, 'B': Bdict, 'C': Cdict}
    return schm_traits

def random_phones_for_word(word):
    all_phones = pronouncing.phones_for_word(word)
    phones = random.choice(all_phones)
    return phones

def perfect_rhyme(word, phones = None):
    """Get words that perfectly rhyme with given word and optional CMUdict phonemes

    Identical to pronouncing's "rhymes" function, but have option to define phonemes

    :param phones:
    :return:
    """
    if phones is None:
        phones = random_phones_for_word(word)
    if len(phones) > 0:
        return [w for w in pronouncing.rhyme_lookup.get(pronouncing.rhyming_part(phones), [])
                if w != word]
    else:
        return []


def assonance_slant_rhyme(word, phones=None):
    if phones is None:
        phones = random_phones_for_word(word)
    phones_list = phones.split()
    search_list = []
    rhymes = []
    for i in range(len(phones_list) - 1, 0, -1):
        if phones_list[i][-1] in '0':
            search_list.append(phones_list[i])
        elif phones_list[i][-1] in '12':
            search_list.append(phones_list[i])
            search_list.reverse()
            search = ' '.join(search_list[(i - 1):])
            rhymes = pronouncing.search(search + "$")
            break
        else:
            search_list.append('.')

    return rhymes


def consonance_slant_rhyme(word, phones=None):
    if phones is None:
        phones = random_phones_for_word(word)
    phones_list = phones.split()
    search_list = []
    search = ''
    rhymes = []
    for i in range(len(phones_list) - 1, 0, -1):
        if phones_list[i][-1] in '0':
            search_list.append('.')
        elif phones_list[i][-1] in '12':
            search_list.append('.')
            search_list.reverse()
            search = ' '.join(search_list[(i - 1):])
            rhymes = pronouncing.search(search + "$")
            break
        else:
            search_list.append(phones_list[i])
    print("SEARCH:" + search)
    return rhymes

def wildcard_mix_phones_search_str(phones):
    phones_list = phones.split()
    #================================
    product_factors = []
    for phone in phones_list:
        flist = ['.']
        flist.append(phone)
        product_factors.append(flist)
    print(product_factors)
    combos = list(itertools.product(*product_factors))
    combos.remove(combos[0])  # should be case where ['.', '.', ... '.']
    search_list = [' '.join(list(item)) for item in combos]
    print(search_list)
    # ===============================
    return search_list

def random_general_rhyme(word, phones=None):
    if phones is None:
        phones = random_phones_for_word(word)
    rp = pronouncing.rhyming_part(phones)
    search_list = wildcard_mix_phones_search_str(rp)
    while len(search_list) != 0:
        search = random.choice(search_list)
        rhymes = pronouncing.search(search + "$")
        if len(rhymes) != 0:
            return rhymes
        else:
            search_list.remove(search)
    rhymes = []
    return rhymes

def random_match_phones(word, phones=None):
    if phones is None:
        phones = random_phones_for_word(word)
    search_list = wildcard_mix_phones_search_str(phones)
    while len(search_list) != 0:
        search = random.choice(search_list)
        rhymes = pronouncing.search(search)
        if len(rhymes) != 0:
            return rhymes
        else:
            search_list.remove(search)
    print("random match phones: tried all combos, didn't find anything!")
    rhymes = []
    return rhymes
    # timeout_timer = 0
    # while True:
    #     search = wildcard_mix_phones_search_str(phones)
    #     rhymes = pronouncing.search(search)
    #     if word in rhymes:
    #         rhymes.remove(word)
    #     if len(rhymes) != 0:
    #         return rhymes
    #     else:
    #         timeout_timer += 1
    #         if timeout_timer > 100:
    #             print("couldn't find wildcard rhyme!")
    #             rhymes.append(word)
    #             return rhymes


def assonance():
    print('later')


def consonance():
    print('later')


def rhyme_type_random(word):
    rhyme_types = ['perfect', 'random_match_phones', 'slant_assonance', 'slant_consonance', 'random_general']
    rhymes = []
    print(word)
    while True:
        rt = random.choice(rhyme_types)
        print(rt)
        if rt == 'perfect':
            rhymes = perfect_rhyme(word)
            # if len(rhymes) == 0:
            #     print(word + " doesn't have perfect rhyme")
            #     rhymes = random_match_phones(word)
        elif rt == 'random_match_phones':
            rhymes = random_match_phones(word)
        elif rt == 'random_general':
            rhymes = random_general_rhyme(word)
        elif rt == 'slant_assonance':
            rhymes = assonance_slant_rhyme(word)
        elif rt == 'slant_consonance':
            rhymes = consonance_slant_rhyme(word)
        if len(rhymes) != 0:
            break
    # print(rhymes)
    rhyme = random.choice(rhymes)
    return rhyme


def rhyme_same_stress(word):
    timeout_timer = 0
    # print('in the stress loop')
    while(True):
        phones = pronouncing.phones_for_word(word)
        phone = random.choice(phones)
        word_stress = pronouncing.stresses(phone)
        rhyme = rhyme_type_random(word)
        phones = pronouncing.phones_for_word(rhyme)
        for phone in phones:
            rhyme_stress = pronouncing.stresses(phone)
            if word_stress == rhyme_stress:
                return rhyme
        print(timeout_timer)
        if timeout_timer == 10:
            return rhyme
        timeout_timer += 1


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
        scheme = rhyme_scheme()
        schm_traits = scheme_line_traits(list_intersect)
        line_num = len(scheme)
        for ln in range(0, line_num):
            ltr = scheme[ln]
            sylb_num = schm_traits[ltr]['syl']
            rhyme_word = schm_traits[ltr]['rhym']
            new_rw = rhyme_type_random(rhyme_word)
            line = generate_line(sylb_num, new_rw, list_intersect)
            verse_lines.append(line)
    print("LYRICS:")
    for vl in verse_lines:
        print(vl)
    return


            # for wc in range(0, word_count):
            #     if wc == (word_count - 1):
            #         rhymes = pronouncing.rhymes(rhyme_word)
            #         if len(rhymes) != 0:
            #             word = random.choice(rhymes)
            #         else:
            #             break
            #     else:
            #         word = random.choice(word_list).rstrip()
            #     phones = pronouncing.phones_for_word(word)
            #     if len(phones) != 0:
            #         phone = random.choice(phones)
            #         word_syllabi_count = pronouncing.syllable_count(phone)
            #         if word_syllabi_count != 0:
            #             line_syllabi_count += word_syllabi_count
            #             line += word + " "
            #         else:
            #             break
            #     else:
            #         break
            # else:
            #     print(str(line_syllabi_count) + " " + str(sylb_num))
            #     if line_syllabi_count == sylb_num:



lyrics = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(7, 3)))
print("\n Give me random lyrics!\n")
for s in range(0,structure_num):
    lyrics_length = int(max(0, random.gauss(100, 2)))
    for l in range(0, lyrics_length):
        letter = random.choice(letters)
        lyrics += letter
print("LYRICS:")
print(lyrics)

print("\n very funny. I mean REAL random lyrics! \n")

lyrics = ""
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
            lyrics += word + " "
        lyrics += "\n"
    lyrics += "\n"
print("LYRICS:")
print(lyrics)

print("no! actual words.\n\n")
print("COMPUTER: OKAY USING WORD LIST YOU GOT FROM ONLINE, 'google-10000-english-usa.txt'\n\n")

f = open("google-10000-english-usa.txt", "rt")
word_list = f.readlines()
lyrics = ""
letters = string.ascii_lowercase
structure_num = int(max(3, random.gauss(7, 2)))
for s in range(0, structure_num):
    struct_line_num = int(max(1, random.gauss(5, 2)))
    for l in range(0, struct_line_num):
        word_count = int(max(0, random.gauss(5, 1)))
        for w in range(0,word_count):
            word = random.choice(word_list).rstrip()
            lyrics += word + " "
        lyrics += "\n"
    lyrics += "\n"
print("LYRICS:")
print(lyrics)

print("\n okay, that's actually funny. what about actual song structure?")
introduction = ""
chorus = []
bridge = ""
end = ""


random_verse()

# CMU Pronouncing Dictionary
# cmu_test = pronouncing.search_stresses("200100")
# for c in cmu_test:
#     print(c)
# word = "permit"
# cmu_rhyme_test = pronouncing.rhymes(word)
# phones = pronouncing.phones_for_word(word)
# main_rp = pronouncing.rhyming_part(random.choice(phones))
# main_rp1 = main_rp.split()[0]
# main_rp2 = main_rp.split()[1]
# print("main")
# print(main_rp1)
# print(main_rp2)
# print("other")
# print(pronouncing.search("^" + main_rp))
# print(pronouncing.search(main_rp + "$"))
# for rw in cmu_rhyme_test:
#     phones = pronouncing.phones_for_word(rw)
#     for p in phones:
#         rp = pronouncing.rhyming_part(p)
#         if main_rp == rp:
#             print(rp)


# word list w/ frequency, from 'most common' and one from genius
# repeated words / key words / home words
# hybrid between totally random and most common / actual lyrics
# make them rhyme
# make them follow some "meter" for songs, to make them sound musical
# or you know get deeper into some previous research on this, as I'm sure it's out there
# sould discuss things like song structure, word frequency, ect.
# man-computer symbiosis solution (feedback)
# machine learning solution

