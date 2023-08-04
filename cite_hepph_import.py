import requests
import os
import sys
import time

s = requests.session()

dates_dir = "dataset/cite-HepPh/pure_txt/cit-HepPh-dates.txt"
links_dir = "dataset/cite-HepPh/pure_txt/cit-HepPh.txt"

dates_file = open(dates_dir, 'r')
_ = dates_file.readline()

count = 0
while True:
    count += 1

    line = dates_file.readline()
    if not line:
        break

    paper_id, date = line.split()
    cross_list = False

    if paper_id[:2] == "11":
        cross_list = True
        paper_id = paper_id[2:]

    if len(paper_id) != 7:
        paper_id = "0" * (7 - len(paper_id)) + paper_id
        # print(paper_id)

    # if count < 100:
    #     print(paper_id, date, cross_list)

    paper_link = "https://arxiv.org/abs/hep-ph/" + paper_id
    req = s.get(paper_link)

    if not req.ok:
        print(paper_link)

print(count)

dates_file.close()