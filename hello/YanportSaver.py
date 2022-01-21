from django.shortcuts import render
from django.http import HttpResponse
import requests
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


def YanportSaver(study_url):

    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId":
        "Save as PDF",
        "version":
        2,
        "isCssBackgroundEnabled":
        True
    }
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings)
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options)

    driver.get(study_url)

    time.sleep(3)

    driver.execute_script('window.print();')
    driver.quit()
