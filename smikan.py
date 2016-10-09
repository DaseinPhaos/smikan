"""
    ##Introduction
    **smikan**, a simple module grabbing bangumi information from http://mikanani.me
    The API is kindof messing for the time being but using it is quiet simple.
    --------
    ##Example
    ```python
    import smikan

    # Starting from a homepage
    homepage = smikan.get_homepage()

    # Finding bangumis by broadcasting date
    print(hp.fri)

    # Grabing details from a particular bangumi
    bangumi = hp.fri[0]
    bangumi.get()
    print(bangumi.subtitles)
    
    # Check which season the homepage is currently in
    print(homepage.period)

    # Navigate to another season
    homepage.change_period(homepage.periods[1])
    print(homepage.fri)
    ```
    --------
    ##License

    This module is distributed under the MIT license (https://opensource.org/licenses/MIT).

    Copyright (c) 2016 Dasein Phaos

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


from bs4 import BeautifulSoup
import datetime
import requests

_mikan_url = "http://mikanani.me"
_post_url = "http://mikanani.me/Home/BangumiCoverFlowByDayOfWeek"
_base_headers = {
     'Host': 'mikanani.me',
     'Connection': 'keep-alive',
     'Accept-Encoding': 'gzip, deflate',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
     'Cookie': '__cfduid=de118d7462a8fe4b0a72c074e4165e2401473314399; mikan-announcement=3',
     'Accept': '*/*',
     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
}
_get_headers = {'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
_post_headers = {'Origin': 'http://mikanani.me', 
'Content-Length': '31', 
'Referer': 'http://mikanani.me/', 
'X-Requested-With': 'XMLHttpRequest', 
'Content-Type': 'application/json; charset=UTF-8'}
_post_params = {"httpVersion": "HTTP/1.1", "queryString": [], "headersSize": 569, "bodySize": 29}


_session = requests.Session()
_session.headers.update(_base_headers)

def _get_post_data(period):
    splitted = period.split()
    assert(len(splitted) == 2)
    return {"year":int(splitted[0]),"seasonStr":splitted[1][0]}

def start_session():
    """
        Prepare to start a new connection session with http://mikanani.me
    """
    global _session
    _session = requests.Session()
    _session.headers.update(_base_headers)
    
def close_session():
    """
        Close the current connection session with http://mikanani.me
    """
    global _session
    _session.close()

def restart_session():
    """
        Close and prepare to restart the connection session with http://mikanani.me
    """
    close_session()
    start_session()


class EpResource:
"""
    A self-explainable episode resource item.
"""
    def __init__(self, name:str, info_url: str, size:float, update_time: datetime.datetime, magnet_link:str, torrent_link:str):
        self.name = name
        self.info_url = info_url
        self.size = size
        self.update_time = update_time
        self.magnet_link = magnet_link
        self.torrent_link = torrent_link

    def __repr__(self):
        return "[Title: \"{0}\", size: {1}MB]".format(self.name, self.size)

class Bangumi:
"""
    A self-explainable bangumi item.
"""
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
    """
        Save details to data members using soup constructing from the bangumi's html-page.
    """
        leftbar = bsoup.find("div", "pull-left leftbar-container")
        poster_rurl = leftbar.find("div", "bangumi-poster")["style"]
        poster_rurl = poster_rurl[(poster_rurl.find("'")+1): poster_rurl.rfind("'")]
        self.poster_url = _mikan_url + poster_rurl
        self.name = leftbar.find("p", "bangumi-title").contents[0].strip()
        infos = leftbar.find_all("p", "bangumi-info")
        for info in infos:
            info_str = ""
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

    def get(self, timeout = 10):
    """
        Save details to data members via information fetched from self.url

        `timeout`: the longest time to wait for responce from mikanani.me before
            raising a `requests.exceptions.ConnectTimeout`  
    """
        # r = requests.get(self.url, timeout = timeout)
        r = _session.get(_mikan_url, headers = _base_headers, timeout = timeout)
        if r.status_code != 200: r.raise_for_status_code()
        soup = BeautifulSoup(r.content, "html.parser")
        self.feed(soup)


class HomePage:
"""
    Analog to mikanani's homepage.
"""
    def __init__(self):
        self.periods = []
        self.period = ""
        self._reset_bangumi_data()

    def _reset_bangumi_data(self):
        self.mon = []
        self.tue = []
        self.wed = []
        self.thu = []
        self.fri = []
        self.sat = []
        self.sun = []

    def _find_target(self, weekday:str):
        if weekday == "星期一": return self.mon
        if weekday == "星期二": return self.tue
        if weekday == "星期三": return self.wed
        if weekday == "星期四": return self.thu
        if weekday == "星期五": return self.fri
        if weekday == "星期六": return self.sat
        if weekday == "星期日": return self.sun
        raise ValueError() 

    def feed_p(self, soup:BeautifulSoup):
    """
        Initialize bangumi-data contents using `soup`, which should be constructed
        from a .html containing valid infos. e.g. mikanani's homepage. 
    """
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
                bangumi = None
                if len(update_time[0]) == 4:
                    bangumi = Bangumi(a_tag['title'], datetime.date(int(update_time[0]), int(update_time[1]), int(update_time[2])), _mikan_url + a_tag['href'])
                else:
                    bangumi = Bangumi(a_tag['title'], datetime.date(int(update_time[2]), int(update_time[0]), int(update_time[1])), _mikan_url + a_tag['href'])
                target.append(bangumi)
    
    def feed(self, soup:BeautifulSoup):
    """
        Initialize data menbers using `soup`, which should be constructed
        from a .html containing valid infos. e.g. mikanani's homepage. 
    """
        psoup = soup.find("li", "sk-col dropdown date-btn")
        self.period = psoup.find_next("div", "sk-col date-text").contents[0].strip()
        periods = psoup.find_all(lambda tag: tag.name == "a" and tag.has_attr("data-season"))
        for p in periods:
            self.periods.append("{0} {1}".format(p["data-year"], p.contents[0].strip()))
        self._reset_bangumi_data()
        self.feed_p(soup)

    def change_period(self, period):
    """
        Change the bangumi-data members according to the new season period specified. 
    """
        global _session
        post_data = _get_post_data(period)
        r = _session.post(_post_url, json=post_data, headers = _post_headers)
        if r.status_code != 200: r.raise_for_status_code()
        soup = BeautifulSoup(r.content, "html.parser")
        self.feed_p(soup)    


def get_homepage(timeout = 10):
"""
    Return a new `HomePage` containing infos fetched from mikanani.me.

    `timeout`: the longest time to wait for responce from mikanani.me before
        raising a `requests.exceptions.ConnectTimeout`  
"""
    r = _session.get(_mikan_url, timeout = timeout, headers = _get_headers)
    #r = requests.get(_mikan_url, timeout = timeout)
    if r.status_code != 200: r.raise_for_status_code()
    hp = HomePage()
    soup = BeautifulSoup(r.content, "html.parser")
    hp.feed(soup)
    return hp