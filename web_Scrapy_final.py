
# coding: utf-8

# In[1]:

from lxml import html
import requests
import json


# In[29]:

import urllib2

def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url



# In[2]:

def color_string(color_list):
    col_str = ''
    
    for col in color_list:
        if not "Select" in col:
            col_str = col_str + " " + col
    col_str.replace("[out of stock]", " ")
    return col_str


# In[3]:

count =0
prod_info = []

for i in range(1,50):  #corresponds to page range
    
    page = requests.get('http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=iphone+6&_pgn='+ str(i) + '&_skc=50&rt=nc')
    main_tree = html.fromstring(page.content)
    
    
    items_id = main_tree.xpath("//li/@id")
    for item in items_id:   # corresponds to items displayed on the page
        if "item" in item:
            item_url = main_tree.xpath('//*[@id=' +  '"'+ item + '"' +']/h3/a[@title]/@href')
            print item_url
            print '---------'
            try:
                item_page = requests.get(item_url[0],allow_redirects=False,timeout=10)
            except requests.ConnectionError as e:
                continue
            except requests.ReadTimeout as re:
                continue
            item_tree = html.fromstring(item_page.content)
            item_name = item_tree.xpath('//*[@id="itemTitle"]/text()') # name
            if len(item_name)==0:
                item_name = ['NA']
            item_price = item_tree.xpath('//*[@id="prcIsum"]/text()') # price
            if len(item_price)==0:
                item_price = ['NA']
            color = item_tree.xpath('//*[@id="msku-sel-1"]/option/text()') # color list
            if len(color)==0:
                color = ['NA']
            sold = item_tree.xpath('//*[@id="why2buy"]/div/div[1]/span/text()') # number of sold items
            if len(sold)==0:
                sold = ['NA']
            ship = item_tree.xpath('//*[@id="fshippingCost"]/span/text()') # shipping cost
            if len(ship)==0:
                ship = ['NA']
            pic = item_tree.xpath('//*[@id="icImg"]/@src')  # pic url
            if len(pic)==0:
                pic = ['NA']
            item_seller = item_tree.xpath('//*[@id="mbgLink"]/span/text()') # item seller
            if len(item_seller)==0:
                item_seller = ['NA']
            item_sell_feedback = item_tree.xpath('//*[@id="si-fb"]/text()') # seller feedback
            if len(item_sell_feedback)==0:
                item_sell_feedback = ['NA']
        
            item_bids = item_tree.xpath('//*[@id="vi-VR-bid-lnk"]/span[1]/text()')  # number of bids
            if len(item_bids)==0:
                item_bids = ['NA']
            item_views = item_tree.xpath('//*[@id="vi_notification_new"]/span/text()') #number of views
            if len(item_views)==0:
                item_views = ['NA']

            
                
                
            prod_dict = {'Name' : item_name[0] , 'Price' : item_price[0] ,  'color' : color_string(color) , 'Number sold' : sold[0],'ship' : ship[0],  'product_url' : item_url[0] ,   'pic' : pic[0] , 'SellerFeedback' : item_sell_feedback[0].encode('utf-8') , 'number_of_bids' : item_bids[0],'number_of_views': item_views[0]}
            count = count + 1
            prod_info.append(prod_dict)
        
        
json_file = open('product.json','w')
json.dump(prod_info,json_file)
            
            
