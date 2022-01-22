import base64
import json
import os
import time
import base64

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.http import FileResponse

from .forms import UserForm



def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def get_pdf_from_html(driver,
                      url,
                      print_options={},
                      output_file_path="example.pdf"):
    driver.get(url)
    time.sleep(5)
    calculated_print_options = {
        'landscape': False,
        'displayHeaderFooter': True,
        'printBackground': True,
        'preferCSSPageSize': True,
    }
    calculated_print_options.update(print_options)
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    data = base64.b64decode(result['data'])
    with open(output_file_path, "wb") as f:
        f.write(data)

def YanportSaver(study_url):
    webdriver_options = Options()
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        options=webdriver_options)
    get_pdf_from_html(driver, study_url)
    driver.quit()




def index(request):
    # makes the form dynamic + returns index when form is not completed, and
    # file once it's done
    submitbutton = request.POST.get("submit")

    study_url = ''
    test_value = ''
    form = UserForm(request.POST or None)
    if form.is_valid():
        study_url = form.cleaned_data.get("study_url") #retrieve study_url
        YanportSaver(study_url) #call the func that creates and dl pdf
        response = FileResponse(open('../app/example.pdf', 'rb'))
        return response

    context = {
        'form': form,
        'study_url': study_url,
        'submitbutton': submitbutton,
        'test_value' : str(test_value)
    }

    return render(request, 'index.html', context)
