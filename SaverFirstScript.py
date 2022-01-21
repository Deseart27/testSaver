from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

def YanportSaver():
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
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    #driver = webdriver.Chrome(ChromeDriverManager().install(),
        #                    options=chrome_options)

    # test lines
    driver.get("https://medium.com")
    print(driver.page_source)
    print("Finished!")

    '''driver.get(
        "https://app.yanport.com/share/study?url=https:%2F%2Fstorage.googleapis.com%2Fapi.yanport.com%2Fstudies%2Fd483e6d0-2686-11ec-9061-fbd5f33784fe%3FGoogleAccessId%3D430491686678-compute@developer.gserviceaccount.com%26Expires%3D1643708883%26Signature%3DZPZwy3uqGEPRRW%252BuvUDwCejfl0YL4OC1ePhNeU9oL20o%252FU6SNWxr4X6S%252BsEcR7gj39WF5Jfzj5PEQbkUCZsUT4TDoxxEfUuzvkjzHu2TtIRxGI79WWh8gWUvlW%252BKgHi42Dtj6KYcM6dTJZrNBOFCPt5YRakyx7UmerOzcqfen4AjkMnsVqf%252F2jAqWoUmWFD9ZXKmeqmn%252Bgfjc8WcvA0JeBA8HGj88s8xa7aE5ZkGGyHwXSFsrkb6Gv6uX549g7zK37zVz0xSW9tAqmnzGVl%252Fha6zGC4yHThCS131QUcaMW8bwS%252BSz31KUCYWiCB4%252B5fhVgcTySjZKuYeY48w8PXnFw%253D%253D"
    )

    time.sleep(3)

    driver.execute_script('window.print();')
    driver.quit()'''

if __name__ == "__main__":
    YanportSaver()
