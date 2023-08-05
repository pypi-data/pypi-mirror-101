import json
import re
import requests
from datetime import datetime

def parse_int(s):
    t=s[:]
    while ord('0')>ord(t[0])or ord('9')<ord(t[0]):
        t=t[1:]
    n=0
    if len(t)==0:
        return None
    while len(t)>0:
        if ord('0')<=ord(t[0])<=ord('9'):
            n=n*10+(ord(t[0])-ord('0'))
            t=t[1:]
        else:
            break
    return n

class PointWeather():
    def __init__(self,time=None,temp=None,feelslike=None,wea=None,weaicon=None,winddir=None,winddeg=None,windscale=None,windspeed=None,humidity=None,vis=None,aqi=None):
        self.time=time
        self.temp=temp
        self.feelslike=feelslike
        self.wea=wea
        self.weaicon=weaicon
        self.winddir=winddir
        self.winddeg=winddeg
        self.windscale=windscale
        self.windspeed=windspeed
        self.humidity=humidity
        self.vis=vis
        self.aqi=aqi

    def get_icon(self):
        return requests.get(self.weaicon).content

    def add(self,pw):
        if not self.time and pw.time:
            self.time=pw.time
        if not self.temp and pw.temp:
            self.temp=pw.temp
        if not self.feelslike and pw.feelslike:
            self.feelslike=pw.feelslike
        if not self.wea and pw.wea:
            self.wea=pw.wea
        if not self.weaicon and pw.weaicon:
            self.weaicon=pw.weaicon
        if not self.winddir and pw.winddir:
            self.winddir=pw.winddir
        if not self.winddeg and pw.winddeg:
            self.winddeg=pw.winddeg
        if not self.windscale and pw.windscale:
            self.windscale=pw.windscale
        if not self.windspeed and pw.windspeed:
            self.windspeed=pw.windspeed
        if not self.humidity and pw.humidity:
            self.humidity=pw.humidity
        if not self.vis and pw.vis:
            self.vis=pw.vis
        if not self.aqi and pw.aqi:
            self.aqi=pw.aqi
    def __str__(self):
        orig='''
Time: {}
Temperature: {}
Feels Like: {}
Weather: {}
Weather Icon URL: {}
Wind Direction: {}
Wind Degrees: {}
Wind Scale: {}
Wind Speed: {}
Humidity: {}
Visible Distance: {}
AQI: {}
'''.strip()
        fmted=orig.format(
            str(self.time),
            self.temp,
            self.feelslike,
            self.wea,
            self.weaicon,
            self.winddir,
            self.winddeg,
            self.windscale,
            self.windspeed,
            self.humidity,
            self.vis,
            self.aqi
        )
        return fmted
    
    def __repr__(self):
        return str(self).replace('\n',' ')+'\n'


def LocateMe_China():
    url='http://myip.ipip.net/json'
    rsp=json.loads(requests.get(url).text)
    return rsp['data']['location'][2]

def LocateMe():
    url='https://api.myip.la/cn?json'
    rsp=json.loads(requests.get(url).text)
    return rsp['location']['city']

def LocateMe_en():
    url='https://api.myip.la/en?json'
    rsp=json.loads(requests.get(url).text)
    return rsp['location']['city']

class QWeatherAPI():
    def __init__(self,key):
        self.key=key
    
    def locate(self,loc):
        url='https://geoapi.qweather.com/v2/city/lookup?location={}&key={}'\
             .format(loc,self.key)
        rsp=json.loads(requests.get(url).text)
        if rsp['code']!='200':
            return ''
        return rsp['location'][0]['id']
    
    def weather(self,cid):
        url='https://devapi.qweather.com/v7/weather/now?location={}&key={}'\
             .format(cid,self.key)
        rsp=json.loads(requests.get(url).text)
        if rsp['code']!='200':
            return PointWeather()
        time=datetime.strptime(rsp['now']['obsTime'][:-6],'%Y-%m-%dT%H:%M')
        temp=parse_int(rsp['now']['temp'])
        feelslike=parse_int(rsp['now']['feelsLike'])
        wea=rsp['now']['text']
        icon_url='https://cdn.jsdelivr.net/gh/qwd/WeatherIcon@master/weather-icon-S1/color-256/{}.png'\
                  .format(rsp['now']['icon'])
        winddir=rsp['now']['windDir']
        winddeg=parse_int(rsp['now']['wind360'])
        windscale=parse_int(rsp['now']['windScale'])
        windspeed=parse_int(rsp['now']['windSpeed'])
        humidity=parse_int(rsp['now']['humidity'])
        vis=parse_int(rsp['now']['humidity'])
        weaobj=PointWeather(time,temp,feelslike,wea,icon_url,winddir,winddeg,windscale,windspeed,humidity,vis)
        return weaobj


class TianqiAPI():
    def __init__(self,appid,appsecret):
        self.appid=appid
        self.appsecret=appsecret
        self.icodic={
            'xue':403,
            'lei':304,
            'shachen':507,
            'wu':501,
            'bingbao':313,
            'yun':103,
            'yu':306,
            'yin':101,
            'qing':100
        }

    def weather(self,cid=None,city=None,ip=None):
        url='https://v0.yiketianqi.com/api?version=v61&appid={}&appsecret={}'\
             .format(self.appid,self.appsecret,cid)
        if cid:
            url+='&cityid={}'.format(cid)
        if city:
            url+='&city={}'.format(city)
        if ip:
            url+='&ip={}'.format(ip)
        rsp=json.loads(requests.get(url).text)
        time='{} {}'.format(rsp['date'],rsp['update_time'])
        time=datetime.strptime(time,'%Y-%m-%d %H:%M')
        temp=parse_int(rsp['tem'])
        feelslike=None
        wea=rsp['wea']
        icon_url='https://cdn.jsdelivr.net/gh/qwd/WeatherIcon@master/weather-icon-S1/color-256/{}.png'\
                  .format(self.icodic[rsp['wea_img']])
        winddir=rsp['win']
        windscale=parse_int(rsp['win_speed'])
        windspeed=parse_int(rsp['win_meter'])
        humidity=parse_int(rsp['humidity'])
        vis=parse_int(rsp['visibility'])
        aqi=parse_int(rsp['air'])
        weaobj=PointWeather(time,temp,None,wea,icon_url,winddir,None,windscale,windspeed,humidity,vis,aqi)
        return weaobj


class SeniverseAPI():
    def __init__(self,key):
        self.key=key

    def weather(self,loc):
        url='https://api.seniverse.com/v3/weather/now.json?key={}&location={}'\
             .format(self.key,loc)
        rsp=json.loads(requests.get(url).text)
        rsp=rsp['results'][0]
        time=datetime.strptime(rsp['last_update'][:-6],'%Y-%m-%dT%H:%M:%S')
        temp=parse_int(rsp['now']['temperature'])
        wea=rsp['now']['text']
        weaobj=PointWeather(time,temp,None,wea)
        return weaobj
        
QWFreeAPI1=QWeatherAPI('0257abdc83864872a566e49e11c85174')
QWFreeAPI2=QWeatherAPI('6478ef7de6e243bba30e49702d56044f')
QWFreeAPI3=QWeatherAPI('fd2f40b2ffb14e03821591fe6f0ed528')
TianqiFreeAPI=TianqiAPI(51122817,'Ss3i8fjK')
SeniverseFreeAPI1=SeniverseAPI('S2wP3OMHRftI4jiuN')
SeniverseFreeAPI2=SeniverseAPI('SKCTDEAwDySL7aos0')
SeniverseFreeAPI3=SeniverseAPI('S6_Zv1FDXzGPj8yjQ')
