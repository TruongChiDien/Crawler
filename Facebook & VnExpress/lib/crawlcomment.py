from time import sleep
from selenium.webdriver.common.by import By
from lib.utils import *
import random



def getContentComment(driver, filePath='data/comments.txt'):
    try:
        links = driver.find_elements(By.XPATH, '//a[contains(@href, "comment/replies")]')
        ids = []
        if (len(links)):
            for link in links:
                takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
                textCommentElement = driver.find_element(By.XPATH, ('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                if (takeLink not in ids):
                    print(textCommentElement.text)
                    writeFileTxt(filePath, textCommentElement.text)
                    ids.append(takeLink)
        return ids
    except:
        print("error get link")

def getContentPost(driver, file_path):
    try:
        p_tag = driver.find_element(By.CLASS_NAME, 'bi')
        writeFileTxt(file_path, p_tag.text)
    except:
        print('Get content post error!')

def getAmountOfComments(driver,postId, numberCommentTake, filePath='data/comments.txt'):
    try:
        driver.get("https://mbasic.facebook.com/" + str(postId))
        getContentPost(driver, filePath)
        sumLinks = getContentComment(driver, filePath)
        while(len(sumLinks) < numberCommentTake):
            try:
                nextBtn = driver.find_elements(By.XPATH, '//*[contains(@id,"see_next")]/a')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sumLinks.extend(getContentComment(driver, filePath))
                else:
                    break

                sleep(random.randint(0, 2))
                
            except:
                print('Error when cralw content comment')
    except:
        print("Error get cmt")



def getPostIds(driver, filePath = 'data/posts.txt'):
    allPosts = readData(filePath)
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = driver.find_elements(By.XPATH, '//a[contains(@href, "/sharer.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            if postId not in allPosts:
                print(postId)
                writeFileTxt(filePath, postId)



def getnumOfPostFanpage(driver, pageId, amount, filePath = 'data/posts.txt'):
    driver.get("https://touch.facebook.com/" + pageId)
    while len(readData(filePath)) < amount:
        getPostIds(driver, filePath)