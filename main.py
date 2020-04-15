# coding: utf-8

import time
from datetime import datetime
from selenium import webdriver
from sys import exit

login_id = 'login_idm'
login_password = 'login_password'
item_url = 'https://www.amazon.ca/B-spaces-Battat-Organizer-Furniture/dp/B071FT91BJ/'
limit_value = 200.00  # Max purchase Price
delay_time = int(60)  # Delay time in second





ACCEPT_SHOP = 'Amazon'

def l(str):
    print("%s : %s" % (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))


if __name__ == '__main__':

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome('./chromedriver', options=options)
        browser.get(item_url)
    except:
        l('Failed to open browser.')
        exit()

    while True:
        # check stock
        while True:
            try:
                # check seller
                shop = browser.find_element_by_id('merchant-info').text

                if ACCEPT_SHOP not in shop:
                    raise Exception("not Amazon.")

                # add into cart

                browser.find_element_by_id('add-to-cart-button').click()
                break
            except:
                l('Not in stock yet')
                time.sleep(delay_time)
                browser.refresh()

        # process to check out
        browser.get('https://www.amazon.ca/gp/cart/view.html?ref_=nav_cart')
        browser.find_element_by_name('proceedToRetailCheckout').click()

        # sign in
        try:
            browser.find_element_by_id('ap_email').send_keys(login_id)
            browser.find_element_by_id('continue').click()
            browser.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            browser.find_element_by_id('signInSubmit').click()
            l('Logged in.')
        except:
            l('Fail to login')
            pass

        # Price check
        p = browser.find_element_by_css_selector('td.grand-total-price').text
        if float(p.split(' ')[1].replace(',', '')) > limit_value:
            l('Price is too high.')
            exit()
        else:
            browser.find_element_by_name('placeYourOrder1').click()
            l('Bought item')
            break
    browser.close()
exit()
