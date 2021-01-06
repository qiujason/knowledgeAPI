import re
from selenium import webdriver

DRIVER = webdriver.Chrome(executable_path=r'/usr/local/Caskroom/chromedriver/87.0.4280.20/chromedriver')


def web_scraping(site):
    DRIVER.get(site)

    article_body = DRIVER.find_elements_by_class_name('article-body')

    article = article_body[0].text

    article = re.sub('[^A-Za-z0-9 .,\n]+', '', article)
    article = article.split('\n')
    DRIVER.close()
    return article
