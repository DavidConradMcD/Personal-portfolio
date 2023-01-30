from bs4 import BeautifulSoup
import pandas
import csv
import requests
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium as selenium
from urllib.parse import urljoin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select



url = "https://ca.indeed.com"
csv_file = open('test_file3.csv', 'w')
job_writer = csv.writer(csv_file)
job_writer.writerow(['JobTitle','Company','Location','Link','Description'])

driver = webdriver.Chrome(r"C:\Users\David\Documents\Ideas\Personal website\portfoliowebsite\job_postings_dash_app\chromedriver")
driver.get(url)
driver.implicitly_wait(2)


companies = []
job_names = []
job_descs = []
total_driver_names = []
locations = []
salaries = []
links = []
res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")


def advanced_search(driver):
    job_title_input = driver.find_element_by_id('text-input-what')
    job_title_input.send_keys('Analyst')
    try:
        cookies_button = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        cookies_button.click()
    except selenium.common.exceptions.NoSuchElementException as Error:
        pass
    job_title_input.send_keys(Keys.ENTER)
    adv_search = driver.find_element_by_partial_link_text('Advanced Job')
    adv_search.click()
    word_reduction = driver.find_element_by_id('as_not')
    word_reduction.send_keys('Hiring Event')
    choose_loc = driver.find_element_by_id('where')
    choose_loc.clear()
    choose_loc.send_keys('Toronto, ON')
    display_limit = Select(driver.find_element_by_id('limit'))
    display_limit.select_by_value('10')
    word_reduction.send_keys(Keys.ENTER)


def next_page(driver):
    driver.implicitly_wait(3)
    next_page = driver.find_element_by_partial_link_text('Next »')
    next_page.click()

    #driver.switch_to_alert().dismiss()
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_xpath('//*[@id="popover-close-link"]').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="popover-x"]/a').click()
    except:
        pass


def page_loop(driver):
    driver.implicitly_wait(2)
    close_popup = driver.find_element_by_xpath('//*[@id="popover-x"]')
    close_popup.click()

    for page in range(0,99):
        try:
            driver.find_element_by_xpath('//*[@id="popover-close-link"]').click()
        except:
            pass
        driver_name = driver.find_elements_by_class_name('title')
        company = driver.find_elements_by_class_name('company')
        location = driver.find_elements_by_class_name('location')
        for i in driver.find_elements_by_id('resultsCol'):
            for a in i.find_elements_by_xpath('.//a'):
                if str(a.get_attribute('href')).__contains__('/rc/clk?jk') or str(a.get_attribute('href')).__contains__('pagead/clk?') or str(a.get_attribute('href')).__contains__('/company/'):
                    links.append(a.get_attribute('href'))
                else:
                    continue

        print(len(links))

        driver.implicitly_wait(2)

        try:
            cookies_button = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
            cookies_button.click()
        except selenium.common.exceptions.NoSuchElementException as Error:
            pass

        for i in company:
            companies.append(i.text)
            print(i.text)

        for i in location:
            locations.append(i.text)

        for i in driver_name:
            i.click()
            try:
                job_id = driver.find_element_by_id('vjs-desc')
                job_descs.append(job_id.text)
            except selenium.common.exceptions.NoSuchElementException:
                job_descs.append('#N/A')
                pass
            job_names.append(i.text)
            total_driver_names.append(i.text)
            job_name_length = len(job_names)

        if len(links) < len(job_names):
            links.append('#N/A')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            next_page(driver)
        except selenium.common.exceptions.NoSuchElementException:
            break

        print(len(total_driver_names))
        print(len(job_names))
        print(len(job_descs))
        print(len(locations))
        print('\n')

        page = page + 1

    return companies, job_names, job_descs, total_driver_names, locations, links

def write_to_csv(driver):
    advanced_search(driver)
    page_loop(driver)
    for row in range(len(total_driver_names)):
        job_writer.writerow([job_names[row],companies[row],locations[row],links[row],job_descs[row]])
write_to_csv(driver)

driver.quit()
csv_file.close()
