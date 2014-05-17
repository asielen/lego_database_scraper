from z_junk import get_set

__author__ = 'andrew.sielen'


def read_testfileAdd():

    with open("../Sets.txt", encoding='utf-8', errors='ignore') as f:
        set_list = f.readlines()
    set_list = set_list[3:]
    current_set = ""
    counter = 1
    total = len(set_list)
    for set in set_list:
        current_set = set.split("\t")[-2]
        print("{"+str(counter)+"/"+str(total)+"} "+"Getting info on "+current_set)
        get_set.get_basestats(current_set.strip(), verbose=0)
        get_set.get_pieces(current_set.strip(), verbose=0)
        counter+=1

read_testfileAdd()