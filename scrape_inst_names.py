from bs4 import BeautifulSoup
import requests
import os 

class InstitutionScraper:
    def fetch_and_save_webpage(self, url):
        '''
        Fetch the webpage HTML and saves it to a file.
        '''
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        webpage = requests.get(url, headers = headers)

        with open('top_uni.html', 'w') as fp:
            fp.write(webpage.text)


    def parse_and_save_raw_inst_html(self, subject, filepath):
        '''
        Parse the raw html (of USNews instituition ranking page format) and save the scraped institution names to a file.
        '''
        # create a folder named results if it doesn't exist
        if not os.path.exists('./results'):
            os.makedirs('./results')

        OUT_FILE = './results/top_{}_univs.csv'.format(subject)

        # Parse university names from raw html
        with open(filepath, "r") as f:
            soup = BeautifulSoup(f, 'html.parser')

        univ_divs = soup.find_all("div", {"class": ["Box-w0dun1-0", "jSPhKa"]})

        univ_names = []
        for u in univ_divs:
            if 'name' in u.attrs:
                cur_u_name = u.attrs['name']
                univ_names.append(cur_u_name)

        # Save data as csv
        with open(OUT_FILE, "w") as f:

            for i in range(len(univ_names)):
                cur_u_id = i + 1
                cur_u_name = univ_names[i]
                data_line = f"{cur_u_id},'{cur_u_name}'\n"

                f.write(data_line)

    def cleanup(self, filepath):
        os.remove(filepath) 

    def scrape(self, url, raw_html_path, department):
        '''
        This function takes in the url or raw_html_path and scrapes the institution names and saves them to a file.
        '''
        if(url != None):
            self.fetch_and_save_webpage(url)   
            raw_html_path = "./top_uni.html"     
        self.parse_and_save_raw_inst_html(department, raw_html_path)
        self.cleanup(raw_html_path)


# scraper = InstitutionScraper()
# url = 'https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings'
# scraper.scrape(url, None, 'math')
