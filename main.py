# 爬取必应壁纸
import os
import re
import requests
import sys


def get_one_page(url):  # 解析给定url的网页源代码
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.181 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  # 状态码200说明返回状态正确，状态码是404,403等其他代号则说明网页请求失败
        return response.text
    return None


def download(url, filename):  # 下载图片到本地文件夹
    filepath = filename + '.jpg'  # 这里的路径可以更改自己的文件夹
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.181 Safari/537.36'
    }
    if os.path.exists(filepath):  # 判断图片路径是否已经存在，如果存在就不保存了
        print("文件已经存在了，跳过: %s" % filepath)
        return
    with open(filepath, 'wb') as f:  # 把图片以二进制形式写入到本地
        response = requests.get(url, headers=headers)
        f.write(response.content)
        f.flush()
    # 如果文件的大小为0，说明写入失败，删除
    if os.path.getsize(filepath) == 0:
        os.remove(filepath)


def parse(save_dir, html):  # 解析网页源代码
    pattern = re.compile('data-progressive="(.*?)".*?<h3>(.*?)</h3>')  # 正则表达式筛选html
    items = re.findall(pattern, html)
    for item in items:
        try:
            # url = re.sub(r'(_\d{2,3}x\d{2,3})', "_1920x1080", item[0]) # 2k图片
            url = re.sub(r'(_\d{2,3}x\d{2,3})', "_UHD", item[0])  # 4k图片
            print(url)
            imagename = item[1].strip()
            rule = re.compile(r'[a-zA-z1-9()-/]')  # []用来表示一组字符【abc】匹配a,b,或c
            imagename = rule.sub('', imagename)
            download(url, save_dir + imagename.replace("©", "").strip())
            print(imagename, "正在下载")
        except Exception:
            continue


if __name__ == '__main__':
    if len(sys.argv) == 1 :
        print("存储路径设置错误，示例： \"python main.py save_dir pages\"")
        sys.exit(-1)
    
    page = 10
    
    if len(sys.argv) == 3 :
        page = int(sys.argv[2])
    
    save_dir = sys.argv[1] # "/Users/sam/Pictures/壁纸/bing/"
    r = save_dir[len(save_dir)-1] 
    if r != "/" and r != "\\" :
        save_dir += "/"
    print("存储位置：%s, 下载页数: %d" % (save_dir, page))

    for page in range(1, 10):  # 爬取页面的范围，可以随意更改
        try:
            url = 'https://bing.ioliu.cn/?p=' + str(page)
            print("正在抓取第", page, "页", url)
            html = get_one_page(url)
            parse(save_dir, html)
        except Exception:
            continue
