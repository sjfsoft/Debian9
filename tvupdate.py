#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
import requests, json, sys, re, time, base64, random

jsonfile = r'/var/www/tv.sjfvip.tk/tvjson/tvdata.json'
userdir = r'/var/www/html/tvjson/'
logfile = r'/var/log/tv.log'
user = ['shenjunfeng']
#user = ['shenjunfeng', 'shenyulan']

chrome_path = r'/root/browsermob/bin/chromedriver'
server = Server(r'/root/browsermob/bin/browsermob-proxy')

num = 1

def load_tvch():
    """清空日志并读取源频道JSON文件"""
    with open(logfile, 'wt', encoding='utf-8') as f:
        f.write(r'')
    with open(jsonfile, 'rt', encoding='utf-8') as f:
        return json.load(f)


def save_tvch():
    """保存频道JSON文件"""
    for name in user:
        file = userdir + name + ".json"
        with open(file, 'wt', encoding='utf-8') as f:
            json.dump(channel_data, f, ensure_ascii=False, indent=2)
        print("成功写入频道文件=======================》【%s】" % (file))


def tv_update(url):
    """更新频道视频链接"""
    global num
    channel_data['live'][key]['num'] = str(num).zfill(3)
    channel_data['live'][key]['urllist'] = url
    num = num + 1
    channel_data['live'][key]['error'] = '0'
    print('%s  %s频道成功更新========> 【%s】' % (run_time, tv_net, room_id))

def tv_error():
    """更新频道错误码"""
    channel_data['live'][key]['error'] = '1'
    print('%s  %s频道或房间错误------> 《%s》' % (run_time, tv_net, room_id))


def delete_error():
    """删除未开播频道"""
    for key in range(2000,-1,-1):
        try:
            error = channel_data['live'][key]['error']
            room_id = channel_data['live'][key]['roomid']
            del channel_data['live'][key]
            print('%s  删除频道==========>【%s】' % (run_time, room_id))
        except Exception:
            continue


def channel_update(tv_net, room_id):
    if tv_net == '哔哩TV':
        api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={}'.format(room_id)
        try:
            api_json = json.loads(requests.get(api_url, timeout=5).text)
            if api_json['data']['live_status'] == 1:
                url = 'http://192.168.192.168/bilibili.php?channel=' + room_id + '&chs=-0'
                url += '#' + 'http://192.168.192.168/bilibili.php?channel=' + room_id + '&chs=-1'
                url += '#' + 'http://192.168.192.168/bilibili.php?channel=' + room_id + '&chs=-2'
                url += '#' + 'http://192.168.192.168/bilibili.php?channel=' + room_id + '&chs=-3'
                tv_update(url)
            else:
                tv_error()
        except Exception:
            tv_error()
    elif tv_net == '斗鱼TV':
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
        room_url = 'https://www.douyu.com/{}'.format(room_id)
        proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
        driver.get(room_url)
        time.sleep(1)
        try:
            video_id = re.search('"rtmp_live":"(.+?)\.', str(proxy.har)).group(1)
            url = 'http://tx2play1.douyucdn.cn/live/' + video_id + '.xs?uuid='
            tv_update(url)
            driver.quit()
        except Exception:
            tv_error()
            driver.quit()
    elif tv_net == '虎牙TV':
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        room_url = 'http://www.huya.com/{}/'.format(room_id)
        try:
            html = requests.get(room_url, headers=headers, timeout=5)
            html = html.content.decode()
            html = re.search('"stream": ({.+?})\s*};', html).group(1)
            html_json = json.loads(html)
            api_list = html_json['data'][0]['gameStreamInfoList']
            urls = ''
            for item in api_list:
                urls += item['sHlsUrl'] + '/' + item['sStreamName'] + '.' + item['sHlsUrlSuffix'] + '#'
            url = re.search('(http://al.*?).m3u8', urls).group(0)
            if re.search('(http://tx.*?).m3u8', urls) != None:
                url += '#' + re.search('(http://tx.*?).m3u8', urls).group(0)
                if re.search('(http://ws.*?).m3u8', urls) != None:
                    url += '#' + re.search('(http://ws.*?).m3u8', urls).group(0)
            tv_update(url)
        except Exception:
            tv_error()



if __name__ == '__main__':
    channel_data = load_tvch()
    server.start()
    proxy = server.create_proxy()
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--no-sandbox')
    for key, data in enumerate(channel_data['live']):
        sys.stdout.flush()
        run_time = time.strftime('%H:%M:%S', time.localtime())
        try:
            room_id = data['roomid']
            tv_net = data['info']
            channel_update(tv_net, room_id)
            errors = channel_data['live'][key]['error']
            if data['error'] == '0':
                del channel_data['live'][key]['info']
                del channel_data['live'][key]['roomid']
                del channel_data['live'][key]['error']
            else:
                continue
        except:
            channel_data['live'][key]['num'] = str(num).zfill(3)
            num = num + 1
    delete_error()
    save_tvch()

