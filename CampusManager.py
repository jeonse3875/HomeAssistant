import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def LeftDayToStr(i):
    if i == 0:
        return '오늘'
    elif i == 1:
        return '내일'
    elif i == 2:
        return '모레'
    else:
        return f'{i}일 뒤'

def GetAssignmentList(day):
    with open('secrets.json') as f:
        jsonData = json.load(f)
        campusId = jsonData["campusId"]
        campusPw = jsonData["campusPw"]

    options = webdriver.ChromeOptions()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    options.add_argument("no-sandbox")
    options.add_argument('window-size=1920x1080')

    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)

    driver.implicitly_wait(1)

    driver.get('https://e-campus.khu.ac.kr/xn-sso/login.php?auto_login=&sso_only=&cvs_lgn=true&return_url=https%3A%2F%2Fe-campus.khu.ac.kr%2Fxn-sso%2Fgw-cb.php%3Ffrom%3Dweb_redirect%26login_type%3Dstandalone%26return_url%3Dhttps%253A%252F%252Fkhcanvas.khu.ac.kr%252Flearningx%252Flogin')

    driver.implicitly_wait(1)

    idElem = driver.find_element_by_name('login_user_id')
    idElem.send_keys(campusId)
    pwElem = driver.find_element_by_name('login_user_password')
    pwElem.send_keys(campusPw)
    pwElem.send_keys(Keys.ENTER)

    driver.implicitly_wait(1)

    driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/span/button')[0].send_keys(Keys.ENTER)
    driver.find_elements_by_xpath('/html/body/span/span/span/span[2]/ul/li[1]/span/ul/li[2]/span')[0].send_keys(Keys.ENTER)

    driver.implicitly_wait(1)
    toDoList = []

    #sleep(100)
    for i in range(3,3 + day):
        toDoLen = len(driver.find_elements_by_xpath(f'//*[@id="dashboard-planner"]/div/div[{i}]/div/div/ol/li'))
        leftAmount = toDoLen

        lectureIdx = 1
        infoStr = f'{LeftDayToStr(i-3)} '
        while(leftAmount > 0):
            blockLen = len(driver.find_elements_by_xpath(f'//*[@id="dashboard-planner"]/div/div[{i}]/div/div[{lectureIdx}]/ol/li'))
            leftAmount -= blockLen
            for blockIdx in range(1,blockLen + 1):
                infoTypeStr = driver.find_elements_by_xpath(f'//*[@id="dashboard-planner"]/div/div[{i}]/div/div[{lectureIdx}]/ol/li[{blockIdx}]/div/div[3]/div/div[1]/div[1]/span')[0].text.split()
                info1 =  f'{infoTypeStr[0]} {infoTypeStr[2]} '
                info2 = driver.find_elements_by_xpath(f'//*[@id="dashboard-planner"]/div/div[{i}]/div/div[{lectureIdx}]/ol/li[{blockIdx}]/div/div[3]/div/div[1]/div[2]/a/span/span[2]')[0].text
                infoStr += info1 + info2 + ' '
            lectureIdx += 1
            toDoList.append(infoStr + '가 예정되어 있습니다.')

    return toDoList

GetAssignmentList(5)