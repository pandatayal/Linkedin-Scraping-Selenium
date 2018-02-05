from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv

def validate(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open('linkedin_data_3.csv', 'wb'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'URL'])

driver = webdriver.Chrome('/Users/panda/Downloads/chromedriver')
driver.get('https://www.linkedin.com')

email = driver.find_element_by_class_name('login-email')
email.send_keys('ADD YOUR EMAIL ADDRESS HERE')
sleep(0.5)

password = driver.find_element_by_class_name('login-password')
password.send_keys('ADD YOUR LINKEDIN PASSWORD HERE')
sleep(0.5)

submit_button = driver.find_element_by_class_name('submit-button')
submit_button.click()
sleep(5)

driver.get('http://www.google.com')

search_query = driver.find_element_by_name('q')
search_query.send_keys('site:/linkedin.com/in/ AND python developer AND Bangalore')
search_query.send_keys(Keys.RETURN)
sleep(3)
linkedin_urls = driver.find_elements_by_tag_name('cite')

linkedin_urls = [url.text for url in linkedin_urls]
sleep(0.5)
print(linkedin_urls)

for link in linkedin_urls:
   driver.get(link)
   sleep(5)

   sel = Selector(text=driver.page_source)
   name = sel.xpath('//h1/text()').extract_first()
   job = sel.xpath('//h2/text()').extract_first()
   school = sel.xpath('//*[starts-with(@class,"pv-top-card-section__school")]/text()').extract_first().strip()
   location = sel.xpath('//*[starts-with(@class,"pv-top-card-section__location")]/text()').extract_first().strip()
   linkdin_url = driver.current_url

   sel = validate(sel)
   name = validate(name)
   job = validate(job)
   school = validate(school)
   location = validate(location)
   linkdin_url = validate(linkdin_url)

   print('\n')
   print('Name: ' + name)
   print('Job Title: ' + job)
   print('School: ' + school)
   print('Location: ' + location)
   print('URL: ' + linkdin_url)
   print('\n')

   writer.writerow([name.encode('utf-8'),
                job.encode('utf-8'),
                school.encode('utf-8'),
                location.encode('utf-8'),
                linkdin_url.encode('utf-8')])

   try:
       driver.find_element_by_xpath('//span[text()="Connect"]').click()
       sleep(3)

       driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
       sleep(3)

   except:
       pass


driver.quit()
