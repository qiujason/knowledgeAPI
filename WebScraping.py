import re
from selenium import webdriver

DRIVER = webdriver.Chrome(executable_path=r'/usr/local/Caskroom/chromedriver/87.0.4280.20/chromedriver')


def web_scraping(site):
    DRIVER.get(site)

    title = DRIVER.find_element_by_css_selector('h1').text

    url = DRIVER.current_url

    parent_element = DRIVER.find_elements_by_class_name('mb-0')

    about_section = parent_element[0].find_elements_by_tag_name('span')[0]

    author = about_section.find_element_by_tag_name('a').text

    about = about_section.text

    words = about.split(' ')

    date_of_article = '-'.join(words[3:6])
    date_of_article = date_of_article.replace(',', '', 1)

    tags_of_article = ','.join(words[-4:])

    article_body = DRIVER.find_elements_by_class_name('article-body')

    table_of_contents = article_body[0].find_element_by_class_name('sidebar-module-inset').text

    recommend = parent_element[1].text

    article = article_body[0].text

    article = re.sub('[^A-Za-z0-9 .,\n]+', '', article)

    about_the_author = DRIVER.find_elements_by_id('author')[0].text

    return {'title': title, 'author': author, 'date_of_article': date_of_article, 'tags_of_article': tags_of_article,
            'table_of_contents': table_of_contents, 'recommend': recommend, 'article': article,
            'about_the_author': about_the_author, 'url': url}
