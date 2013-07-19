import os
import json
import subprocess
import glob
from tempfile import NamedTemporaryFile
from ..archiver.tgzarchiver import TarGzipArchiver
from .generic_exporter import GenericExporter
from ..package.package_config import PackageConfig


class StatementSplitter:
    parts = {
        ("main", None),
        ("input", "\\InputFile"),
        ("output", "\\OutputFile"),
        ("notes", "\\Note"),
    }

    def __init__(self, filename):
        self.filename = filename

    def split(self):
        self.files = {file: NamedTemporaryFile(delete=False) for file, tex_command in self.parts}
        content = {file: file == "main" for file, tex_command in self.parts}
        current = "main"
        for line in open(self.filename, "r"):
            part = [part for part in self.parts if line.strip() == part[1]]
            if len(part):
                current = part[0][0]
            else:
                content[current] = True
                self.files[current].write(bytes(line, 'utf-8'))
        for filename, file in self.files.items():
            file.close()
            if not content[filename]:
                os.unlink(file.name)
        return self.files


class AutomationExporter(GenericExporter):
    def __init__(self, network={}, libs=[], problems=[]):
        self.archiver = TarGzipArchiver('please.tar.gz')
        self.network = network
        self.problems = problems
        self.libs = libs
        super(AutomationExporter, self).__init__(self.archiver, None, libs, problems)

    def set_problems(self, problems):
        self.problems = problems

    def set_contest_id(self, contest_id):
        self.contest_id = contest_id

    def create_archive(self):
        if len(self.problems) != 1:
            raise ValueError("For exporting to automation there must be only one task per contest")
        problem = self.problems[0]
        conf = PackageConfig.get_config(problem)
        config_file = self.get_config(conf)
        self.archiver.add_folder(os.path.join(problem, ".tests"), "tests")
        self.archiver.add(conf['checker'], "checker.cpp")
        self.archiver.add(config_file.name, "config")
        if os.path.exists(os.path.join(problem, "statements", "description.ru.tex")):
            self.archiver.add(os.path.join(problem, "statements", "description.ru.tex"), "statement/description")
        splitter = StatementSplitter(os.path.join(problem, "statements", "default.ru.tex"))
        files = splitter.split()
        for filename, file in files.items():
            if os.path.exists(file.name):
                self.archiver.add(file.name, "statement/" + filename)
        for file in glob.glob(os.path.join(problem, "statements", "picture[0-9][0-9].*")):
            self.archiver.add(file, os.path.join("statement", os.path.basename(file)))
        self.archiver.close()
        os.unlink(config_file.name)
        for filename, file in files.items():
            if os.path.exists(file.name):
                os.unlink(file.name)

    def upload_file(self):
        pass

    def run_script(self):
        self.clean_after()

    def clean_after(self):
        subprocess.call(["please", "clean"], cwd=self.problems[0], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_samples_count(self):
        self.clean_after()
        subprocess.call(["please", "generate", "tests", "with", "tag", "sample"], cwd=self.problems[0],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = len(os.listdir(os.path.join(self.problems[0], '.tests'))) // 2
        subprocess.call(["please", "build", "all"], cwd=self.problems[0],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result

    def get_config(self, conf):
        config = {
            "id": int(conf['shortname']),
            "name": conf['name'],
            "time_limit": int(conf['time_limit']),
            "memory_limit": int(conf['memory_limit']),
            "input_file": conf['input'],
            "output_file": conf['output'],
            "tags": conf['tags'],
            "samples": self.get_samples_count(),
        }
        content = json.dumps(config, indent=4, separators=(',', ': '))
        file = NamedTemporaryFile(delete=False)
        file.write(bytes(content, 'utf-8'))
        file.close()
        return file
