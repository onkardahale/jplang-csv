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

#finds number of words in a chapter
def findNWMax(NChpt):
    try:
        soup = req_soup(URL+str(NChpt)+"/"+str(NChpt)+".html").find("ul", {"class":"new_word_list list-group"}).find_all("li")
        return len(soup)
    except:
        print("失敗")

#writes csv for chapter
def writeCsv(ChptName, NChpt):

    soup = req_soup(URL+str(NChpt)+"/"+str(NChpt)+".html").find("ul", {"class", "new_word_list list-group"}).find_all("li")
    NWMax = findNWMax(NChpt)

    file = open(ChptName, 'w', encoding='UTF8', newline='')

    writer = csv.writer(file)

    for i in range(NWMax):

        for li in soup:
            row = []
            front = ""
            back = ""
            hasKanji = True

            kanji = li.find("span", {"class": "word"})
            if kanji is not None:
                try:
                    front = front + kanji.text.strip()
                except:
                    front =""
                row.append(front)
            else:
                hasKanji = False

            yomikata = li.find("span",{"class":"word-answer"})
            if hasKanji == False:
                front = front + yomikata.text.strip()
                row.append(front)
            else:
                back = back + word.text.strip() + "\n"

            imi = li.find("span",{"class":"textOverLine"})
            try:
                back = back + imi.text.strip()+"\n"
            except:
                back = back + ""

            #append backside
            row.append(back)

            # write the data
            writer.writerow(row)
            
    print("Wrote "+ChptName+"...\n")
    file.close()

