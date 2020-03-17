import pandas as pd
import os
import numpy as np
import re, json, os, requests, scipy.misc
import matplotlib.pyplot as plt
import lxml.html as lh
from bs4 import BeautifulSoup, NavigableString, Tag
from skimage import io, data
from skimage.color import rgb2gray
from skimage.color import rgb2hsv
from scipy import ndimage
from sklearn.decomposition import PCA


full_list_images = []
def data(urls, outpath): 
    total_list = {}
   
    for u in urls: 
        page = requests.get(u)
        soup = BeautifulSoup(page.content,'html.parser')
        tb = soup.find_all('table', class_='main')
        title = soup.find('title').get_text('title')[16:]   

        list_names = []
        images = []
        type_art = []
        for link in tb:
            name = link.find('b')
            text = link.find('br')
            
            list_names.append(name.get_text('title'))
            images.append(link.find('img').get('src'))
    
        meta_data = []
        #br tags
        for br in soup.findAll('br'):
            next_s = br.nextSibling
            if not (next_s and isinstance(next_s,NavigableString)):
                continue
            next2_s = next_s.nextSibling
            if next2_s and isinstance(next2_s,Tag) and next2_s.name == 'br':
                text = str(next_s).strip()
                if text:
                    meta_data.append(text)
        
        full_list_images.append(images)
        total_list[title] = list_names,images,meta_data
        if not os.path.exists(outpath):
            os.mkdir(outpath)
    return total_list


def process(data): 
    links = []
    titles = []
    misc_data = []
    for i in data.values(): 
        links.append(i[1])
        titles.append(i[0])
        misc_data.append(i[2])
    
    df = pd.DataFrame({'name of painting':titles,
                   'img link':links,
                  'info':misc_data}, 
        
                  index=[list(data.keys())])
    l = []
    for i in df['info']: 
        s_l = []
        for j in range(0,len(i),3): 
            s_l.append(i[j+1:j+3])
        l.append(s_l)
    df['l'] = l
    
    #Index by each painting, and not each era 
    list_one = []
    for i in range(len(df['name of painting'])): #go through each era 
        list_two = []
        for j in range(len(df['name of painting'][i])): #go through each list 

            painting = df['name of painting'][i][j]
            era = list(df.index[i])[0]
            link = df['img link'][i][j]        
            moreinfo = []
            for k in df['l'][i][j]:
                moreinfo.append(k)

            list_two.append([era,painting,link,moreinfo[0]])

        list_one.append(list_two)
    tolist = [j for i in list_one for j in i ]
    big_df = pd.DataFrame(tolist)
    big_df = big_df.rename(columns={0:'era', 1:'painting', 2:'url', 3:'metadata'})

    #painting or drawing
    paintdraw = []
    for i in big_df['metadata']:
        if 'paint' in i or 'canvas' in i:
            paintdraw.append('Painting')
        elif 'paper' in i:
            paintdraw.append('Drawing')
        else: 
            paintdraw.append('N/A')
    big_df['painting or drawing'] = paintdraw
    big_df['metadata'] = big_df['metadata'].str.replace('\n','').str.replace(' ','')
    big_df['metadata'] = big_df['metadata'].str.split(',')

    #separate type and dimensions
    big_df["type"] = big_df["metadata"].str[0]
    big_df['dimensions'] = big_df['metadata'].str[1]
    big_df = big_df.drop(columns=['metadata'])

    return big_df


#driver function
def get_data(urls,outdir, **kwargs): 

	if not os.path.exists(outdir):
		os.mkdir(outdir)
	x = data(urls, **kwargs)
	cfg = json.load(open('config_a1.json'))  
	df = process(x)
	df.to_csv(os.path.join(outdir,'df.csv'))

	return