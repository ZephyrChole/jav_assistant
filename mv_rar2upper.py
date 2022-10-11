import os


def loop(path):
    for i in os.listdir(path):
        ipath = os.path.join(path, i)
        if os.path.isdir(ipath):
            loop(ipath)
        elif i[-4:] == '.rar':
            os.rename(ipath, os.path.join(os.path.split(path)[0],i))


if __name__ == '__main__':
    loop('./')
