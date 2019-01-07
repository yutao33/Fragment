from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

driver.get("http://www.51ape.com/Taylor-Swift/")
links = driver.find_elements_by_xpath("//div[@class='news w310 over fl']/ul[@class='mt_05']/li[@class='blk_nav lh30 over']")
hrefs=[link.find_element_by_tag_name('a').get_attribute('href') for link in links]


# browser = webdriver.Chrome("/home/kyle/bin/chromedriver")
# browser.implicitly_wait(10)  #设置智能等待10秒

# from selenium.webdriver.support.wait import WebDriverWait
# 使用selenium提供的WebDriverWait方法，每0.5秒检查一次定位的元素，超时设置是2秒
# WebDriverWait(browser, 2).until(
#        lambda driver: driver.find_element_by_tag_name('body'))

# http://www.51ape.com/ape/156942.html
# http://www.51ape.com/ape/156917.html
# http://www.51ape.com/ape/156891.html
select = hrefs[hrefs.index('http://www.51ape.com/ape/156884.html'):]

for href in select:
    print(href)
    driver.get(href)
    time.sleep(1)
    pwline_ele = driver.find_element_by_xpath("//div[@class='fl over w638']/b[@class='mt_1 yh d_b']")
    pwline = pwline_ele.text
    pw = None
    if pwline[-1]!='无':
        pw = pwline[-4:]
    #
    print("pw=",pw)
    download = driver.find_element_by_xpath("//h2[@class='bg_gr b_b_s m_s logo mt_1 yh white']")
    href = download.find_element_by_xpath('..').get_attribute('href')
    driver.get(href)
    time.sleep(1)
    # driver.switch_to_window(driver.window_handles[1])
    #
    if pw:
        # inp = driver.find_element_by_xpath("//input[@class='clearfix']")
        inp = driver.find_elements_by_tag_name('input')
        if inp:
            inp[0].send_keys(pw)
            inp[0].send_keys(Keys.ENTER)
            time.sleep(10)
    #
    for i in range(10):
        save = driver.find_element_by_xpath("//a[@data-button-id='b1']")
        save.click()
        time.sleep(5)
        #
        items = driver.find_elements_by_xpath("//ul[@class='treeview treeview-root-content treeview-content ']/li")
        if len(items)>16:
            break
    items[16].click()
    time.sleep(5)
    #
    sure = driver.find_element_by_xpath("//a[@class='g-button g-button-blue-large']")
    sure.click()
    time.sleep(5)


