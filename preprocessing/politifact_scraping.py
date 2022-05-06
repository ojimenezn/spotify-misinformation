from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.request,sys,time
import pandas as pd
import os

def main(pagesToGet=683):

	upperframe=[]  
	for page in range(1,pagesToGet+1):
	    print('processing page :', page)
	    url = 'https://www.politifact.com/factchecks/list/?page='+str(page)
	    print(url)
	    
	    #an exception might be thrown, so the code should be in a try-except block
	    try:
	        #use the browser to get the url. This is suspicious command that might blow up.
	        page=requests.get(url)                             # this might throw an exception if something goes wrong.
	    
	    except Exception as e:                                   # this describes what to do if an exception is thrown
	        error_type, error_obj, error_info = sys.exc_info()      # get the exception information
	        print ('ERROR FOR LINK:',url)                          #print the link that cause the problem
	        print (error_type, 'Line:', error_info.tb_lineno)     #print error info and line that threw the exception
	        continue                                              #ignore this page. Abandon this and go back.

	    time.sleep(2)   
	    soup=BeautifulSoup(page.text,'html.parser')
	    frame=[]
	    links=soup.find_all('li',attrs={'class':'o-listicle__item'})

	    # print(len(links))
	    # filename="/drive/My Drive/politifact.csv"
	    # f = open(filename,"w", encoding = 'utf-8')
	    # headers="Statement,Link,Date, Source, Label\n"
	    # f.write(headers)
	    
	    for j in links:
	        Statement = j.find("div",attrs={'class':'m-statement__quote'}).text.strip()
	        Link = "https://www.politifact.com"
	        Link += j.find("div",attrs={'class':'m-statement__quote'}).find('a')['href'].strip()
	        Date = j.find('div',attrs={'class':'m-statement__body'}).find('footer').text[-14:-1].strip()
	        Source = j.find('div', attrs={'class':'m-statement__meta'}).find('a').text.strip()
	        Label = j.find('div', attrs ={'class':'m-statement__content'}).find('img',attrs={'class':'c-image__original'}).get('alt').strip()
	        frame.append((Statement,Link,Date,Source,Label))
	        # f.write(Statement.replace(",","^")+","+Link+","+Date.replace(",","^")+","+Source.replace(",","^")+","+Label.replace(",","^")+"\n")
	    upperframe.extend(frame)
	# f.close()
	df = pd.DataFrame(upperframe, columns=['Statement','Link','Date','Source','Label'])

	save_dir = f"./outputs"

	if not os.path.isdir(save_dir):
		os.mkdir(save_dir)

	save_fp = f"{save_dir}/politifact_filtered.csv"

	df.to_csv(save_fp, index=False)


def filter_data(df):
	cond = ~df.Label.eq('full-flop') & ~df.Label.eq('half-flip') & ~df.Label.eq('no-flip')
	return df[cond]

if __name__ == "__main__":
	main()

