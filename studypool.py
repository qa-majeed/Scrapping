# Scrap studypool site

import os
import requests
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm

def write_json(f_obj = '', data = ''):
    assert f_obj, 'File object is empty.'
    json.dump(data, f_obj)
    f_obj.close()

def scrap_site(lnk = ''):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    res = requests.get(lnk, headers= headers)
    raw_data = res.text
    res.close()
    raw_data = raw_data.split('\n')
    excerpt = raw_data[3][51:-4]   
    # description = raw_data[4][63:-4]
    description = res.text.split('<div class="user-generated-description">')[1]
    description = description.split('<div>')[0]

    title = ''
    i = 950
    while (True):
        try:
            if raw_data[i] == '<label for="" class="tag-section-title">Subject</label>':
                # try:
                # print(raw_data[i+1])
                title = raw_data[i+1].split('>')[1].split('<')[0]
                break
            i +=1
        except:
            print("Issue occurred: {}".format(lnk))
            return ''
    return {'excerpt': excerpt, 'title': title, 'description':description}


def parse_xml_site(lnk = ''):
    assert lnk, "Input link for xml data."
    # header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    res = requests.get(lnk, headers = headers)
    file_path = lnk.split('/')[-1].split('.')[0] + '.json'
    site_dict = dict()
    root = ET.fromstring(res.text)
    res.close()

    i = 0
    for child in tqdm(root):
        scrap_link = root[i][0].text
        # print(scrap_link)
        data = scrap_site(scrap_link)
        i+=1
        if data == '':
            continue
        site_dict.update({i: data})
        if i % 300 == 0:
            # Json writing
            if not (os.path.exists(file_path)):
                json_file =  open(file_path, 'w+', encoding='utf-8')
                write_json(json_file, site_dict)
            else:
                print("\n{} links has been parseed from site: {}".format(i, lnk))
                print()
                json_file =  open(file_path, 'r+', encoding='utf-8')
                temp = json.load(json_file)
                temp.update(site_dict)
                json_file.seek(0)
                write_json(json_file, temp)
            site_dict = {}
    
    json_file =  open(file_path, 'r+', encoding='utf-8')
    temp = json.load(json_file)
    temp.update(site_dict)
    json_file.seek(0)
    write_json(json_file, temp)
    

link_files = './sites.txt'
with open(link_files) as f:
    sites = f.readlines()
    for lnk in sites:
        lnk = lnk.split('\n')[0]
        # print(lnk)
        xml_data = parse_xml_site(lnk)
        break
print('Done!')

# https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/


# <!--googleoff: index--><p></p><!--googleon: index--><p>