import os
import re


def loop(path, files_: dict):
    for u in os.listdir(path):
        upath = os.path.join(path, u)
        if os.path.isdir(upath):
            loop(upath, files_)
        else:
            result = re.search('\.([^.]+)$', u)
            if result:
                suffix = result.group(1)
                struct_ = {'name': u, 'path': upath}
                if files_.get(suffix) is None:
                    files_[suffix] = [struct_]
                else:
                    files_[suffix].append(struct_)


def rename_suffix(files_, old, new):
    file2change = files_.get(old)
    if file2change is not None:
        for f in file2change:
            old_path = f['path']
            new_path = f['path'][:-len(old)] + new
            os.rename(old_path, new_path)
            print('\n{} --> {}'.format(old_path, new_path))
            # f['path'] = new_path
        # del files_[old]
        # tar_files = files_.get(new)
        # if tar_files is None:
        #     files_[new] = file2change
        # else:
        #     tar_files.extend(file2change)


target = 'rar'

while True:
    files = {}
    loop('./', files)
    suffixes = list(files.keys())
    for n, s in enumerate(suffixes):
        print(f'{n + 1}. {s}')
    command = input(f'要将哪个后缀修改为目标后缀({target})？按0以退出 ').strip()
    if command == '':
        pass
    else:
        command = int(command)
        if command == 0:
            break
        else:
            suffix2change = suffixes[command - 1]
            a = input(f'要将以 {suffix2change} 为后缀的文件转为以 {target} 为后缀吗？(y/n) ').strip()
            if a == 'y':
                rename_suffix(files, suffix2change, target)
                print('\n成功\n')
