import os
import re
import sys
import glob
import pickle
import platform


def get_decompressible_combs(files):
    files = list(filter(lambda x: x[-4:] == '.rar', files))
    name2sequence = {}
    type2container = {'single_whole': [], 'slices': name2sequence}
    for f in files:
        res = re.match('(^[^.]+)\.part(\d)\.rar$', f)
        if res:
            name = res.group(1)
            index = int(res.group(2))
            if type2container['slices'].get(name) is None:
                index2file = {}
                type2container['slices'][name] = index2file
            type2container['slices'][name][index] = f
        else:
            type2container['single_whole'].append(f)
    return type2container


def check_complete(indexes):
    target_num = len(indexes)
    start_num = 1
    count = 0
    while True:
        if start_num in indexes:
            start_num += 1
            count += 1
        else:
            break
    return target_num == count


def get_pwd(n):
    blogs = []
    print(sys.path[0])
    for name in glob.glob(os.path.join(sys.path[0], 'aww_blog_history/blogs*.pickle')):
        f = open(name, 'rb')
        blogs.extend(pickle.load(f))
        f.close()

    blogs = list(filter(lambda x: x.get('name'), blogs))
    for blog in blogs:
        if n in blog.get('name'):
            return blog.get('pwd')


def generate_decompress_command_line(current_path, name):  # , is_slice=False):
    pwd = get_pwd(name)
    if pwd is None:
        pwd = get_pwd(os.path.split(current_path)[1])
        if pwd is None:
            pwd = input('查询不到密码，请手动输入：').strip()
    return '7z x "{}" -p"{}" -o"{}" && {} "{}"'.format(os.path.join(current_path, name), pwd, current_path,
                                                       "rm" if platform.system() == 'Linux' else 'Windows',
                                                       os.path.join(current_path, name))


def write_in(s):
    with open('decompress.bat', 'a') as file:
        file.write(s + '\n')
    print('成功写入！')


def main():
    # root_path = './'
    current_path = './'

    while True:
        print('当前路径：' + current_path)
        file_l = list(filter(lambda x: os.path.isfile(os.path.join(current_path, x)), os.listdir(current_path)))
        dir_l = list(filter(lambda x: os.path.isdir(os.path.join(current_path, x)), os.listdir(current_path)))
        dir_l.insert(0, '..')

        count = 1

        for dir_ in dir_l:
            print(f'{count} {dir_}/')
            count += 1

        type2container = get_decompressible_combs(file_l)
        print('可供解压的压缩包: 切片组合:{} 单个:{}'.format(len(type2container.get('slices').keys()),
                                                             len(type2container.get('single_whole'))))
        name2sequence = type2container.get('slices')
        name_l = list(name2sequence.keys())
        for name in name_l:
            index2file = name2sequence.get(name)
            print('{}. #{} {}'.format(count, 'complete' if check_complete(index2file.keys()) else 'broken',
                                      ' '.join(index2file.values())))
            count += 1

        single_whole_l = type2container.get('single_whole')
        for name in single_whole_l:
            print(f'{count}. {name}')
            count += 1

        a = input('')
        print('\n')
        try:
            a = a.strip()
            if a == 'a':
                for a in range(len(dir_l) + 1, len(dir_l) + len(name_l) + len(single_whole_l) + 1):
                    if len(dir_l) + 1 <= a <= len(dir_l) + len(name_l):
                        a = a - len(dir_l) - 1
                        name = name_l[a] + '.part*.rar'
                    elif len(dir_l) + 1 + len(name_l) <= a <= len(dir_l) + len(name_l) + len(single_whole_l):
                        a = a - len(name_l) - len(dir_l) - 1
                        name = single_whole_l[a]
                    else:
                        print(a)
                        raise ValueError('number out of range')
                    s = generate_decompress_command_line(current_path, name)  # , is_slice)
                    write_in(s)
            elif a == 'e':
                break
            else:
                a = int(a)
                # is_slice = False
                if a == 1:
                    current_path = os.path.split(current_path)[0]
                elif 2 <= a <= len(dir_l):
                    a = a - 1
                    current_path = os.path.join(current_path, dir_l[a])
                else:
                    if len(dir_l) + 1 <= a <= len(dir_l) + len(name_l):
                        a = a - len(dir_l) - 1
                        name = name_l[a] + '.part*.rar'
                    elif len(dir_l) + 1 + len(name_l) <= a <= len(dir_l) + len(name_l) + len(single_whole_l):
                        a = a - len(name_l) - len(dir_l) - 1
                        name = single_whole_l[a]
                    else:
                        raise ValueError('number out of range')
                    s = generate_decompress_command_line(current_path, name)  # , is_slice)
                    write_in(s)
        except ValueError as e:
            print(e)
            input('need a number,try again')


if __name__ == '__main__':
    main()
