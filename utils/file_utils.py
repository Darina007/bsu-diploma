import os
import shutil


def get_filepath(path):
    return path.rsplit('/', 1)[0]


def is_dir_exist(path):
    return os.path.exists(path)

def create_dir(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

def mkdir_if_not_exist(path):
    if is_dir_exist(path):
        return
    create_dir(path)

def dir_is_empty(path):
    return not os.listdir(path)


def clear_if_exist(path):
    if not is_dir_exist(path):
        return
    if dir_is_empty(path):
        return
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
