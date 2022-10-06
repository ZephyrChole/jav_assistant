import glob
import pickle

blogs = []
for name in glob.glob('./aww_blog_history/blogs*.pickle'):
    f = open(name, 'rb')
    blogs.extend(pickle.load(f))
    f.close()

blogs = list(filter(lambda x: x.get('name'), blogs))

while True:
    a = input('name: ').strip()
    for blog in blogs:
        if a in blog.get('name'):
            print(f"\t名称：{blog.get('name')}\n\t密码：{blog.get('pwd')}\n\t网址：{blog.get('url')}\n")
