import os
import tarfile


class TarGzipArchiver:
    def add_folder(self, directory, folder=""):
        self.sbj.add(directory, folder, recursive=True)

    def __init__(self, path, mod='w:gz'):
        self.sbj = tarfile.open(path, mod)
        self.path = path
        self.mod = mod

    def add(self, src_path, dst_path='./'):
        self.sbj.add(src_path, dst_path)

    def close(self):
        self.sbj.close()
