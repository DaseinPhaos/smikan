from bs4 import BeautifulSoup
import datetime
import requests

_mikan_url = "http://mikanani.me"

class EpResource:
    def __init__(self, name:str, info_url: str, size:float, update_time: datetime.datetime, magnet_link:str, torrent_link:str):
        self.name = name
        self.info_url = info_url
        self.size = size
        self.update_time = update_time
        self.magnet_link = magnet_link
        self.torrent_link = torrent_link

    def __repr__(self):
        return "[\"Title: {0}\", size: {1}MB]".format(self.name, self.size)

class Bangumi:
    def __init__(self, name:str, update_time:datetime.date, url: str):
        self.name = name
        self.update_time = update_time
        self.url = url
        self.intro = None
        self.info = {}
        self.subtitles = {}

    def __repr__(self):
        return "\n[Title: {0}\n Descrption: {1}]\n".format(self.name, self.intro)

    def feed(self, bsoup:BeautifulSoup):
        leftbar = bsoup.find("div", "pull-left leftbar-container")
        poster_rurl = leftbar.find("div", "bangumi-poster")["style"]
        poster_rurl = poster_rurl[(poster_rurl.find("'")+1): poster_rurl.rfind("'")]
        self.poster_url = _mikan_url + poster_rurl
        self.name = leftbar.find("p", "bangumi-title").contents[0].strip()
        infos = leftbar.find_all("p", "bangumi-info")
        for info in infos:
            # info_str = info.string
            # if info_str == None or info_str == "":
            #     info_str = ""
            #     for s in info.strings:
            #         info_str = info_str + s.strip()
            info_str = ""
            # try:
            #     for s in info.strings:
            #         info_str = info_str + s.strip()
            # except StopIteration as identifier:
            #     pass
            for s in info.strings:
                info_str = info_str + s.strip()
            splitted = info_str.split("：", 1)
            if len(splitted) == 2: self.info[splitted[0]] = splitted[1]
        intro_tag = bsoup.find("p", "header2-desc") 
        self.intro = intro_tag.string.strip()
        sgt_tag = intro_tag.find_next("div", "subgroup-text")
        while sgt_tag != None:
            sgt = sgt_tag.contents[0].strip()
            last_tag = sgt_tag
            self.subtitles[sgt] = []
            sgtl = self.subtitles[sgt]
            trs = sgt_tag.find_next("tbody").find_all("tr")
            for tr in trs:
                last_tag = tr.find_next("a")
                rinfo_url = _mikan_url + last_tag["href"]
                rname = last_tag.string.strip()
                last_tag = last_tag.find_next("a")
                rmagnet = last_tag["data-clipboard-text"]
                last_tag = last_tag.find_next("td")
                rsize = float(last_tag.string.strip()[:-2])
                last_tag = last_tag.find_next("td")
                dts = last_tag.string.strip().split(" ")
                ds = dts[0].split("/")
                ts = dts[1].split(":")
                rdt = datetime.datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]))
                last_tag = last_tag.find_next("a")
                rtorrent = _mikan_url + last_tag["href"]
                sgtl.append(EpResource(rname, rinfo_url, rsize, rdt, rmagnet, rtorrent))
            sgt_tag = last_tag.find_next("div", "subgroup-text")

    def get_content(self, timeout = 10):
        r = requests.get(self.url, timeout = timeout)
        if r.status_code != 200: r.raise_for_status_code()
        soup = BeautifulSoup(r.content, "html.parser")
        self.feed(soup)


class HomePage:
    def __init__(self):
        self.mon = []
        self.tue = []
        self.wed = []
        self.thu = []
        self.fri = []
        self.sat = []
        self.sun = []
        self.periods = []
        self.period = ""

    def find_target(self, weekday:str):
        if weekday == "星期一": return self.mon
        if weekday == "星期二": return self.tue
        if weekday == "星期三": return self.wed
        if weekday == "星期四": return self.thu
        if weekday == "星期五": return self.fri
        if weekday == "星期六": return self.sat
        if weekday == "星期日": return self.sun
        raise ValueError() 

    def feed(self, soup:BeautifulSoup):
        psoup = soup.find("li", "sk-col dropdown date-btn")
        self.period = psoup.find_next("div", "sk-col date-text").contents[0].strip()
        periods = psoup.find_all(lambda tag: tag.name == "a" and tag.has_attr("data-season"))
        for p in periods:
            self.periods.append("{0} {1}".format(p["data-year"], p.contents[0].strip()))
        subsoups = soup.find_all("div", "sk-bangumi")
        for subsoup in subsoups:
            weekday = subsoup.find_next("div", "row").contents[0].strip()
            target = None
            if weekday == "星期一": target =  self.mon
            elif weekday == "星期二": target =  self.tue
            elif weekday == "星期三": target =  self.wed
            elif weekday == "星期四": target =  self.thu
            elif weekday == "星期五": target =  self.fri
            elif weekday == "星期六": target =  self.sat
            elif weekday == "星期日": target =  self.sun
            bangumis = subsoup.find_all("div", "an-info")
            for bangumi_tag in bangumis:
                update_time = bangumi_tag.find("div", "date-text").string.strip().split(" ")[0].split("/")
                a_tag = bangumi_tag.find(lambda tag: tag.name == "a" and tag.has_attr("title"))
                bangumi = Bangumi(a_tag['title'], datetime.date(int(update_time[2]), int(update_time[0]), int(update_time[1])), _mikan_url + a_tag['href'])
                target.append(bangumi)


def get_homepage(timeout = 10):
    r = requests.get(_mikan_url, timeout = timeout)
    if r.status_code != 200: r.raise_for_status_code()
    hp = HomePage()
    soup = BeautifulSoup(r.content, "html.parser")
    hp.feed(soup)
    return hp