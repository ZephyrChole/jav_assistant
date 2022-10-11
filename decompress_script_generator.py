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

def load_blogs(pickle_dir_path):
    blogs = []
    for name in glob.glob(os.path.join(pickle_dir_path, 'blogs*.pickle')):
        f = open(name, 'rb')
        blogs.extend(pickle.load(f))
        f.close()
    blogs = list(filter(lambda x: x.get('name'), blogs))
    return blogs


def test_pwd4archive(pwd,archive_path):
    a = sp.run(['7z','t',f'-p{pwd}',archive_path))
    return a.returncode == 0


def bruce_force_pwd(path):
    for blog in BLOGS:
        pwd = blog.get('pwd')
        if test_pwd4archive(pwd,path):
            return pwd
    return None

def lookup_pwd(n):
    for blog in BLOGS:
        if n in blog.get('name'):
            return blog.get('pwd')


def generate_decompress_command_line(current_path, name,files):  # , is_slice=False):
    pwd = lookup_pwd(os.path.split(current_path)[1])
    archive_path = os.path.join(currrent_path,name)
    if pwd is None:
        a = input('cannot lookup password,try bruce force? It may take a while.(y/n)')
        if a.strip() == 'y':
            pwd = bruce_force_pwd(archive_path)
            if pwd is None:
                pwd = input('查询不到密码，请手动输入：').strip()
        else:
            return None
    command='7z x "{}" -p"{}" -o"{}" -y'.format(archive_path, pwd, current_path)
    if len(files)>0:
        command +=' && '
    rm_sh = list(map(lambda x:"{} '{}'".format("rm" if platform.system() == 'Linux' else 'Windows',os.path.join(current_path,x)),files))
    command+=' && '.join(rm_sh)
    return command


def write_in(s):
    if platform.system() == 'Linux':
        with open('decompress.bat', 'a') as file:
            file.write(s + '\n')
    else:
        with open('decompress.sh', 'a') as file:
            file.write(s + '\n')
    print('成功写入！')

def input_num_switch(input_num,current_path,name2sequence,dir_l,name_l,single_whole_l):
    if input_num == 1:
        current_path = os.path.split(current_path)[0]
    elif len(dir_l) + 1 <= input_num <= len(dir_l) + len(name_l):
        input_num = input_num - len(dir_l) - 1
        files=name2sequence.get(name_l[input_num]).values()
        name = name_l[input_num] + '.part*.rar'
    elif len(dir_l) + 1 + len(name_l) <= input_num <= len(dir_l) + len(name_l) + len(single_whole_l):
        input_num = input_num - len(name_l) - len(dir_l) - 1
        name = single_whole_l[input_num]
        files = [name]
    else:
        raise ValueError(f'input_num:{inpuut_num}number out of range')
    return current_path,name,files



def main():
    # root_path = './'
    current_path = './'
    global BLOGS
    BLOGS = load_blogs(os.path.join(sys.path[0], 'aww_history'))
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

        a = input('#')
        print('\n')
        try:
            a = a.strip()
            if a == 'a':
                for a in range(len(dir_l) + 1, len(dir_l) + len(name_l) + len(single_whole_l) + 1):
                    current_path,name,files = input_num_switch(a,current_path,name2sequence,dir_l,name_l,single_whole_l)
                    s = generate_decompress_command_line(current_path, name,files)
                    if s is not None:
                        write_in(s)
            elif a == 'e':
                break
            else:
                a = int(a)
                current_path,name,files = input_num_switch(a,current_path,name2sequence,dir_l,name_l,single_whole_l)
                s = generate_decompress_command_line(current_path, name,files)
                if s is not None:
                    write_in(s)
        except ValueError as e:
            print(e)
            input('need a number,try again')


if __name__ == '__main__':
    main()
