import re
import json
import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize


def header():
    tr1 = open("greatagain", "r")
    tr2 = open("trtwi", "r")

    text1 = tr1.readlines()
    text2 = tr2.readlines()
    
    trump1 = ""
    trump2 = ""
    trump1 = trump1.join(text1)
    trump2 = trump2.join(text2)
    print(trump1)
    print(trump2)



def get_page(addr, hdr):
    req = urllib.request.Request(addr, headers=hdr)

    try:
        page = urllib.request.urlopen(req)
        return page
    except(urllib.request.HTTPErrorProcessor, e):
        print(e.fp.read())

def get_links(page):
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("a")
    #print(links)

    return links

def db_links(links, keyword):
    news_links = []
    key_links = []

    for link in links:
        link = link.get("href").lower()
        if link[0] == '/' and link[1] == 'n':
            link = db + link[1:]
            news_links.append(link)

    for link in news_links:
        if keyword in link:
            key_links.append(link)

    return key_links

def ap_links(links, keyword):
    news_links = []
    key_links = []

    for link in links:
        link = link.get("href").lower()
        if "politikk" in link or "norge" in link or "verden" in link or "okonomi" in link:
            news_links.append(link)

    for link in news_links:
        if keyword in link:
            key_links.append(link)

    return key_links

def get_articles(links):
    articles = []
    
    for link in links:
        r = requests.get(link)
        body = r.text

        soup = BeautifulSoup(body, "html.parser")
        articles.append(soup)

    return articles

def refine_articles(articles):
    refined_articles = []

    for article in articles:
        title = article.title.getText()
        pars = article.find_all('p')
        text = []
        text.append(title)
        for par in pars:
            text.append(par.getText())

        refined_articles.append(text)

    return refined_articles

def sentiment_analysis(articles, from_lang, hdrs):
    for article in articles:
        resfile = open('output', 'a')
        title = article[0]
        string = "".join(article)

        sentence_list = string.split('.')
        paragraph_sentiments = 0.0
        analyzer = SentimentIntensityAnalyzer()

        resfile.write(title + "\n")
        resfile.write(str(sentence_list))

        for sentence in sentence_list:
            to_lang = "en"
            if (from_lang == "en") or (from_lang == "en-US"):
                translation = sentence
                translator_name = "No translation needed"
            else:
                api_url = "http://mymemory.translated.net/api/get?q={}&langpair={}|{}&de={}".format(sentence, from_lang, to_lang, "sigurd14@gmail.com")
       
                response = requests.get(api_url, headers=hdrs)
                response_json = json.loads(response.text)
                translation = response_json["responseData"]["translatedText"]
                translator_name = "MemoryNet Translation Service"

            vs = analyzer.polarity_scores(translation)
            #print("{:-<69} {}".format(translation, str(vs["compound"])))
            paragraph_sentiments += vs["compound"]

        resfile.write("\n")
        resfile.write(str(round(paragraph_sentiments/len(sentence_list), 4)))
        resfile.write("\n")
        resfile.write("-----------------\n\n")
        # print("Article title: \t", title)
        print("Average sentiment for article: \t", str(round(paragraph_sentiments/len(sentence_list), 4)), "Article title: \t", title)
        resfile.close()

def analyze(link, hdrs, keyword):
    page = get_page(link, hdrs)
    links = get_links(page)

    if "dagbladet" in link:
        special_links = db_links(links, keyword)
    elif "aftenposten" in link:
        special_links = ap_links(links, keyword)
    articles = get_articles(special_links)
    refined_articles = refine_articles(articles)

    sentiment_analysis(refined_articles, "no", hdrs)




if __name__ == "__main__":
    header()
    db = "http://www.dagbladet.no/emne/utenriks/"
    vg = "http://www.vg.no/nyheter/"
    ap = "http://www.aftenposten.no/nyheter/"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    analyze(db, hdr, "trump")
    analyze(ap, hdr, "trump")

    #page = get_page(ap, hdr)
    #links = get_links(page)
    #special_links = ap_links(links, "trump")
    #print(special_links)
    #articles = get_articles(special_links)
    #refined_articles = refine_articles(articles)
    #sentiment_analysis(refined_articles, "no", hdr)

    #analyze(db, hdr)

