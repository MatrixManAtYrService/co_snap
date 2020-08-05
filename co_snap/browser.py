#! /usr/bin/env python3

description = "launches a browser at the pipeline indicated by --url and logs in"

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from os import environ, path
from collections import namedtuple
import re
import argparse
from inspect import cleandoc
import sys
from co_snap import xpath, cli

# https://stackoverflow.com/questions/16462177/selenium-expected-conditions-possible-to-use-or
class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """

    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except:
                pass


def wait_for_tree(driver):
    # wait until root node is visible
    WebDriverWait(driver, 10).until(
        AnyEc(
            EC.presence_of_element_located((By.XPATH, xpath.root_node_wide)),
            EC.presence_of_element_located((By.XPATH, xpath.root_node_narrow)),
        )
    )


def wait_for_stdout(driver):
    # wait until root node is visible
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, xpath.stdout_box_wide)),
    )
    pass


def pipeline(args):
    user = args.user
    password = args.password
    url = args.url

    # launch browser
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)

    # log in
    root = driver.find_element_by_id("root")
    root.find_element_by_xpath("div/div/form/div/div/input").send_keys(user)
    root.find_element_by_xpath("div/div/form/div[2]/div/input").send_keys(password)
    root.find_element_by_xpath("div/div/form/button").click()

    # wait for load
    wait_for_tree(driver)

    # provide driver to caller
    return driver


def _target_js(xpath):
    return f"""var target = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;\n"""



def _restyle_scrollbars(xpath, width):
    return _target_js(xpath) + cleandoc(
        """
            var styleTag = document.createElement('style');
            var dynamicStyleTag = document.createTextNode(
            "::webkit-scrollbar { width: """ + str(width) + """px; }");
            styleTag.appendChild(dynamicStyleTag);
            target.appendChild(styleTag);
       """
    )


def delete(driver, xpath):
    js = _target_js(xpath) + "target.parentNode.removeChild(target);"
    driver.execute_script(js)


# not sure if this is a good idea, but leaving it here for future tinkering
def hide_scrollbars(driver, xpath, restore_child=None):

    # set scrollbar width to zero
    js = _restyle_scrollbars(xpath, 0)
    print(js)
    driver.execute_script(js)


def launch():
    args = cli.get_args()

    if args.url:
        return pipeline(args.url)


if __name__ == "__main__":
    launch()
