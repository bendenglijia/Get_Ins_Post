# coding:utf-8
import urllib2
import re
import time
import urlparse


promt = raw_input("Please enter the address: > ")
url = promt
o = urlparse.urlparse(url)
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
           'Referer' : 'https://www.instagram.com' + o.path}
video_num = 0
pic_num = 0


def load_page(url, headers):
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    source = response.read()
    return source


def save_pic_and_video(video_num, pic_num):

    for i in range(len(short_code)):
        try:
            url = "https://www.instagram.com/p/" + str(short_code[i]) + "/?taken-by=" + o.path[1:-1]
            print url
            pattern = re.compile('"config_width":750,"config_height":\d+},{"src":"(.*?)","config_width":1080', re.S)
            result = re.findall(pattern, load_page(url, headers))
            pattern_video = re.compile('"video_url":"(.*?)"')
            result_video = re.findall(pattern_video, load_page(url, headers).decode('utf-8'))
            if result_video != []:
                url = result_video[0]
                print result_video[0]
                with open("%s.mp4" % (time.strftime("%H%M%S")), "wb") as f:
                    f.write(load_page(url, headers))
                print "Video saved!"
                video_num += 1
                time.sleep(2)
            if len(result) > 1:
                for i in range(1, len(result)):
                    url = result[i]
                    print result[i]
                    with open("%s.jpg" % (time.strftime("%H%M%S")), "wb") as f:
                        f.write(load_page(url, headers))
                    print "Picture saved!"
                    pic_num += 1
                    time.sleep(1.5)
            else:
                url = result[0]
                print result[0]
                with open("%s.jpg" % (time.strftime("%H%M%S")), "wb") as f:
                    f.write(load_page(url, headers))
                print "Picture saved!"
                pic_num += 1
                time.sleep(1.5)
        except urllib2.HTTPError:
            continue
    return video_num, pic_num


while True:

    pattern = re.compile('"shortcode":"(.*?)"', re.S)
    short_code = re.findall(pattern, load_page(url, headers).decode('utf-8'))

    pattern_end_cursor = re.compile('"end_cursor":"(.*?)"', re.S)
    next_page = re.findall(pattern_end_cursor, load_page(url, headers).decode('utf-8'))

    pattern_id = re.compile('"id":"(\d{8,10})"', re.S)
    result_id = re.findall(pattern_id, load_page(url, headers).decode('utf-8'))

    video_num, pic_num = save_pic_and_video(video_num, pic_num)

    try:
        url = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=%7B%22id%22%3A%22' + result_id[0] + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + next_page[0] + '%22%7D'
        print url
        print "Getting Next Page..."
    except IndexError:
        break
print "All Done bro!!"
print "%d Video has been saved!" % video_num
print "%d Pictures has been saved!" % pic_num















