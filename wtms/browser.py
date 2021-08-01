import os
from datetime import datetime
from typing import NamedTuple, AnyStr, Hashable, Any, Dict
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.common.exceptions import TimeoutException
from functools import wraps

d = os.path.dirname(__file__)
fname = os.path.join(d, "xpath.yaml")
with open(fname, "r", encoding="utf-8") as f:
    xpath: Dict[Hashable, Any] = yaml.load(f, Loader=yaml.FullLoader)["XPATH"]

TIMESTAMP1 = datetime.now().strftime("%Y%m%d_%H%M%S")
logger = logging.getLogger(__name__)

def click_element(driver, xpath) -> None:
    driver.find_element_by_xpath(xpath).click()

def input_text(driver, xpath, text) -> None:
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(Keys.CONTROL + "a");
    element.send_keys(Keys.DELETE);

    element.send_keys(text)
    logger.debug("text={}, TF={}".format(text, element.get_attribute("value")))

class WaitCondition(NamedTuple):
    timeout:int = 15
    xpath:AnyStr= None

class Credential(NamedTuple):
    id:str
    pwd:str


def wait_until_presence(driver, wc:WaitCondition):
    """
    Tag lib, function type with arguments
    Wait for presence of the web element

    :Parameters:
        - driver:selenium.webdriver
        - wc: browser.WaitCondition
    :Returns:
        - function return
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Enter wait_until_presence tag，Func={}".format(func.__name__))
            logger.debug("timeout={}, xpath={}".format(wc.timeout, wc.xpath))
            try:
                WebDriverWait(driver, wc.timeout).until(EC.presence_of_element_located((By.XPATH, wc.xpath)))
                return func(*args, **kwargs)
            except TimeoutException as e:
                e.msg = "func={}".format(func.__name__)
                raise e

        return wrapper

    return decorate

def click_until_presence(driver, wc:WaitCondition):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Enter open_function tag, Func={}".format(func.__name__))
            try:
                element = WebDriverWait(driver, wc.timeout).until(EC.presence_of_element_located((By.XPATH, wc.xpath)))
                element.click()
                return func(*args, **kwargs)
            except TimeoutException as e:
                e.msg = "func={}".format(func.__name__)
                raise e
        return wrapper
    return decorate


def loginWithCredentials(driver, credential: Credential):
    input_text(driver, xpath["LOGIN_ID_TF"], credential.id)
    input_text(driver, xpath["LOGIN_PWD_TF"], credential.pwd)
    click_element(driver, xpath["LOGIN_SUBMIT_BTN"])





