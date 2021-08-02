#!/usr/bin/env python3

import os
import secrets
import string
import numpy as np

LOC_DEFAULT = "/home/username/Documents/"


def make_wordlist(the_loc):
    replacers = ["1", "2", "3", "4", "5", "6", " ", "\t", "\r", "\n"]
    word_banks = dict()
    sets = [a_file for a_file in os.listdir(the_loc) if "wordlist" in a_file]
    for a_file in sets:
        with open(f"{the_loc}{a_file}", "r") as r_file:
            for line in r_file:
                for replacer in replacers:
                    line = line.replace(replacer, "")
                key = len(line)
                if key not in word_banks:
                    word_banks[key] = set()
                word_banks[key].add(line)
    return word_banks


def determine(chr_req):
    # Allowed/Forbidden characters functionality
    specChrs = set(string.punctuation)
    which = input("Allowed or Forbidden? (a/f): ")
    if which.lower() == "f":
        charset = set(input("Forbidden chars (no sep): "))
        # valid = [char for char in string.punctuation if char not in charset]
        valid = specChrs - charset
    elif which.lower() == "a":
        charset = set(input("Allowed chars (no sep): "))
        # valid = [char for char in charset if char in string.punctuation]
        valid = specChrs.intersection(charset)
    elif which.lower() not in ["a", "f"]:
        print("You chose poorly.")
    return "".join(valid)


def begin(wurdz, len_max, num_req, chr_req):
    smallest = min(list(wurdz.keys()))
    best_words = []
    if chr_req:
        chr_req = determine(chr_req)
    while True:
        curr_len = sum([len(word) for word in best_words])
        new_word = roll(wurdz, len_max, curr_len, num_req, chr_req, smallest)
        if new_word == False:
            break
        else:
            best_words.append(new_word)
    return "".join(best_words)


def roll(words, len_max, curr_len, num_req, chr_req, smol):
    pad = (num_req + bool(chr_req))
    gap = (len_max - curr_len - pad)
    chooser = secrets.SystemRandom()
    # If the maximum length of the password is <= the current length of 
    # chosen pw parts, then stop choosing more parts.
    if len_max <= curr_len:
        chosen = False
    # If the smallest word length is <= "gap" (number of remaining chrs)
    # then pick another password part.
    elif smol <= gap:
        usable = [num for num in words.keys() if int(num) <= int(gap)]
        u_totals = [len(words[word]) for word in usable]
        u_totals = [num / sum(u_totals) for num in u_totals]
        c_num = np.random.choice(usable, replace=False, p=u_totals)
        chosen = chooser.choice(list(words[c_num])).capitalize()
    # If the smallest word is larger than "gap" then add special chrs and numbers.
    elif smol > gap:
        rem = []
        if chr_req:
            rem.append(chooser.choice(chr_req))
        if num_req:
            rem.append(chooser.choice(string.digits))
        for num in range(gap):
            rem.append(chooser.choice(string.digits))
        chosen = "".join(rem)
    return chosen


def main():
    length_max = None
    req_nums = None
    req_chrs = None
    word_bank_loc = input("Where are your word banks located?: ")
    if word_bank_loc:
        LOC_DEFAULT = word_bank_loc
    while not isinstance(length_max, int):
        try:
            length_max = int(input("Maximum number of characters?: "))
        except ValueError:
            length_max = 32
    while not isinstance(req_nums, bool):
        req_nums_try = input("Numbers required? (T/F): ")
        req_nums = False if req_nums_try in ["f", "F"] else True
    while not isinstance(req_chrs, bool):
        req_chrs_try = input("Special characters required? (T/F): ")
        req_chrs = False if req_chrs_try in ["f", "F"] else True
    words = make_wordlist(LOC_DEFAULT)
    pw = begin(words, length_max, req_nums, req_chrs)
    print(pw)
    return pw


if __name__ == "__main__":
    main()
