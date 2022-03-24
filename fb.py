from lib.utils import readData, initDriver, clearFile
from lib.fblogin import checkLiveCookie
from lib.crawlcomment import *
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='id to the page for crawling', default='ConfessionUIT')
parser.add_argument('--num_post', type=int, help='number post to get crawling', default=20)
parser.add_argument('--num_cmt', type=int, help='number comment ber post', default=20)
parser.add_argument('--save_file', type=str, default='data/comments.txt')

args = vars(parser.parse_args())

cookie = 'dpr=1.25;datr=GggwYnFfc9Pczy98NvQxG1nb;sb=HggwYjQyGM8oyF0WHBZKnqoH;wd=1536x746;c_user=100048241460483;xs=24%3AThtGz32Jh6GWog%3A2%3A1647314976%3A-1%3A8434;fr=01ujSp9SJQOH2pQ6a.AWUZH1SDzKkx6jisHcg59KKGHuI.BiMAge.5D.AAA.0.0.BiMAjY.AWV6Dq4h6Ig;presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1647315163099%2C%22v%22%3A1%7D;|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
driver = initDriver()
isLive = checkLiveCookie(driver, cookie)
if (isLive):
    savePath = Path(args['save_file'])
    savePath.touch(exist_ok=True)
    clearFile('data/posts.txt')
    clearFile(args['save_file'])
    getnumOfPostFanpage(driver, args['id'], args['num_post'], 'data/posts.txt')
    for postId in readData('data/posts.txt'):
        getAmountOfComments(driver, postId, args['num_cmt'], args['save_file'])

driver.close()
