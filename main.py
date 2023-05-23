import os
import sys
from bs4 import BeautifulSoup
from rich.console import Console
from rich.theme import Theme

IG_NAME_CLASS = "x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"

DEFAULT_INPUT_PATH = "input"
DEFAULT_EXCLUDE_PATH = os.path.join(DEFAULT_INPUT_PATH, "exclude.pnp")
DEFAULT_PARSE_MODE = "html.parser"

ERROR_THEME = Theme({'error': 'bold red'})
SUCCESS_THEME = Theme({
    'success': 'bold green',
    'out': 'italic bold blue'
    })

OUT_THEME = Theme({'out': 'blue'})

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

def write_output(intersection: list, users: list):
    out_pattern = '<------------------------------------------------------------------------------>'

    with open('out.txt', 'w') as file:
        sys.stdout = file
        i_output = ''
        u_output = ''

        for u in intersection:
            i_output = i_output + u + '\n'

        for u in users:
            u_output = u_output + u + ' '

        print(f'Common Followers: {u_output}\n')
        print(f'{out_pattern}\n\n{i_output}\n\n{out_pattern}')

        sys.stdout = sys.__stdout__

def exit_unsufficient():
    Console(theme=ERROR_THEME).print("[error]ERROR: Not enough pnp comparison files provided![/error]")
    sys.exit(1)

def exit_unread():
    
    Console(theme=ERROR_THEME).print("[error]ERROR: No files were read![/error]")
    sys.exit(1)

def main():
    file_names = []
    user_sets = []
    exclude_set = []

    if not (os.path.exists(DEFAULT_INPUT_PATH) and os.path.isdir(DEFAULT_INPUT_PATH)):
        os.makedirs(DEFAULT_INPUT_PATH)
        exit_unread()

    for file in os.listdir(DEFAULT_INPUT_PATH):
        if os.path.isfile(os.path.join(DEFAULT_INPUT_PATH, file)) and '.pnp' in file:
            if not (file == 'exclude.pnp'):
                file_names.append(file)

    if not len(file_names):
        exit_unread()

    elif len(file_names) == 1:
        exit_unsufficient()

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

    write_output(intersection, file_names)

    Console(theme=SUCCESS_THEME).print("[success]SUCCESS: Results are written to [/success][out]out.txt[/out][success]![/success]")

    sys.exit(0)

if __name__ == "__main__":
    main()