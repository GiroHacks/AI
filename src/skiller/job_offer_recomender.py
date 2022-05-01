"""
AI Model for related job offer recomendations.
Powerful
"""


import csv
from pprint import pprint
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster
import numpy as np
import concurrent.futures
from math import ceil
from stop_words import get_stop_words


chunk_size = 200


# Load data ####################################################
with open('skills.csv') as fin:
    raw_skills = list(csv.DictReader(fin))
    print(f"Raw skills = {len(raw_skills)}")

with open('views_leads.csv') as fin:
    raw_jobs = list(csv.DictReader(fin))
    print(f"Raw jobs = {len(raw_jobs)}")

################################################################


#
# WARNING: DEBUG TEST HACK
#
# raw_jobs = raw_jobs[:5000]
#
#
#


# Process efficient data types #################################
jobs_ids   = set(j['id_ad_site'] for j in raw_jobs)
skills_ids = set(s['id_ad_site'] for s in raw_skills)
match_ids  = jobs_ids.intersection(skills_ids)
print(len(match_ids))

# Clean up unnecessary data
jobs   = [j for j in raw_jobs if j['id_ad_site'] in match_ids]
skills = [s for s in raw_skills if s['id_ad_site'] in match_ids]
################################################################

# skillnames
skillnames = [s['skill'] for s in skills]
skillnames_map = {
    skillnames[i]: i for i in range(len(skillnames))
}

# Calculate idnames
idnames = {}
for s in skills:
    if not s['id_ad_site'] in idnames:
        idnames[s['id_ad_site']] = []
    idnames[s['id_ad_site']].append(s['skill'])

print(len(idnames))

# Calculate jobskills = [['SKILL1', 'SKILL2'], ...]
jobskills = [set(idnames[j['id_ad_site']]) for j in jobs if j['id_ad_site'] in idnames]

freqskills={}
for js in jobskills:
    for jjs in js:
        if jjs not in freqskills:
            freqskills[jjs] = 0
        freqskills[jjs] += 1


# IA 🌈✨ ######################################################

PROGRESS_BAR_SIZE = 40

def report_progress(path, now, total):
    """
    Prints the current progress
    """
    progress_bar = '▣' * int(now / total * PROGRESS_BAR_SIZE)
    print(" " * (PROGRESS_BAR_SIZE + 20), end='\r')
    print(path)
    print(f"[{progress_bar:□<{PROGRESS_BAR_SIZE}}] [{now:05} / {total:05}]", end='\r')

def report_progress_end():
    """
    End progress reporting
    """
    print(" " * (PROGRESS_BAR_SIZE + 1), end='\r')
    msg = "Done ^.^"
    print(f"[ ★★★ {msg} " + "★" * (PROGRESS_BAR_SIZE - len(msg) - 7))


# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

sopa = [
    f"{' '.join(idnames[j['id_ad_site']])} {j['description']} {j['requirements']} {j['job_title']}"
    for j in jobs
]

swords = get_stop_words('english')

print("Creating CountVectorizer from data")
count = CountVectorizer(stop_words=swords)
count_matrix = count.fit_transform(sopa)
print(count_matrix.shape)
matrix_len, _ = count_matrix.shape

exit(1)
################################################################

print("Calculating the similarity matrix")

def similarity_cosine_by_chunk(start, end):
    if end > matrix_len:
        end = matrix_len
    return cosine_similarity(X=count_matrix[start:end], Y=count_matrix) # scikit-learn function

def calculate_and_save_similarity_cosine_chunk(start):
    matrix_chunk = similarity_cosine_by_chunk(start, start+chunk_size)
    with open(f"ai/sim-{start}.bia", "wb") as fout:
        for row in matrix_chunk:
            fout.write(bytearray(row))
    return True


chunks_done = 0
# Multithreaded, chunked computation
with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
    future_todo = {
        executor.submit(calculate_and_save_similarity_cosine_chunk, i): i
        for i in range(0, matrix_len, chunk_size)
    }
    for future in concurrent.futures.as_completed(future_todo):
        index = future_todo[future]
        try:
            ok = future.result()
            if not ok:
                raise ValueError(":v")
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
            continue
        chunks_done += 1
        report_progress(f"Similarity matrix {chunks_done}", chunks_done, ceil(matrix_len/chunk_size))

report_progress_end()
