import requests as r
import urllib.parse
from bs4 import BeautifulSoup as bs
from time import time
def get_moviename_from_link(magnet_link:str):
    parsed = urllib.parse.urlparse(magnet_link)
    query_params = urllib.parse.parse_qs(parsed.query)
    return query_params.get('dn', [''])[0].replace('+', ' ')
def extract_page(link:str)->str:
   response=r.get(link)
   return response
def getmovie_link(moviename:str,all_links=False):
    moviename="|".join(moviename.split()) if " " in moviename else moviename
    print(f"Searching Links for {moviename}")
    link1=f"https://www-1tamilmv-com.translate.goog/index.php?/search/&q={moviename}&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp"
    page1=extract_page(link1).text
    soup=bs(page1,"html.parser")
    links= [link.get("href") for link in soup.select('h2.ipsType_reset a')]
    magnet_links=[]
    for link in links:
        curpage=extract_page(link).text
        soup=bs(curpage,"html.parser")
        a_tags=soup.findAll("a",class_="skyblue-button")
        if a_tags:
            magnet_links.extend(link.get("href")for link in a_tags)
            if not all_links:
                return magnet_links
            else:
                pass
        else:
            pass
    return magnet_links  
if __name__=="__main__":
    start_time=time()
    links=getmovie_link("peaky blinders")
    names=[get_moviename_from_link(i) for i in links]
    end_time=time()-start_time
    print(f"{end_time:.2f}s")
    
