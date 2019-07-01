import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup

root_url = "https://www2.eecs.berkeley.edu"
url = "https://www2.eecs.berkeley.edu/Scheduling/CS/schedule.html"
TWENTY_MIN_SECONDS = 1200


def populate_classes():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    classes_lst = []

    #Get URLs to all CS class pages
    for x in soup.findAll('a', href=True):
        if re.search(r"CS.*\d+", x.get_text()):
            #Found a class
            class_url = root_url + x['href']
            classes_lst += [class_url]

    return classes_lst


def get_prereqs(classes):
    prereqs = {}
    for class_URL in classes:
        response = requests.get(class_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        course = class_URL.split("/").pop()
        if "Prerequisites" in soup.get_text():
            prereq = [x for x in soup.findAll("p") if "Prerequisites" in x.get_text()].pop()
            matches = re.findall(r"\w*\d+\w*", str(prereq))
            matches = set(matches)
            prereqs[course] = str(matches)
    return prereqs

classes_lst = populate_classes()
prereqs = get_prereqs(classes_lst)
for classefhsjkf in prereqs.keys():
    print(classefhsjkf + ": " + prereqs[classefhsjkf])