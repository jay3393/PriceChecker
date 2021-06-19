from bs4 import BeautifulSoup
import requests
import time

def does_exist(filter_skills, skills):
    if filter_skills[0] == '':
        return True
    for skill in filter_skills:
        if skill in skills:
            return False
    return True

print('Enter a filter out skill (Separate all skills with a comma)')
filter_out_skill = input('>').lower().strip().split(',')
if len(filter_out_skill) >= 1 and filter_out_skill[0] != '':
    print(f"Filtering out {','.join(filter_out_skill)}...")
else:
    print("Finding jobs...")

def find_jobs():
    r = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    bs = BeautifulSoup(r, 'lxml')
    jobs = bs.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    results = 0
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        valid = True
        if 'few' in published_date:
            company = job.find('h3', class_ = 'joblist-comp-name').text.strip()
            skills = job.find('span', class_ = 'srp-skills').text.strip()
            more_info = job.header.h2.a['href']
            if does_exist(filter_out_skill, skills):
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name: {company}\n")
                    f.write(f"Required Skills: {skills.replace(' ', '')}\n")
                    f.write(f"More info: {more_info}\n")
                    results += 1
                print(f'File saved: {index}')

    print(f"Found {results} results")

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = .1
        time.sleep(60*time_wait)
        print(f"Refreshing search...")