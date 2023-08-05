import os

class a():
    def __init__(self):
        pass
    def file_exists(self,path):
        if not os.path.exists(path):
            return True
        else:
            return False

    def file_remove(self,path):
        os.remove(path)

    def create_folder(self,path):
        os.mkdir(path)

    def path_get_file_name(self,path):
        return path.split('\\')[-1]

    def file_name_get_suffix_name(self,fill_name):
        return fill_name.split('.')[-1]