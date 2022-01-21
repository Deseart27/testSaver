import base64
import io
import json
import os
import time

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from selenium import webdriver

from .forms import UserForm


def YanportSaver(study_url):

    buffer = io.BytesIO()

    file_directory = '.'
    # set webdriver and set chrome_options/settings
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
        True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4 210 x 297 mm"
        },
    }
    chrome_options.add_argument('--enable-print-browser')
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--lang=eng')


    prefs = {
        "download.default_directory": file_directory,
        'printing.print_preview_sticky_settings.appState':
        json.dumps(settings),
        'savefile.default_directory': file_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # set chrome bin location & driver (change paths to run locally)
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options)

    driver.get(study_url)
    driver.maximize_window()

    # necessary for webpage to fully load
    #time.sleep(3)

    #driver.execute_script(f'document.title="hello.pdf";window.print();')

    #driver.execute_script('document.title="my_test_file1.pdf";window.print();')
    driver.get_screenshot_as_file('testBonjour.png')
    driver.close()

    #TryValue2 = os.listdir("tmp")
    #buffer.seek(0)

    #TryValue2 = buffer.read()
    #return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


    #check all files in app
    path ="."
    TryValue = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #append the file name to the list
            TryValue.append(os.path.join(root, file))
    return str(TryValue)


def FunkyFunc():
    return "bonJUR"


# makes the form dynamic
def index(request):
    submitbutton = request.POST.get("submit")

    study_url = ''
    test_value = ''
    form = UserForm(request.POST or None)
    if form.is_valid():
        study_url = form.cleaned_data.get("study_url")
        #YanportSaver(study_url)
        test_value = YanportSaver(study_url)

    context = {
        'form': form,
        'study_url': study_url,
        'submitbutton': submitbutton,
        'test_value' : str(test_value)
    }

    return render(request, 'index.html', context)
