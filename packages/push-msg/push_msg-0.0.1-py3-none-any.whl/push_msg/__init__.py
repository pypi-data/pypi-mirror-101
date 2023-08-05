__name__ = "push_msg"
__version__ = "1.0"
__description__ = "Push message to wechat for personal usage."
__keywords__ = "Push Message"
__author__ = "oliverxu"
__contact__ = "273601727@qq.com"
__url__ = "https://blog.oliverxu.cn"
__license__ = "MIT"

import urllib.request
import urllib.parse

url = 'https://push.oliverxu.cn/work.php?msg='

def pushmsg(title: str, msg: list):
    global url
    output_msg = ''
    msg_div = '<div class="gray">{}</div>'
    for i in msg:
        output_msg += msg_div.format(i)
    url += urllib.parse.quote(output_msg)
    url += "&title="
    url += urllib.parse.quote(title)
    #print(output_msg)
    #print(url)
    urllib.request.urlopen(url=url)
    #urllib.request.urlopen(url=urllib.parse.quote(url))

if __name__=='__main__':
    pushmsg(title='程序测试', msg=['可以卖的：', '008888', '002736', '008943'])


