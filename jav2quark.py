import glob
import os.path
import pickle
import re
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm
from utils import get_browser


def get_blog_urls():
    br.get('https://www.javbus.com/forum/home.php?mod=space&uid=440145&do=thread&view=me&order=dateline&from=space&page=1')
    br.implicitly_wait(10)
    # input('enter blog resemble url\n')
    urls = []
    i = 2
    while True:
        try:
            urls.append(br.find_by_css(f'tr:nth-child({i}) th a').get_attribute('href'))
            i += 1
        except Exception as e:
            print(e)
            break
    return urls


def get_quark_and_pwd():
    s = br.find_by_css('td.t_f').get_attribute('textContent')
    #print([s])
    a = []
    a.append(re.search('资源(连|链)接:(.+)\n', s).group(2).strip())
    a.append(re.search('解压密码:(.+)\n', s).group(1).strip())
    return a


def load():
    blogs = []
    for name in glob.glob('./aww_blog_history/blogs*.pickle'):
        f = open(name, 'rb')
        blogs.extend(pickle.load(f))
        f.close()

    blogs = list(filter(lambda x: x.get('name'), blogs))
    return blogs


br = get_browser(minimize_on_start=True, proxy='http://127.0.0.1:9910',load_main_config=True)
br.find_by_css = lambda css: br.find_element(By.CSS_SELECTOR, css)

# input('turn on proxy\n')
br.get('https://javbus.com/forum')
# input('login\n')
remain_blogs = load()
# remain_blog_urls = [i.get('url') for i in remain_blogs]
remain_blog_urls = {i.get('url'): True for i in remain_blogs}
blog_urls = get_blog_urls()
blog_urls = list(filter(lambda x: not remain_blog_urls.get(x), blog_urls))
blogs = [{'url': url} for url in blog_urls]
for blog in tqdm(blogs):
    try:
        #input('any key to continue')
        br.get(blog['url'])
        #br.implicitly_wait(10)
        time.sleep(20)
        quark, pwd = get_quark_and_pwd()
        print(quark, pwd)
        blog['quark_url'], blog['pwd'] = quark, pwd
    except Exception as e:
        print(e)

temp_blogs = list(filter(lambda x: x.get('quark_url') is None, blogs))
for blog in tqdm(temp_blogs):
    try:
        br.get(blog['url'])
        print(blog['url'])
        time.sleep(10)
        quark, pwd = get_quark_and_pwd()
        print(quark, pwd)
        blog['quark_url'], blog['pwd'] = quark, pwd
        blog['is_quark_added'] = False
    except Exception as e:
        print(e)
temp_blogs = list(filter(lambda x: x.get('quark_url') is None, blogs))
print(len(blogs), ' found', len(temp_blogs), 'not analysed')

# input('turn off proxy\n')
br.get('https://pan.quark.cn/')
# input('login\n')
for blog in tqdm(blogs):
    if blog.get('is_quark_added') is True:
        continue
    try:
        br.get(blog['quark_url'])
        time.sleep(3)
        name = br.find_by_css('span.file-tit').text
        blog['name'] = name
        br.find_by_css('div.file-info_r').click()
        time.sleep(3)
        br.find_by_css('button.ant-btn.btn-file.btn-file-primary.ant-btn-primary').click()
        blog['is_quark_added'] = True
        time.sleep(3)
    except Exception as e:
        print(e)
        input([blog['url'], blog['quark_url']])

br.quit()
if len(blogs):
    count = 1
    while os.path.exists(f'./aww_blog_history/blogs{count}.pickle'):
        count += 1
    f = open(f'./aww_blog_history/blogs{count}.pickle', 'wb')
    pickle.dump(blogs, f)
    f.close()
