import os
from bs4 import BeautifulSoup

IG_NAME_CLASS = "x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"

DEFAULT_INPUT_PATH = "input"
DEFAULT_PARSE_MODE = "html.parser"

def get_user_set(file_path: str) -> list:
    html_content = ''
    user_set = []

    with open("input/jas.txt", 'r') as file:
        html_content = file.read()

    html_soup = BeautifulSoup(html_content, DEFAULT_PARSE_MODE)
    user_tags = html_soup.find_all('div', class_=IG_NAME_CLASS)

    for t in user_tags:
        user_set.append(t.text)

    return user_set

def main():
    file_names = []
    user_sets = []

    if not (os.path.exists(DEFAULT_INPUT_PATH) and os.path.isdir(DEFAULT_INPUT_PATH)):
        os.makedirs(DEFAULT_INPUT_PATH)
        print("Nothing to be read")
        return -1

    for file in os.listdir(DEFAULT_INPUT_PATH):
        if os.path.isfile(os.path.join(DEFAULT_INPUT_PATH, file)) and ".txt" in file:
            file_names.append(file)

    if len(file_names) == 0:
        print("Nothing to be read")
        return 0

    for f in file_names:
        print(get_user_set(os.path.join(DEFAULT_INPUT_PATH, f)))
        user_sets.append(get_user_set(os.path.join(DEFAULT_INPUT_PATH, f)))

    return 0


if __name__ == "__main__":
    main()