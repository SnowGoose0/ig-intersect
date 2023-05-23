import os
import sys
from bs4 import BeautifulSoup

IG_NAME_CLASS = "x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"

DEFAULT_INPUT_PATH = "input"
DEFAULT_EXCLUDE_PATH = os.path.join(DEFAULT_INPUT_PATH, "exclude.txt")
DEFAULT_PARSE_MODE = "html.parser"

def get_user_set(file_path: str) -> list:
    html_content = ''
    user_set = []

    with open(file_path, 'r') as file:
        html_content = file.read()

    html_soup = BeautifulSoup(html_content, DEFAULT_PARSE_MODE)
    user_tags = html_soup.find_all('div', class_=IG_NAME_CLASS)

    for t in user_tags:
        user_set.append(t.text)

    return user_set

def exit_unread():
    print("No files read")
    sys.exit(1)

def main():
    file_names = []
    user_sets = []
    exclude_set = []

    if not (os.path.exists(DEFAULT_INPUT_PATH) and os.path.isdir(DEFAULT_INPUT_PATH)):
        os.makedirs(DEFAULT_INPUT_PATH)
        exit_unread()

    for file in os.listdir(DEFAULT_INPUT_PATH):
        if os.path.isfile(os.path.join(DEFAULT_INPUT_PATH, file)) and '.txt' in file:
            if not (file == 'exclude.txt'):
                file_names.append(file)

    if not len(file_names):
        exit_unread()

    for f in file_names:
        rfp = os.path.join(DEFAULT_INPUT_PATH, f)
        user_sets.append(get_user_set(rfp))

    set_count = len(user_sets)
    intersection = []
    user_table = {}

    if os.path.isfile(DEFAULT_EXCLUDE_PATH):
        exclude_set = get_user_set(DEFAULT_EXCLUDE_PATH)

    for set in user_sets:
        for user in set:
            if user in user_table:
                rep_count = user_table[user] + 1

                if rep_count == set_count:
                    intersection.append(user)
                
                user_table[user] = rep_count

            else:
                user_table[user] = 1

    if len(exclude_set) > 0:
        for excluded_user in exclude_set:
            if excluded_user in intersection:
                intersection.remove(excluded_user)

    print(intersection)
    print(exclude_set)

    sys.exit(0)


if __name__ == "__main__":
    main()