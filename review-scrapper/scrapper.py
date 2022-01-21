from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import re
import time

chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(executable_path='driver/chromedriver/chromedriver', options=chrome_options)


class Scrapper:

    def __init__(self):
        self.not_continue = False
        self.url = "https://www.tripadvisor.es/Hotels-g187497-Barcelona_Catalonia-Hotels.html"

    def scrapper(self, opinion):

        csvFile = open("files/reviews.csv", "w", newline='', encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Rating', 'Review'])
        driver.get(self.url)
        url_list = []

        try:
            # botó que accepta les condicions de les cookies
            driver.find_element_by_xpath("//*[contains(@id, 'onetrust-accept-btn-handler')]").click()
        except:
            print('No cookies found')

        for i in range(10):
            print('Processing page:' + str(i))
            e = driver.find_elements_by_class_name('property_title')
            for x in e:
                url_list.append(x.get_attribute('href'))
            # next button
            driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]').click()
            time.sleep(5)

        for i in range(len(url_list)):
            print('Processing listing:' + str(i+1)+'/'+str(len(url_list)) + ' ' + str(url_list[i]))
            self.open_listing(url_list[i], csvWriter, opinion)

    '''
    Metode que processa les reviews d'un hotel en concret
    '''
    def open_listing(self,listing, csvWriter, opinion):
        driver.get(listing + '#REVIEWS')

        #click per seleccionar reviews en tots els idiomes
        #driver.execute_script("document.getElementById('LanguageFilter_0').click();")

        '''if opinion == 0:
            self.positive_reviews()
        elif opinion == 1:
            self.negative_reviews()'''

        if not self.not_continue:
            for i in range(10):
                rev = driver.find_elements_by_class_name('cWwQK')
                for review in rev:
                    score = review.find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
                        "class")
                    score = self.parse_score(score)
                    text = review.find_element_by_class_name('XllAv').text
                    csvWriter.writerow([score, text])
                try:
                    driver.find_element_by_xpath(".//a[contains(@class, 'next')]").click()
                except:
                    break
                time.sleep(5)
        self.not_continue = False


    def parse_score(self, s):
        score = int(re.findall('\d*\.?\d+', s)[0]) / 10
        return score

    '''
    Mètode emprat per filtrar les reviews negatives
    '''
    def negative_reviews(self):
        rating1 = driver.find_element_by_id('ReviewRatingFilter_1')
        rating2 = driver.find_element_by_id('ReviewRatingFilter_2')

        if rating1.get_property("disabled") or rating2.get_property("disabled"):
            self.not_continue = True
        else:
            if not rating1.get_property('checked'):
                driver.execute_script("document.getElementById('ReviewRatingFilter_1').click();")
            if not rating2.get_property('checked'):
                driver.execute_script("document.getElementById('ReviewRatingFilter_2').click();")
            time.sleep(5)

    '''
        Mètode emprat per filtrar les reviews positives
    '''
    def positive_reviews(self):
        rating1 = driver.find_element_by_id('ReviewRatingFilter_5')
        rating2 = driver.find_element_by_id('ReviewRatingFilter_4')

        if rating1.get_property("disabled") or rating2.get_property("disabled"):
            self.not_continue = True
        else:
            if not rating1.get_property('checked'):
                driver.execute_script("document.getElementById('ReviewRatingFilter_5').click();")
            if not rating2.get_property('checked'):
                driver.execute_script("document.getElementById('ReviewRatingFilter_4').click();")
            time.sleep(5)


if __name__ == "__main__":
    sc = Scrapper()
    sc.scrapper(0)

