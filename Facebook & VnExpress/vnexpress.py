from lib.utils import initDriver, clearFile, writeFileTxt
from lib.crawlcomment import *
import argparse
from pathlib import Path
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--num_post', type=int, help='number post to get crawling', default=20)
parser.add_argument('--num_cmt', type=int, help='number comment ber post', default=20)
parser.add_argument('--del_old', type=bool, help='delete old files', default=True)
args = vars(parser.parse_args())

savePath = 'data/vnexpress'
clearFile('data/posts.txt')

driver = initDriver()

driver.get('https://vnexpress.net/')

if args['del_old']:
    files = glob.glob(savePath + '/*')
    for f in files:
        os.remove(f)

allLinks = []
allPosts = driver.find_elements(By.CLASS_NAME, 'title-news')

for post in allPosts:
    allLinks.append(post.find_element(By.XPATH, './/a').get_attribute('href'))
 
# allTexts = []
n = min(len(allLinks), args['num_post'])
for idx, link in enumerate(allLinks[:n]):
    filePath = Path(savePath, str(idx) + '.txt')
    filePath.touch(exist_ok=True)

    driver.get(link)

    try:
        contentTags = driver.find_element(By.CLASS_NAME, 'sidebar-1')
        # writeFileTxt(filePath, contentTags.text)

        title = contentTags.find_element(By.XPATH, './/*[@class="title-detail"]')
        writeFileTxt(filePath, title.text)

        description = contentTags.find_element(By.XPATH, './/*[@class="description"]')
        writeFileTxt(filePath, description.text)

        allContentTags = contentTags.find_elements(By.XPATH, './/p')
        for content in allContentTags:
            writeFileTxt(filePath, content.text)

    except:
        print('Post not include text content')
        
    allCmts = set()
    num_cmts = len(allCmts)
    while num_cmts < args['num_cmt']:
        try:
            cmts = driver.find_elements(By.CLASS_NAME, 'content-comment')
        except:
            break

        allCmts.update(cmts)

        if (num_cmts == len(allCmts)):
            break

        num_cmts = len(allCmts)
        try:
            btn = driver.find_element(By.XPATH, '//*[@id="box_comment_vne"]/div/div[8]/a')
        except:
            break

        driver.execute_script ("arguments[0].click();",btn)

    for cmt in list(allCmts)[:args['num_cmt']]:
        try:
            cmt_text = cmt.find_element(By.XPATH, './/p[contains(@class, "full_content")]')
        except:
            cmt_text = cmt.find_element(By.XPATH, './/p[contains(@class, "content_more")]')
        
        
        writeFileTxt(filePath, cmt_text.text)
        # allTexts.append(text)

driver.close()