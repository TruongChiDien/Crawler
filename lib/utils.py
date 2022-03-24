from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep


def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        data.append(line[:-1])
    return data



def writeFileTxt(fileName, content):
    with open(fileName, 'a', encoding='utf-8') as f1:
        f1.write(str(content) + '\n')



def initDriver():
    driver = webdriver.Chrome('lib/chromedriver.exe')
    return driver



def outCookie(driver):
    try:
        sleep(1)
        script = "javascript:void(function(){ function deleteAllCookiesFromCurrentDomain() { var cookies = document.cookie.split(\"; \"); for (var c = 0; c < cookies.length; c++) { var d = window.location.hostname.split(\".\"); while (d.length > 0) { var cookieBase = encodeURIComponent(cookies[c].split(\";\")[0].split(\"=\")[0]) + '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path='; var p = location.pathname.split('/'); document.cookie = cookieBase + '/'; while (p.length > 0) { document.cookie = cookieBase + p.join('/'); p.pop(); }; d.shift(); } } } deleteAllCookiesFromCurrentDomain(); location.href = 'https://mbasic.facebook.com'; })();"
        driver.execute_script(script)
    except:
        print("loi login")


def clearFile(filePath):
    with open(filePath, 'w') as f:
        f.write('')

