from lib.utils import readData, initDriver, clearFile, writeFileTxt
from lib.fblogin import checkLiveCookie
from lib.crawlcomment import *
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--num_post', type=int, help='number post to get crawling', default=20)
parser.add_argument('--num_cmt', type=int, help='number comment ber post', default=20)
parser.add_argument('--save_file', type=str, default='data/comments.txt')
args = vars(parser.parse_args())

savePath = Path(args['save_file'])
savePath.touch(exist_ok=True)
clearFile(args['save_file'])

driver = webdriver.Chrome('lib/chromedriver.exe')


driver.get('https://vnexpress.net/')
sleep(5)

allLinks = []
allPosts = driver.find_elements(By.CLASS_NAME, 'title-news')

for post in allPosts:
    allLinks.append(post.find_element(By.XPATH, './/a').get_attribute('href'))

# allTexts = []
for link in allLinks[:min(len(allLinks, args['num_post']))]:
    driver.get(link)
    sleep(2)
    allCmts = set()
    num_cmts = len(allCmts)
    while num_cmts < args['num_cmt']:
        try:
            cmts = driver.find_elements(By.CLASS_NAME, 'content-comment')
        except:
            break
        allCmts.update(cmts)
        # if len(allCmts) == num_cmts:
        #     break
        # num_cmts = len(allCmts)
        try:
            btn = driver.find_element(By.ID, 'show_more_coment')
        except:
            break
        driver.execute_script ("arguments[0].click();",btn)

    for cmt in list(allCmts):
        try:
            cmt_text = cmt.find_element(By.XPATH, './/p[contains(@class, "full_content")]')
        except:
            cmt_text = cmt.find_element(By.XPATH, './/p[contains(@class, "content_more")]')
        
        
        writeFileTxt('data/comments.txt', cmt_text.text)
        # allTexts.append(text)

driver.close()