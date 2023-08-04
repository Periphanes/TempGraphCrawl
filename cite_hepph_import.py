import requests
import os
import sys
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
import pickle

s = requests.session()

dates_dir = "dataset/cite-HepPh/pure_txt/cit-HepPh-dates.txt"
links_dir = "dataset/cite-HepPh/pure_txt/cit-HepPh.txt"
pickle_dir = "dataset/cite-HepPh/pickles/"

dates_file = open(dates_dir, 'r')
lines = dates_file.readlines()

papers_list = []

count = 0
for line in tqdm(lines[1:]):
    count += 1

    # line = dates_file.readline()
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

    found = False

    possible_reps = ["https://export.arxiv.org/abs/hep-ph/", "https://export.arxiv.org/abs/hep-th/", 
                     "https://export.arxiv.org/abs/hep-lat/"]

    for possible_rep in possible_reps:
            
        paper_link = possible_rep + paper_id
        req = s.get(paper_link)

        if req.ok:
            found = True
            break
    
    if not found:
        print(paper_link)
        continue

    soup = BeautifulSoup(req.content, 'html.parser')


    title = soup.find_all("h1", class_="title mathjax")[0].contents[1].string
    authors = [i.string for i in soup.find_all("div", class_="authors")[0].contents[1::2]]
    abstract = soup.find_all("blockquote", class_="abstract mathjax")[0].contents[2].string.replace("\n", " ").strip()
    # metatable = soup.find_all("div", class_="metatable")[0].contents[1].contents

    # print(type(metatable[0]))

    # print("\nTitle :", title)
    # print("\nAuthors :", authors)
    # print("\nAbstract : ", abstract)

    # print(metatable)

    # exit(0)

    papers_list.append((paper_id, date, paper_link, title, authors, abstract))

print(count)

with open(pickle_dir + "raw_text", 'wb') as handle:
    pickle.dump(papers_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

dates_file.close()