#!/usr/bin/python3

import csv
import json
import pickle
from pprint import pprint
import array
import constants


CHUNK_SIZE = 200
ROW_SIZE = 142204800 // 200 # full_block_filesize / chun_size
NUM_ENTRIES = 20


# Load data ####################################################

with open('skiller/skills.csv') as fin:
    raw_skills = list(csv.DictReader(fin))
    print(f"Raw skills = {len(raw_skills)}")

with open('skiller/views_leads.csv') as fin:
    raw_jobs = list(csv.DictReader(fin))
    print(f"Raw jobs = {len(raw_jobs)}")

#
# WARNING: DEBUG TEST HACK
#
#raw_jobs = raw_jobs[:2000]
#
#
#

# WARNING: Full dataset can take up more than 64GB of RAM
#          You've been warned.
DATASET_MAX_SIZE = 100000

#
# WARNING: DEBUG TEST HACK
#
knc_raw_jobs = raw_jobs[:DATASET_MAX_SIZE]
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


# Process efficient data types #################################
knc_jobs_ids   = set(j['id_ad_site'] for j in knc_raw_jobs)
knc_skills_ids = set(j['id_ad_site'] for j in raw_skills)
knc_match_ids  = knc_jobs_ids.intersection(knc_skills_ids)
print(len(knc_match_ids))
################################################################


# Clean up unnecessary data
knc_jobs   = [j for j in knc_raw_jobs if j['id_ad_site'] in knc_match_ids]
knc_skills = [s for s in raw_skills if s['id_ad_site'] in knc_match_ids]

# skillnames
knc_skillnames = []
with open('skiller/knc_skillnames.json') as fin:
    knc_skillnames = json.load(fin)
knc_skillnames_map = {
    knc_skillnames[i]: i for i in range(len(knc_skillnames))
}


# Calculate idnames
idnames = {}
for s in skills:
    if not s['id_ad_site'] in idnames:
        idnames[s['id_ad_site']] = []
    idnames[s['id_ad_site']].append(s['skill'])

# Calculate jobskills = [['SKILL1', 'SKILL2'], ...]
jobskills = [set(idnames[j['id_ad_site']]) for j in jobs if j['id_ad_site'] in idnames]

################################################################

knc = None
with open('skiller/ai/knc.pkl', 'rb') as f:
    knc = pickle.load(f)

def predict_knc(search_skills):
    # myskills = {"ARDUINO", "PHP", "MYSQL"}
    myskills = set(search_skills)
    vec = [(s in myskills) for s in knc_skillnames]
    result = knc.predict([vec])
    return [name for s, name in constants.massilla_powerup_skills if s in result]

import struct # !!!!

def direct_read_cosine_matrix(idx):
    """
    Read from a binary structured file
    """
    filetarget_num = (idx // CHUNK_SIZE) * CHUNK_SIZE
    filetarget = f"skiller/ai/sim-{filetarget_num}.bia"
    row_start = (idx % CHUNK_SIZE) * ROW_SIZE

    print(f"direct_read_cosine_matrix {idx} filetarget={filetarget}. row_start={row_start}")

    arr = array.array('d')
    with open(filetarget, 'rb') as fin:
        fin.seek(row_start)
        arr.frombytes(fin.read(ROW_SIZE))

    return arr

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(job_index):
    idx = job_index

    cosine_sim = direct_read_cosine_matrix(idx)

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = sorted(list(enumerate(cosine_sim)), key=lambda x: -x[1])

    # # Sort the movies based on the similarity scores
    # sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar job offers
    sim_scores = sim_scores[:NUM_ENTRIES]

    # Get the indices
    res = [i[0] for i in sim_scores]

    print([jobs[j] for j in res])
    print([idnames[jobs[j]['id_ad_site']] for j in res])

    # Return the top 10 most similar movies
    return res

def recomend_job_by_keywords(keywords):
    kwset = set(keywords)
    best, index = max(
        ((len(kwset.intersection(jobskills[i])), i)
         for i in range(len(jobskills))),
    )
    if best < 1:
        return []
    seed_job  = index
    ia = get_recommendations(seed_job)
    iajobs = [jobs[j] for j in ia]
    cleaned = {
        iajobs[i]['description']: ia[i] for i in range(len(iajobs))
    }
    res = ([seed_job] + list(cleaned.values()))[:NUM_ENTRIES]
    print(res)

    topfreq={}
    for js in res:
        for jjs in jobskills[js]:
            if jjs not in topfreq:
                topfreq[jjs] = 0
            topfreq[jjs] += 1

    toptags = [t[0] for t in sorted(topfreq.items(), key=lambda k: -k[1]) if t[0] in kwset]

    return {
        "top": toptags,
        "offers": res,
    }
