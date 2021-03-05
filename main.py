import requests
from bs4 import BeautifulSoup
import csv

jobsFile = open('jobs.csv', 'w')
writer = csv.writer(jobsFile)
writer.writerow(('Job Title', 'Company', 'Location', 'Data Post'))

class Indeed:
    def __init__(self, position, location, number_pages):
        self.position = position
        self.location = location
        self.number_pages = number_pages

    def get_url(self):
        url = f'https://indeed.com/jobs?q={self.position}&l={self.location}'
        return url

    def url_request(self, url):
        headers = {
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36',
        }
        response = requests.get(url)
        return response

    def extract_jobs(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in range(1, self.number_pages):
            boxes = soup.find_all('div', class_='jobsearch-SerpJobCard')
            for box in boxes:
                card = box.h2.a
                jobtitle = card['title']
                company = box.find('span', class_='company').text.strip()
                location = box.find('span', class_='location').text.strip()
                data_post = box.find('span', class_='date').text.strip()
                writer = csv.writer(jobsFile)
                writer.writerow((jobtitle, company, location, data_post))
                next = soup.find('a', {'aria-label': 'Next'}).get('href')
                next_sliced = next[:next.find('start=') + 6]
                url = 'https://www.indeed.com' + next_sliced + f'{i * 10}'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

        jobsFile.close()


if __name__ == '__main__':
    jobs = Indeed('data scientist', '', 3)
    url = jobs.get_url()
    response = jobs.url_request(url)
    jobs.extract_jobs(response)






