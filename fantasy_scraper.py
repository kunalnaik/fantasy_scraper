import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# browser setup
dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)  # userAgent for phantomjs
dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
     "(KHTML, like Gecko) Chrome/15.0.87")
path_to_phantomjs = ''  # change path as needed
browser = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)

# chromedriver version
# path_to_chromedriver = ''   # change path as needed
# browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# login page and user credentials
AUTH_URL = 'https://www.nfl.com/login'
USERNAME = ''   # your username here
PASSWORD = ''   # your password here

# setup csv file
output = open('totals.csv', 'w')
writer = csv.writer(output, delimiter=',')
title = ['Team #', 'Kicker Total', 'D/ST Total']
writer.writerow(title)

# open login page and wait until username and password elements are capturable
browser.get(AUTH_URL)
try:
    username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))
except TimeoutException as e:
    print e.message
    browser.quit()

# fill credentials and login
username.send_keys(USERNAME)
password.send_keys(PASSWORD)
password.submit()
# wait until login completed
try:
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "account-info-email")))
except TimeoutException as e:
    print e.message
    browser.quit()

# loop through the 12 teams
for team in range(1, 13):
    # point totals for kicker and dst
    k_total = 0.0
    dst_total = 0.0
    # loop through weeks 1-13
    for week in range(1, 14):
        # open page and wait until matchup summary is loaded
        url = 'http://fantasy.nfl.com/league/2820130/team/' + str(team) + '/gamecenter?gameCenterTab=track&trackType=fbs&week=' + str(week)
        browser.get(url)
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "teamMatchupSummary")))
        except TimeoutException as e:
            print e.message
            browser.quit()

        # get page source html and traverse tree to get score summary list
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        matchup_summary = soup.find("div", { "class" : "teamMatchupSummary" })
        teamWrap = matchup_summary.find("div", { "class" : "teamWrap teamWrap-1" })
        player_list = teamWrap.find("ul")

        # iterate through list and calculate sums
        counter = 0
        for li in player_list.contents:
            points = float(li.find("span", { "class" : "playerTotal" }).string)
            if counter == 7:        # K is 7th item in list
                k_total += points
            elif counter == 8:      # D/ST is 8th item in list
                dst_total += points
            counter += 1

    # print results to output file
    row = [str(team), '{:.2f}'.format(k_total), '{:.2f}'.format(dst_total)]
    writer.writerow(row)

# close output file
output.close()

# logout and close the browser
logout_url = 'https://sso.nfl.com/logout'
browser.get(logout_url)
browser.quit()
