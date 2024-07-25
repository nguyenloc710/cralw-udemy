import json
import time

import requests


def getDataCategories():
    url = "https://www.udemy.com/api-2.0/structured-data/navigation-lists/"
    params = {
        "list_ids": "ud-main",
        "locale": "en_US"
    }
    # Make the GET request
    response = requests.get(url, params=params)

    # Check the response status and print the JSON response if successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return None


def getCoursesByCategory(category_id, page_size, page):
    # page_size max = 60
    url = "https://www.udemy.com/api-2.0/discovery-units/all_courses/"
    params = {
        "p": page,
        "page_size": page_size,
        "subcategory": "",
        "instructional_level": "",
        "lang": "",
        "price": "",
        "duration": "",
        "closed_captions": "",
        "subs_filter_type": "",
        "category_id": category_id,
        "source_page": "category_page",
        "locale": "en_US",
        "currency": "vnd",
        "navigation_locale": "en_US",
        "skip_price": "true",
        "sos": "pc",
        "fl": "cat"
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check the response status and print the JSON response if successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data {response.status_code}: {response.json()}")
    return None


def run(categories):
    with open("output.txt", "w") as file:
        for category in categories:
            print(category["sd_tag"]["title"])
            category_id = category["sd_tag"]["id"]
            page = 1
            sleep = 0
            while True:
                try:
                    print(f"{page}: {category["sd_tag"]["title"]}")
                    raw_courses = getCoursesByCategory(category_id, 60, page)
                    if raw_courses is None:
                        break
                    else:
                        courses = raw_courses["unit"]["items"]
                        if len(courses) == 0:
                            break
                        for course in courses:
                            course_string = json.dumps(course)
                            file.write(course_string + ",")
                    page += 1
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    sleep += 1
                    if sleep > 5:
                        break


if __name__ == '__main__':
    raw_categories = getDataCategories()
    categories = raw_categories["ud-main"]["items"]
    run(categories)
