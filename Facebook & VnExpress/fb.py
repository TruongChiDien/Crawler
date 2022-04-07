from lib.utils import readData, initDriver, clearFile
from lib.fblogin import checkLiveCookie
from lib.crawlcomment import *
import argparse
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='id to the page for crawling', default='ConfessionUIT')
parser.add_argument('--num_post', type=int, help='number post to get crawling', default=20)
parser.add_argument('--num_cmt', type=int, help='number comment ber post', default=20)
parser.add_argument('--del_old', type=bool, help='delete old files', default=True)


args = vars(parser.parse_args())

des_path = 'data/facebook'

cookie = 'datr=GggwYnFfc9Pczy98NvQxG1nb;sb=HggwYjQyGM8oyF0WHBZKnqoH;wd=1536x746;dpr=1.25;c_user=100048241460483;xs=45%3AZ4YupZqe5VGAbQ%3A2%3A1649081280%3A-1%3A8434;fr=0APz1wWtfyReyYIMe.AWU-H8bERO36NIw9U37nhgHWj50.BiMW9D.5D.AAA.0.0.BiSvvB.AWUP8rdZwyo;presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1649081290214%2C%22v%22%3A1%7D;|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
driver = initDriver()
isLive = checkLiveCookie(driver, cookie)

if (isLive):
    clearFile('data/posts.txt')
    getnumOfPostFanpage(driver, args['id'], args['num_post'], 'data/posts.txt')

    if args['del_old']:
        os.system('rm -r ' + des_path)

    for postId in readData('data/posts.txt'):
        if len(postId) < 16: # Not ID of Post
            continue

        save_path = Path(des_path, str(postId) + '.txt')
        save_path.touch(exist_ok=True)
        clearFile(save_path)

        getAmountOfComments(driver, postId, args['num_cmt'], save_path)
        sleep(random.randint(0, 2))

driver.close()
