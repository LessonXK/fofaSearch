#!/usr/bin/env python
#coding:utf8

#author: xiaokong

import requests
import argparse
import re
import base64
import time
import chardet

class Fofa(object):
    
    fofa_dest = "https://fofa.so/result"
    fofa_param = {"page": 1, "qbase64": None}
    
    def __init__(self, auth):
        
        self.auth = auth
    
    def searchResult(self, q):
    
        regRel = re.compile('(\d{1,5})</a> <a class=', re.IGNORECASE)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Cookie': self.auth}
        self.fofa_param['qbase64'] = q
        total_result = 0
        
        try:
            r = requests.get(self.fofa_dest, params=self.fofa_param, timeout=10, headers=headers)
            r.raise_for_status()
            total_result = re.search(regRel, r.content).group(1)
            for i in range(1, int(total_result)+1):
                if self.__searchResultByPage(i, headers) == False:
                        break
                time.sleep(1)
        except Exception as e:
            print str(e)
            
    def __searchResultByPage(self, page, headers):

        result = list()
        try:
            self.fofa_param['page'] = page
            r = requests.get(self.fofa_dest, params=self.fofa_param, timeout=10, headers=headers)
            r.raise_for_status()
            urls = re.findall('<a target="_blank" href="(.*?)">', r.content)
            for url in urls:
                print url
                result.append(url+'\n')
        except KeyboardInterrupt as e:
            return False
        except Exception as e:
            #print str(e)
            time.sleep(10)
            self.__searchResultByPage(page, headers)
            

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-r', '--rule', dest='rule', help='search rule by base64encode')
    parser.add_argument('-c', '--cookie', dest='cookie', help='login cookie')
    parser.add_argument('-o', dest='out', type=argparse.FileType('wt'), help='save result')  
    
    p = parser.parse_args()
    if p.rule and p.cookie:
        result = Fofa(p.cookie).searchResult(p.rule)
        if p.out:
            p.out.writelines(result)
            p.out.close()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()