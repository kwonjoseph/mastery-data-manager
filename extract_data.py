import page_util as page
import rubric_dict as keys
import re


creds = page.get_login()
raw = page.get_page(*creds)

keylist=keys.KEYS()

dict = {}

def regex_gen():
    keys = []
    for key in keylist:
        regex = '(?<=class=\"'+keylist[key]+'\">)(.*?)(?=\<\/)'
        keys.append([key, regex])
    return keys

def rubric(regex_keys):
    title = re.findall(regex_keys[0][1], raw)
    criteria = re.findall(regex_keys[1][1], raw)
    descriptions = re.findall(regex_keys[2][1], raw)
    level_titles = re.findall(regex_keys[3][1], raw)
    point_values = re.findall(regex_keys[4][1], raw)
    
    criteria = list(dict.fromkeys(criteria))
    
    rubric = {}

    rubric['title'] = title[0]
    rubric['criteria'] = []
    for i in range(0, len(criteria)):
        rubric['criteria'].append({'criterion'+str(i): criteria[i], 'content': []})
        for j in range(((i+1)*3)-3, (i+1)*3):
            rubric['criteria'][i]['content'].append({'description': descriptions[j], 'level title': level_titles[j], 'point value': point_values[j]})
    return rubric
    






