import tarfile


class TarGzipArchiver:
    def add_folder(self, directory, folder=""):
        if not self.sbj:
            self.sbj = tarfile.open(self.path, self.mod)
        self.sbj.add(directory, folder, recursive=True)

    def __init__(self, path, mod='w:gz'):
        self.sbj = None
        self.path = path
        self.mod = mod

    def add(self, src_path, dst_path='./'):
        if not self.sbj:
            self.sbj = tarfile.open(self.path, self.mod)
        self.sbj.add(src_path, dst_path)

    def close(self):
        if self.sbj:
            self.sbj.close()
