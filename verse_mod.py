import random
import string
import pronouncing
import re
import itertools
import numpy as np

"""
    Web links for more information:
    http://www.speech.cs.cmu.edu/cgi-bin/cmudict
    https://en.wikipedia.org/wiki/Arpabet
    https://en.wikipedia.org/wiki/Rhyme
    https://en.wikipedia.org/wiki/Perfect_and_imperfect_rhymes
    https://en.wikipedia.org/wiki/Assonance
    https://www.litcharts.com/literary-devices-and-terms/slant-rhyme
 """

def consonant_clusters():
    """ Return a list of possible English consonant clusters."""
    """
    See the following resources for more information on consonant clusters.
    "consonant cluster: "a group of consonants which have no intervening vowel"
        https://en.wikipedia.org/wiki/Consonant_cluster
    "Two Theories of Onset Clusters", Duanmu
        http://www-personal.umich.edu/~duanmu/CR02.pdf
    "Phoneme distribution and syllable structure of entry words in the CMU
    English Pronouncing Dictionary", Yang
        http://fonetiks.info/bgyang/db/201606cmu.pdf
    "Blends, Digraphs, Trigraphs, and Other Letter Combinations"
        https://www.enchantedlearning.com/consonantblends/
    """
    return ['F W', 'F R', 'F L', 'S W', 'S V',
            'S R', 'S L', 'S N', 'S M', 'S F',
            'S P', 'S T', 'S K', 'SH W', 'SH R',
            'SH L', 'SH N', 'SH M', 'TH W', 'TH R',
            'V W', 'V R', 'V L', 'Z W', 'Z L',
            'B W', 'B R', 'B L', 'D W', 'D R',
            'G W', 'G R', 'G L', 'P W', 'P R',
            'P L', 'T W', 'T R', 'K W', 'K R',
            'K L', 'L Y', 'N Y', 'M Y', 'V Y',
            'H Y', 'F Y', 'S Y', 'TH Y', 'Z Y',
            'B Y', 'D Y', 'G Y', 'P Y', 'T Y',
            'K Y', 'S P L', 'S P R', 'S T R',  'S K R',
            'S K W']


def check_if_consonant_cluster(phones):
    """Return True if CMUdict phonemes is a consonant cluster."""
    return phones in consonant_clusters()


def check_if_vowel(phone):
    """Returns True if CMUdict phoneme is a vowel."""
    # all vowels in CMU Pronouncing Dictionary have stress number 0-2
    return phone[-1] in '012'


def check_if_stressed_vowel(phone):
    """Returns True if CMUdict phoneme is a stressed vowel."""
    # 1 or 2 indicate vowel is stressed
    return phone[-1] in '12'


def check_if_non_stressed_vowel(phone):
    """Returns True if CMUdict phoneme is a non-stressed vowel."""
    # 0 indicates vowel is unstressed
    return phone[-1] in '0'


def check_if_consonant(phone):
    """Returns True if CMUdict phoneme is a consonant."""
    # consonants do not have any stress number
    return phone[-1] not in '012'

def unique(data_list):
    """Removes duplicates from a list, i.e. just unique elements."""
    return list(dict.fromkeys(data_list))


def all_the_same(data_list, val):
    """Returns true if all elements in data_list at equal to val"""
    if len(data_list) > 0 and len(data_list) == data_list.count(val):
        return True
    else:
        return False

def random_phones_for_word(word):
    """Chooses random set of CMUdict phonemes for word

    :param word: a word
    :return: CMUdict phonemes string
    """
    all_phones = pronouncing.phones_for_word(word)
    if not all_phones:
        return ""
    phones = random.choice(all_phones)
    return phones

def first_phones_for_word(word):
    """Chooses first set of CMUdict phonemes for word

    :param word: a word
    :return: CMUdict phonemes string
    """
    all_phones = pronouncing.phones_for_word(word)
    if not all_phones:
        return ""
    phones = all_phones[0]
    return phones

def rhyme(word, phones=None, syllable_num=0):
    """ Returns a list of rhymes for a word.

    The conditions for this 'normal' rhyme between words are:
    (1) last stressed vowel and subsequent phonemes match
    If phones argument not given, phones/pronunciation used will default to the
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.

    This is the 'default' rhyme, same definition used by the pronoucning
    module for its 'rhymes' function. This is also like the shared set of
    perfect and identical rhymes, except the identical word will be removed
    from the returned rhymes list.


    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :return: a rhyme for word
    """
    
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for " + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    if syllable_num <= 0:
        syllable_num = pronouncing.syllable_count(phones)
    return [
        w for w in
        pronouncing.rhyme_lookup.get(pronouncing.rhyming_part(phones), [])
        if (w != word)]



def perfect_rhyme(word, phones=None):
    """ Returns a list of perfect rhymes for a word.

    The conditions for a perfect rhyme between words are:
    (1) last stressed vowel and subsequent phonemes match
    (2) onset of last stressed syllable is different
    If phones argument not given, phones/pronunciation used will default to the 
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.


    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :return: a list of perfect rhymes for word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    perf_and_iden_rhymes = rhyme(word, phones)
    identical_rhymes = identical_rhyme(word, phones)
    perfect_rhymes = list(np.setdiff1d(perf_and_iden_rhymes, identical_rhymes))
    if word in perfect_rhymes:
        perfect_rhymes.remove(word)
    return perfect_rhymes


def identical_rhyme(word, phones=None):
    """ Returns identical rhymes of word.

    The conditions for an identical rhyme between words are:
    (1) last stressed vowel and subsequent phonemes match
    (2) onset of last stressed syllable is the same
        e.g. 'leave' and 'leave', or 'leave' and 'believe'
    If phones argument not given, phones/pronunciation used will default to the 
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.

    The identical part of the word doesn't have to be a 'real' word.
    e.g. The phonemes for 'vection' will be used to find identical rhymes
    of 'convection' (e.g. advection) even though 'vection' is unusual/obscure.


    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :return: a list of identical rhymes for word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")

    phones_list = phones.split()
    search_list = []
    for i in range(len(phones_list)-1, -1, -1):
        phone = phones_list[i]
        if check_if_stressed_vowel(phone) is False:
            search_list.append(phone)
        else:
            search_list.append(phone)
            last_stressed_vowel_at_start = (i == 0)
            if last_stressed_vowel_at_start is True:
                search_list.reverse()
                search = ' '.join(search_list)
                rhymes = pronouncing.search(search + "$")
                return rhymes
            else:
                consonant_cnt = 0
                consonants= ""
                search_start = ""
                for j in range(i, 0, -1):
                    next_phone = phones_list[j-1]
                    if check_if_consonant(next_phone) is True:
                        consonant_cnt += 1
                        if consonant_cnt > 1:
                            consonants = next_phone + " " + consonants
                            if check_if_consonant_cluster(consonants):
                                search_list.append(next_phone)
                            else:
                                break
                        else:
                            consonants = next_phone
                            search_list.append(next_phone)
                    else:
                        if consonant_cnt == 0:  # null onset
                            # Regex: vowel (AA1, EH0, ect.) or start '^'
                            # pretty sure all vowel start two letters...
                            #   (would be "((.{1,2}(0|1|2) )|^)" otherwise)
                            search_start = "((..(0|1|2) )|^)"
                        break
                search_list.reverse()
                search = search_start + ' '.join(search_list) + "$"
                rhymes = pronouncing.search(search)
                rhymes = unique(rhymes)
                # for r in rhymes:
                #     print(pronouncing.phones_for_word(r)[0])
                return rhymes



def near_rhyme(word, phones=None, stress=True, consonant_tail=0):
    """ Returns a list of words that almost rhyme

    The conditions for a near rhyme between words are:
    (1) At least one of the phonemes after and including the last stressed
        syllable match, except for the case where they all do.
    If phones argument not given, phones/pronunciation used will default to the
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.


    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :param stress: if vowels will match stress (default True)
    :param consannt_tail: number of
    :return: a list of near rhymes for word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for" + word)
    if not phones:
        raise ValueError("phonemes string is empty")

    rp = pronouncing.rhyming_part(phones)
    search_combos = wildcard_mix_phones_regex_searches(rp, stress)
    rhymes = []
    for search in search_combos:
        rhymes += pronouncing.search(
            search + "( .{1,3}){0," + str(consonant_tail) + "}$")
    if rhymes:
        rhymes = unique(rhymes)
        if word in rhymes:
            rhymes.remove(word)
        return rhymes
    print("random general rhyme: tried all combos, didn't find anything!")
    return []

def assonance_slant_rhyme(word, phones=None):
    """ Returns slant rhymes defined by assonance i.e. matching vowels.

    The conditions for an assonance slant rhyme between words are:
    (1) The last stressed vowel and subsequent phonemes match all vowels.
    If phones argument not given, phones/pronunciation used will default to the 
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.

    Slant rhymes seems to have various different meanings. I went ahead and set
    the condition of having to have ALL the same vowels and different
    consonants or vice versa.

    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :return: a list of assonance slant rhymes for word
    """

    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    phones_list = phones.split()
    search_list = []
    for i in range(len(phones_list)-1, -1, -1):
        phone = phones_list[i]
        if check_if_non_stressed_vowel(phone):
            search_list.append(phone[:2]+'.')
        elif check_if_stressed_vowel(phone):
            search_list.append(phone[:2]+'.') #ignore stress
            search_list.reverse()
            search = ' '.join(search_list)
            rhymes = pronouncing.search(search + "$")
            rhymes = unique(rhymes)
            if word in rhymes:
                rhymes.remove(word)
            return rhymes
        elif check_if_consonant(phone):
            search_list.append('.{1,3}')
    return []


def consonance_slant_rhyme(word, phones=None):
    """ Returns slant rhymes defined by consonance i.e. matching consonants.

    The conditions for a consonance slant rhyme between words are:
    (1) The last stressed vowel and subsequent phonemes match all consonants.
    If phones argument not given, phones/pronunciation used will default to the 
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.

    Slant rhymes seems to have various different meanings. I went ahead and set
    the condition of having to have ALL the same vowels and different
    consonants or vice versa.

    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :return: a list consonance slant rhymes for word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    phones_list = phones.split()
    search_list = []
    for i in range(len(phones_list)-1, -1, -1):
        phone = phones_list[i]
        if check_if_stressed_vowel(phone):
            search_list.append('.{1,3}')
            if all_the_same(search_list, '.{1,3}') is True:
                break
            search_list.reverse()
            search = ' '.join(search_list)
            rhymes = pronouncing.search(search + "$")
            rhymes = unique(rhymes)
            if word in rhymes:
                rhymes.remove(word)
            return rhymes
        elif check_if_non_stressed_vowel(phone):
            search_list.append('.{1,3}')
        elif check_if_consonant(phone):
            search_list.append(phone)
    return []


def random_general_rhyme(word, phones=None, search_option="end"):
    """ Return a list of rhymes where a random combination of phonemes match
    
    The conditions for a general rhyme between words are:
    (1) Any possible phonetic similarity between the final stressed vowel and
        subsequent phonemes.
    If phones argument not given, phones/pronunciation used will default to the
    first in the list of phones returned for word. If no rhyme is found, an
    empty list is returned.


    :param word: a word
    :param phones: specific CMUdict phonemes string for word (default None)
    :param search_option option for regex search. (default "end")
    :return: a list of rhymes for word, where specific rhyme is random
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    rp = pronouncing.rhyming_part(phones)
    search_combos = wildcard_mix_phones_regex_searches(rp)
    while search_combos:
        search = random.choice(search_combos)
        if search_option == "end":
            rhymes = pronouncing.search(search + "$")
        elif search_option == "begin":
            rhymes = pronouncing.search("^" + search)
        elif search_option == "whole":
            rhymes = pronouncing.search("^" + search + "$")
        else:
            raise ValueError("search_option should be 'end', 'begin', or 'whole'")
        if rhymes:
            rhymes = unique(rhymes)
            if word in rhymes:
                rhymes.remove(word)
            return rhymes
        else:
            search_combos.remove(search)
    print("random general rhyme: tried all combos, didn't find anything!")
    return []


def random_match_phones(word, phones=None):
    """Returns words that match a random combination of phonemes

    This is like a random general rhyme, however instead of just the
    last syllable portion, it's the entire word.

    :param word: word that should be in the CMU Pronouncing Dictionary
    :param phones: specific phonemes to rhyme with (default None)
    :return: a word that shares a random combinations of phonemes
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError("phonemes and word don't match")
    if not phones:
        raise ValueError("phonemes string is empty")
    search_list = wildcard_mix_phones_regex_searches(phones)
    while search_list:
        search = random.choice(search_list)
        rhymes = pronouncing.search(search)
        if rhymes:
            rhymes = unique(rhymes)
            if word in rhymes:
                rhymes.remove(word)
            return rhymes
        else:
            search_list.remove(search)
    print("random general match phones: tried all combos, didn't find anything!")
    return []


def assonance(word, phones=None, search_direction=None, match_limit=None):
    """Returns words that have assonance

    :param word: word that should be in the CMU Pronouncing Dictionary
    :param phones: specific phonemes to rhyme with (default None)
    :return: a word that has repition of vowel sounds to input word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError(phones + " not phones for +" + word)
    if not phones:
        raise ValueError("phonemes string is empty")
    phones_list = phones.split()
    if search_direction == "backward":
        phones_list.reverse()
    search_list = []
    match_cnt = 0
    for phone in phones_list:
        if check_if_consonant(phone):
            search_list.append('.')
        elif check_if_vowel(phone):
            search_list.append(phone)
            match_cnt += 1
            if (match_limit is not None) and (match_cnt == match_limit):
                break
    if search_direction == "backward":
        search = ' '.join(search_list.reverse()) + "$"
    elif search_direction == "forward":
        search = "^" + ' '.join(search_list)
    else:
        search = ' '.join(search_list)

    rhymes = pronouncing.search(search)
    rhymes = unique(rhymes)
    if word in rhymes:
        rhymes.remove(word)
    return rhymes


def consonance(word, phones=None, search_direction=None, match_limit=None):
    """Returns words that have consonance

    :param word: word that should be in the CMU Pronouncing Dictionary
    :param phones: specific phonemes to rhyme with (default None)
    :return: a word that has repition of consonance sounds to input word
    """
    if phones is None:
        phones = first_phones_for_word(word)
        if phones == "":
            return []
    else:
        if phones not in pronouncing.phones_for_word(word):
            raise ValueError("phonemes and word don't match")
    if not phones:
        raise ValueError("phonemes string is empty")
    phones_list = phones.split()
    if search_direction == "backward":
        phones_list.reverse()
    search_list = []
    match_cnt = 0
    for phone in phones_list:
        if check_if_vowel(phone):
            search_list.append('.{1,3}')
        elif check_if_consonant(phone):
            search_list.append(phone)
            match_cnt += 1
            if (match_limit is not None) and (match_cnt == match_limit):
                break
    if search_direction == "backward":
        search = ' '.join(search_list.reverse()) + "$"
    elif search_direction == "forward":
        search = "^" + ' '.join(search_list)
    else:
        search = ' '.join(search_list)

    rhymes = pronouncing.search(search)
    rhymes = unique(rhymes)
    if word in rhymes:
        rhymes.remove(word)
    return rhymes


def alliteration(word):
    return consonance(word, "start", 1)

def wildcard_mix_phones_regex_searches(phones, stress=False):
    """Generates all combinations of regex strings where phoneme in 'phones' is a wildcard ('.')

    e.g. ['HH IY1 R'],['HH IY1 .{1,3}'],['HH .{1,3} R'],
        ['.{1,3} IY1 R'], ...['.{1,3} .{1,3} .{1,3}']


    :param phones: CMU Pronouncing Dictionary phonemes string
    :param stress: if stress portion of vowel is included or nont (a '.')
    :return: list of regex search strings where phonemes replaced with wildcard
    """
    phones_list = phones.split()
    product_factors = []
    for phone in phones_list:
        flist = ['.{1,3}']
        if stress is False and check_if_vowel(phone):
            flist.append(phone[:2]+'.')  # ignore stress
        else:
            flist.append(phone)
        product_factors.append(flist)
    combos = list(itertools.product(*product_factors))
    combos.remove(combos[0])  # should be case where ['.', '.', ... '.']
    search_combos = [' '.join(list(item)) for item in combos]
    return search_combos

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

def rhyme_type_random(word):
    rhyme_types = ['perfect', 'identical', 'random_match_phones', 'random_general',
                   'assonance', 'consonance', 'slant_assonance', 'slant_consonance']
    rhymes = []
    while rhyme_types:
        rt = random.choice(rhyme_types)
        if rt == 'perfect':
            rhymes = perfect_rhyme(word)
        elif rt == 'identical':
            rhymes = identical_rhyme(word)
        elif rt == 'random_match_phones':
            rhymes = random_match_phones(word)
        elif rt == 'random_general':
            rhymes = random_general_rhyme(word)
        elif rt == 'assonance':
            rhymes = assonance(word)
        elif rt == 'consonance':
            rhymes = consonance(word)
        elif rt == 'slant_assonance':
            rhymes = assonance_slant_rhyme(word)
        elif rt == 'slant_consonance':
            rhymes = consonance_slant_rhyme(word)
        if rhymes:
            a_rhyme = random.choice(rhymes)
            return a_rhyme
        else:
            rhyme_types.remove(rt)
    return []
