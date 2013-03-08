#-*-coding:utf-8-*-
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import urllib2
import time
import random
import os
import re
import StringIO

try:
    import Image, ImageDraw, ImageFont
except:
    from PIL import Image, ImageDraw, ImageFont

app_key = "1211807749"#"2864157873"
app_secret = "04871b4d202a401937386465c0325cc4"#"94024d7c968a75f4ea01e4d103a06f9a"
redirect_uri = "https://api.weibo.com/oauth2/default.html"

ACCOUNT = "ashinminisnake@gmail.com"
#ACCOUNT = "416170497@qq.com"
PASSWORD = "230298603777"

def auth():
    url = "https://api.weibo.com/oauth2/authorize"
    auth_url = "%s?client_id=%s&redirect_uri=%s"%(url, app_key, redirect_uri)
    post_data = urllib.urlencode({'client_id':app_key, 'response_type':'code', 'redirect_uri':redirect_uri, 'action':'submit', 'userId':ACCOUNT, 'passwd':PASSWORD, 'isLoginSina':0, 'from':'', 'regCallback':'', 'state':'', 'ticket':'', 'withOfficalFlag':0})
    headers = {'Referer':auth_url,'Content-Type': 'application/x-www-form-urlencoded'}
    r = urllib2.Request(url, post_data, headers)
    r = urllib2.urlopen(r)
    code = r.geturl().split('=')[1]
    return code


def get_token():
    code = auth()
    url = "https://api.weibo.com/oauth2/access_token"
    post_data = urllib.urlencode({ 'client_id':app_key, 'client_secret':app_secret, 'grant_type':'authorization_code', 'code':code, 'redirect_uri':redirect_uri, })
    r = urllib2.Request(url, post_data)
    c = urllib2.urlopen(r).read()
    import json
    data = json.loads(c)
    return data
    

def home(request):
    return HttpResponseRedirect('/static/clock.swf')


def get_time_pic():
    img = Image.new('RGB', (1100, 800))
    draw = ImageDraw.Draw(img)
    the_dir = os.path.dirname(os.path.realpath(__file__))
    font = ImageFont.truetype(os.path.join(the_dir, 'fonts', 'font%s.ttf'%random.randint(1, 15)), 68)
    p = re.compile('\d+:(\d+:\d+)')
    time_str = time.ctime()
    draw.text((35, 345), time_str.replace(re.search(p,time_str).group(1), '00'), font=font)
    font = ImageFont.truetype(os.path.join(the_dir, 'fonts', 'font%s.ttf'%random.randint(1, 15)), 20)
    draw.text((570, 445), "CUIT-CLOCK By Syclover-A'shIn", font=font)
    buf_img = StringIO.StringIO()
    img.save(buf_img, 'png')
    pic = buf_img.getvalue()
    buf_img.close()
    return pic


def start(request):
    os.environ['disable_fetchurl'] = "1"
    data = get_token()      
    word = ['biu! ', 'dang! ', 'pia! ', 'mia~ ', 'do~ ', 'bi! ', 'pa! ', 'bomb! ', 'ka! ', 'da! ']
    mood = ['(°ー°〃)', '(＃°Д°)', '(-ω- )', '(′・ω・`)', '( ^ω^)', '乀(ˉεˉ乀)', '\(╯-╰)/', '\(╯-╰)/', '\(▔▽▔)/', '^(oo)^', '(O^~^O)', '（╯＾╰）', '[呵呵]', '[哈哈]', '[生病]', '[委屈]', '[泪]', '[衰]', '[嘘]', '[悲伤]', '[怒骂]', '[伤心]', '[打哈欠]', '[走你]', '[江南style]', '[不想上班]', '[笑哈哈]', '[得意地笑]', '[泪流满面]', '[纠结]', '[抠鼻屎]', '[求关注]', '[奥特曼]', '[瞧瞧]', '[嘻嘻]', '[可爱]', '[可怜]', '[挖鼻屎]', '[吃惊]', '[害羞]', '[挤眼]', '[闭嘴]', '[鄙视]', '[爱你]', '[偷笑]', '[亲亲]', '[太开心]', '[懒得理你]', '[右哼哼]', '[左哼哼]', '[吐]', '[抱抱]', '[怒]', '[疑问]', '[馋嘴]', '[拜拜]', '[思考]', '[汗]', '[困]', '[睡觉]', '[甩甩手]', '[失望]', '[酷]', '[花心]', '[哼]', '[鼓掌]', '[拍手]', '[抓狂]', '[黑线]', '[阴险]', '[心]', '[偷乐]', '[转发]', '[好爱哦]', '[蜡烛]', '[羞嗒嗒]', '[大南瓜]', '[立志青年]', '[困死了]', '[带感]', '[崩溃]', '[好囧]', '[别烦我]', '[din害羞]', '[din吃]', '[lxhx喵喵]', '[g思考]', '[lm天然呆]', '[bed凌乱]', '[c捂脸]', '[乐乐]', '[ali踩]', '[冒个泡]', '[吵闹]', '[眨眨眼]']

    oclock = int(time_list[0])
    if oclock > 12:
        oclock = oclock - 12
    text = "%s点啦 %s %s"%(oclock, random.choice(mood), random.choice(word)*oclock)

    #url = "https://api.weibo.com/2/statuses/update.json"
    url = "https://upload.api.weibo.com/2/statuses/upload.json"
            
    pic = get_time_pic()

    values = {
                'source':app_key,
                'access_token':data['access_token'],
                'status':text,
                'visible':'0',
                'lat':'30.580466',
                'long':'103.987645',
            }


    boundary = 'cuitclockweibopostdata%s'%(int(time.time()))
    post_data = []
    for k,v in values.iteritems():
        post_data.append('--%s'%boundary)
        post_data.append('Content-Disposition: form-data; name="%s"\r\n'%k)
        post_data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    post_data.append('--%s'%boundary)
    post_data.append('Content-Disposition: form-data; name="pic"; filename="pic.png"')
    post_data.append('Content-Length: %d'%len(pic))
    post_data.append('Content-Type: image/png\r\n')
    post_data.append(pic)
    post_data.append('--%s--\r\n'%boundary)

    data = '\r\n'.join(post_data)
    headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary}
    try:
        r = urllib2.Request(url, data, headers)
        c = urllib2.urlopen(r)
    except Exception,e:
        print e
    return HttpResponse('ok')
