from bs4 import BeautifulSoup
import requests
import csv

URL="https://jplang.tufs.ac.jp/int2/at/"

headers_list = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

#Returns soup for a url
def req_soup(url):

    try:
        return BeautifulSoup(requests.get(url, headers=headers_list).text, "html.parser")
    except requests.exceptions.ConnectionError:
        return {"status":"404", "reason":"Connection error occurred"}
    except requests.exceptions.ConnectTimeout:
        return {"status":"408", "reason":"Connection Timeout"}
    except:
        return {"status":"418", "reason":"I'm a teapot"}


#finds number of chapters
def findChptMax():
    try:
        soup = req_soup(URL+"1/1.html").find("ul", {"class":"list-unstyled chapter-only"}).find_all("li")
        return len(soup)
    except:
        print("失敗")
        

#writes csv for chapter
def writeCsv(ChptName, NChpt):

    soup = req_soup(URL+str(NChpt)+"/"+str(NChpt)+".html").find("ul", {"class":"new_word_list list-group"}).find_all("li", {"class":"list-group-item"})

    file = open(ChptName, 'w', encoding='UTF8', newline='')
    writer = csv.writer(file)

    for li in soup:
        count +=1
        row = []
        front = ""
        back = ""

        wordSoup = li.find("span", {"class":"word"})
        front = wordSoup.text.strip()
        row.append(front)
        
        yomikata = ""
        imiTranslation = ""
        span = li.find_all("button", {"class":"btn btn-xs btn-word"})
        for s in span:
            if s.text.strip() == "読み方":
                yomikata = s.findNext("span").text.strip()
                print(yomikata)
            if s.text.strip() == "意味":
                imiTranslation = s.findNext("span").text.strip().replace("英訳","")
                print(imiTranslation+"\n-------")

        back = yomikata+"\n"+imiTranslation

        #append backside
        row.append(back)

        # write the data
        writer.writerow(row)
    
    print("Wrote "+ChptName+"...\n")
    file.close()

