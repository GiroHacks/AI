#!/usr/bin/python3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv

skills_header = ['id_ad_site', 'skill']
jobs_header   = 'id_ad_site,publication_date,province,offer_type,industry,job_title,normalized_name,description,requirements,id_salary_min,minimum_salary,maximum_salary,is_salary_showed,num_views,num_leads'.split(',')
match_header  = ["skill", "job"]

job_id = jobs_header.index('id_ad_site')
match_camps = [jobs_header.index(c) for c in (
    'industry',
    'job_title',
    'description',
    'requirements'
)]

def load_skills():
    with open('skills.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            (row['skill'].lower(), row['id_ad_site'])
            for row in reader
        ]

def load_jobs_keyworded():
    # Load CSV data
    res = []
    with open('views_leads.csv', newline='') as csvin:
        reader = csv.reader(csvin)
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for job in reader:
            text = ' '.join(job[mc] for mc in match_camps)
            res.append(job[job_id], text)

def iaaa(jobs):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim.shape


print("Load skills")
skills = load_skills()

print("Processing")
progress = 0
    with open('output.csv', 'w') as csvfile:
        writer.writerow(["skill", "job"])
            for s in skills:
                for mc in match_camps:
                    if s[0] in job[mc]:
                        writer.writerow([s[1], job[0]])
                progress += 1
                if progress % 1000000 == 0:
                    print(progress)
