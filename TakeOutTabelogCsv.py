import requests
from bs4 import BeautifulSoup
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import csv
import pprint


#row = 2

for i in range(1, 14):
    #紳士的に1秒スリープ
    time.sleep(1)

    list_url = "https://tabelog.com/takeout_feature_rst_list/index/?page="+str(i)+"&pal=tokyo&LstPrf=A1310"
    #list_url = "https://tabelog.com/takeout_feature_rst_list/index/?page="+str(i)+"&pal=tokyo&LstPrf=A1304"
    #店舗一覧ページに対するBeautifulSoupの設定
    r_list = requests.get(list_url)
    html_list = r_list.content
    soup_list = BeautifulSoup(html_list, "html.parser")

    #店舗一覧ページ内の個別店舗ページURLの抽出
    stores = soup_list.find_all(class_="list-rst__rst-name-target")
    storeURLs = [ x['href'] for x in stores ]

    #各店舗の情報を順番に見ていく。
    for i,target_url in enumerate(storeURLs):
        #CSVとかに吐かせるようにすればスピードアップできそう→した
        with open('/Users/tsutsumi/Documents/Python3/tabelog/csv/test.csv', 'a') as f:
            writerow = [] 

            time.sleep(1)

            r = requests.get(target_url)
            html = r.content
            soup = BeautifulSoup(html, "html.parser")

            #個別店舗の店名を抽出
            #store_name = soup.find(class_="display-name").text
            store_name = soup.find(class_="rstdtl-crumb").text
            print(store_name.split())
            writerow.append(store_name)

            #URL
            writerow.append(target_url)

            #住所を取得
            store_address = soup.find("p", class_="rstinfo-table__address").text
            writerow.append(store_address)

            #エリア
            writerow.append("秋葉原・神田・水道橋")

            #個別店舗の評価を抽出
            rating_score_tag = soup.find('b', class_='c-rating__val')
            rating_score = rating_score_tag.span.string
            writerow.append(rating_score)

            #個別店舗のテイクアウト情報を抽出
            take_out_tag = soup.findAll('div', class_='rstdtl-takeout-info__text')

            namestr = ''
            #個別店舗のテイクアウト情報(通常)を抽出
            for name in take_out_tag[0].text.split():
                namestr = namestr+'\n'+name
            #wks.update_acell('E'+str(row),namestr)
            writerow.append(namestr)
            
            namestr = ''    
            for name in take_out_tag[1].text.split():
                namestr = namestr+'\n'+name
            #wks.update_acell('F'+str(row),namestr)
            writerow.append(namestr)

            #個別店舗のテイクアウト情報(詳細)を抽出
            namestr = ''
            take_out_dtl_tag = soup.findAll('div', class_='rstdtl-takeout-info__dtl')
            for name in take_out_dtl_tag[0].text.split():
                namestr = namestr+'\n'+name
            #wks.update_acell('G'+str(row),namestr)
            writerow.append(namestr)
            namestr = ''        
            for name in take_out_dtl_tag[1].text.split():
                namestr = namestr+'\n'+name
            #wks.update_acell('H'+str(row),namestr) 
            writerow.append(namestr)

            writer = csv.writer(f)
            writer.writerow(writerow)
            #row = row + 1

