from bs4 import BeautifulSoup
from urllib import request as urlrequest
from urllib.request import urlopen
import os
import sys




import requests
from lxml.html import fromstring


initalPaperid = int(sys.argv[1])
finalPaperid = int(sys.argv[2])



def error_sound():
    os.system('say " Fatal error occured."')
    
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:500]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

import urllib
from random import random
    

def url_to_beautifulsoup(full_url, proxy_list, timeout = 10):
   
    proxy = proxy_list[0]
    count = 0
    while(count < 50):
        try:
            content = requests.get(full_url,proxies={"http": proxy, "https": proxy}, timeout=timeout)
            soup = BeautifulSoup(content.text)
            if "Forbidden" in str(soup.find_all("title")[0]):
                count = count + 1
                proxy = proxy_list[int(random() * len(proxy_list))]
            else:
                return soup
        except requests.exceptions.RequestException as err:
            print("Connection Error or Timeout:" + str(err))
            count = count + 1
            proxy = proxy_list[int(random() * len(proxy_list))]
        except:
            print("Abnormal error when extracting: %s" %(full_url))
            count = count + 1
            proxy = proxy_list[int(random() * len(proxy_list))]
                            
    print("Reached 50 trials for connections.")
    return None
    


    
    
    
output_abstract_path = "full_paper_lenght.dat"

dict_keys= ['Id',
            'og:title',
            'og:site_name',
            'citation_online_date',
            'citation_title',
            'citation_author',
            'citation_pdf_url',
            'citation_arxiv_id',
            'og:description',
            'twitter:site',
            'citation_date',
            'twitter:title',
            'twitter:description',
            'og:url',
            'category']

delimiter = "||||"



def find_category(url):
    for link in get_href(url):
        if "?context" in link:
            return(link.split("=")[1])
            break
def extract_paper_information(full_link, proxy):
    info_dict = {}
    
    separator_within_key = " || "
    
    
    soup = url_to_beautifulsoup(full_link, proxy)
    if soup == None:
        return None
        
    all_href = soup.find_all("a")
    links = []
    category = "None"
    for link in all_href:
        if "?context" in link.get('href'):
            category = link.get('href').split("=")[1]
            break    
    info_dict ["category"] = category
    meta = soup.find_all("meta")
    for meta_scan in meta:
        content_meta = meta_scan.get("content")
        property_meta = meta_scan.get("property")
        name_meta = meta_scan.get("name")
        if (property_meta != None):
            key = property_meta
        elif (name_meta != None):
            key = name_meta
        else:
            continue
            
        key_in_info_dict = info_dict.keys()
        if key in key_in_info_dict:
            initial_value = info_dict[key]
            current_value = content_meta
            joined_value = separator_within_key.join([initial_value,current_value])
            info_dict[key] = joined_value
        else:
            info_dict[key] = content_meta
            
        
    return info_dict


def write_to_file(file,info_dict,dict_keys,index):
    key_in_dict = info_dict.keys()
    file.write(str(index))
    file.write(delimiter)
    for key in dict_keys:
        if key in key_in_dict:
            file.write(str(info_dict[key]).replace("\n"," "))
            file.write(delimiter)
        else:
            file.write("None")
            file.write(delimiter)
    file.write("\n")

import time
from random import random
initial_count = initalPaperid
final_count = finalPaperid
output_paper_info = "paper_axrive_info_%d.dat"%(initial_count)
output_paper_log = "paper_axrive_info_%d.log"%(initial_count)
output_abstract_path = "full_paper_lenght.dat"

        
inFile = open(output_abstract_path,"r")
lines = inFile.readlines()
inFile.close()

outfilelog = open(output_paper_log,"w")
outfilelog.close()

outfile = open(output_paper_info,"w")
outfile.write("#")
for key in dict_keys:
    outfile.write(key)
    outfile.write(delimiter)
outfile.write("\n")
outfile.close()
proxy = list(get_proxies())
print("Proxy generated")
len_proxy = len(proxy)
print(len_proxy)
print(initial_count)
print(final_count)
for index, link in enumerate(lines[initial_count:]):
    index = index + initial_count
    if (index) > final_count:
        print("All papers content extracted.")
        break

    if ((index+1) % 100 == 0):
        proxy = list(get_proxies())
        print("Proxy generated")


        
        
    try:    
        info_dict = extract_paper_information(link, proxy)
        if(len(list(set(info_dict.values())))==1) and info_dict == None:
            print("%d line not read. Link: %s"%(index,link))
            outfilelog = open(output_paper_log,"a")
            outfilelog.write("%d line not read. Link: %s"%(index,link))
            outfilelog.close()
                        
            continue
        outfile=open(output_paper_info,"a")
        write_to_file(outfile,info_dict,dict_keys,index)
        outfile.close()
        print("%d line read. Link: %s"%(index ,link))


    
    except:
        print("%d link not read. Abnormal Error. Link: %s"%(index,link))
        outfilelog = open(output_paper_log,"a")
        outfilelog.write("%d line not read. Link: %s"%(index,link))
        outfilelog.close()
        continue
