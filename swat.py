from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser

WEBPAGE_MAX_LOAD_TIME = 20
driver = None
config = None

def initDriver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(WEBPAGE_MAX_LOAD_TIME) # seconds
    return driver

def readTestcase(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def prepareEnv(driver):
    driver.get(getLink())

def getDescription():
    return config['DEFAULT']['description']

def getLink():
    return config['DEFAULT']['link']

def getTestSteps(config):
    return config.sections()

def runStep(config, step):
    print("# Running step:", step)
    action = config[step]['action']

    if action == 'click':
        if config.has_option(step, 'byid'):
            click_button(driver=driver, byid=config.get(step, 'byid'))
        elif config.has_option(step, 'byname'):
            click_button(driver=driver, byid=config.get(step, 'byname'))
        elif config.has_option(step, 'byxpath'):
            click_button(driver=driver, byid=config.get(step, 'byxpath'))

    if action == 'textbox':
        if not config.has_option(step, 'sendkeys'):
            raise Exception('textbox error')
        else:
            sendkeys = config[step]['sendkeys']
        submit = config.getboolean(step, 'submit') or False
        if config.has_option(step, 'byid'):
            edit_textbox(driver=driver, byid=config.get(step, 'byid'), sendkeys=sendkeys, submit=submit)
        elif config.has_option(step, 'byname'):
            edit_textbox(driver=driver, byid=config.get(step, 'byname'), sendkeys=sendkeys, submit=submit)
        elif config.has_option(step, 'byxpath'):
            edit_textbox(driver=driver, byid=config.get(step, 'byxpath'), sendkeys=sendkeys, submit=submit)

    if action == 'debug':
        if config.has_option(step, 'byid'):
            queryElement(driver=driver, byid=config.get(step, 'byid'))
        elif config.has_option(step, 'byname'):
            queryElement(driver=driver, byname=config.get(step, 'byname'))
        elif config.has_option(step, 'byxpath'):
            queryElement(driver=driver, byxpath=config.get(step, 'byxpath'))
        elif config.has_option(step, 'byclass'):
            queryElement(driver=driver, byclass=config.get(step, 'byclass'))
        elif config.has_option(step, 'bytext'):
            queryElement(driver=driver, bytext=config.get(step, 'bytext'))

    if action == 'assert':
        byid = config.get(step, 'byid') if config.has_option(step, 'byid') else None
        byname = config.get(step, 'byname') if config.has_option(step, 'byname') else None
        byxpath = config.get(step, 'byxpath') if config.has_option(step, 'byxpath') else None
        byclass = config.get(step, 'byclass') if config.has_option(step, 'byclass') else None
        bytext = config.get(step, 'bytext') if config.has_option(step, 'bytext') else None

        targetisdisplayed = config.get(step, 'targetisdisplayed') if config.has_option(step, 'targetisdisplayed') else None
        targetisenabled = config.get(step, 'targetisenabled') if config.has_option(step, 'targetisenabled') else None
        targetisselected = config.get(step, 'targetisselected') if config.has_option(step, 'targetisselected') else None
        targetisdisplayed = config.get(step, 'targetisdisplayed') if config.has_option(step, 'targetisdisplayed') else None
        targettext = config.get(step, 'targettext') if config.has_option(step, 'targettext') else None
        targettag = config.get(step, 'targettag') if config.has_option(step, 'targettag') else None
        targetid = config.get(step, 'targetid') if config.has_option(step, 'targetid') else None

        assertElement(driver=driver, byid=byid, byname=byname, byxpath=byxpath, byclass=byclass, bytext=bytext, targetisdisplayed=targetisdisplayed, targetisenabled=targetisenabled,
                      targetisselected=targetisselected, targettext=targettext, targettag=targettag, targetid=targetid)

def click_button(driver=None, byid=None, byname=None, byxpath=None, byclass=None):
    userElement = None
    if not driver:
        return

    if byid:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.ID, byid))
        )
        userElement = driver.find_element_by_id(byid)
    elif byname:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.NAME, byname))
        )
        userElement = driver.find_element_by_name(byname)
    elif byxpath:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.XPATH, byxpath))
        )
        userElement = driver.find_element_by_xpath(byxpath)
    elif byclass:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.CLASS_NAME, byclass))
        )
        userElement = driver.find_element_by_class_name(byclass)

    if userElement:
        userElement.click()

def edit_textbox(driver=None, byid=None, byname=None, byxpath=None, sendkeys=None, submit=False):
    usernameEdit = None
    if (not driver) or (not sendkeys):
        return

    if byid:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.ID, byid)))
        usernameEdit = driver.find_element_by_id(byid)
    elif byname:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.NAME, byname)))
        usernameEdit = driver.find_element_by_id(byname)
    elif byxpath:
        WebDriverWait(driver, WEBPAGE_MAX_LOAD_TIME).until(
            EC.element_to_be_clickable((By.XPATH, byxpath)))
        usernameEdit = driver.find_element_by_id(byxpath)

    if usernameEdit:
        usernameEdit.send_keys(sendkeys)
    if submit:
        usernameEdit.submit()

def queryElement(driver=None, byid=None, byname=None, byxpath=None, byclass=None, bytext=None):
    element = None
    if not driver:
        raise Exception('driver not provided')

    if byid:
        element = driver.find_element_by_id(byid)
    elif byname:
        element = driver.find_element_by_name(byname)
    elif byxpath:
        element = driver.find_element_by_name(byxpath)
    elif byclass:
        element = driver.find_element_by_class_name(byclass)
    elif bytext:
        element = driver.find_element_by_link_text(bytext)
    print('  >>>')
    print('  dir(element)=', dir(element))
    print('  location =', element.location)
    print('  id =', element.id)
    print('  text =', element.text.encode(encoding='ascii', errors='replace'))
    print('  tag_name =', element.tag_name)
    print('  is_selected =', element.is_selected())
    print('  is_enabled =', element.is_enabled())
    print('  is_displayed =', element.is_displayed())
    # all attributes: http://www.w3schools.com/jsref/dom_obj_all.asp
    print('  content attributes = ', element.get_attribute('attributes'))
    print('  content dir = ', element.get_attribute('dir'))
    print('  content id = ', element.get_attribute('id'))
    # print('  content inner = ', element.get_attribute('innerHTML'))
    # print('  content outer = ', element.get_attribute('outerHTML'))
    # print('  content = ', driver.execute_script("return arguments[0].innerHTML;", element))
    print('  <<<')

def assertElement(driver=None, byid=None, byname=None, byxpath=None, byclass=None, bytext=None, targetisdisplayed=None, targetisenabled=None, targetisselected=None, targettext=None, targettag=None, targetid=None):
    element = None
    if not driver:
        raise Exception('driver not provided')

    if byid:
        element = driver.find_element_by_id(byid)
    elif byname:
        element = driver.find_element_by_name(byname)
    elif byxpath:
        element = driver.find_element_by_name(byxpath)
    elif byclass:
        element = driver.find_element_by_class_name(byclass)
    elif bytext:
        element = driver.find_element_by_link_text(bytext)

    if targetisdisplayed and not element.is_displayed:
        raise Exception('some element is not displayed')
    if targetisenabled and not element.is_enabled:
        raise Exception('some element is not enabled')
    if targetisselected and not element.is_selected:
        raise Exception('some element is not selected')
   
    expected = targettext.encode(encoding='ascii', errors='replace')
    current = element.text.encode(encoding='ascii', errors='replace') 
    if expected != current:
        raise Exception('some element text is not right')

    if targettag and targettag != element.tag_name:
        raise Exception('some tag name is not right')

    if targetid and targetid != element.get_attribute('id'):
        raise Exception('some id name is not right')


try:
    config = readTestcase('test.ini')
    driver = initDriver()
    prepareEnv(driver)

    for step in getTestSteps(config):
        runStep(config, step)
    print("\nTesting status: SUCCESS")
    time.sleep(5)

except Exception as e:
    print ("Test failed ! Reason =", str(e))
    time.sleep(1)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    raise

finally:
    driver.quit()
