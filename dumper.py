from asyncore import read
import json
import string
import os
import random


class Dumper:
    def __init__(self, dump_path=None):

        self.dump_path = self.read("dumper.ini")
        if not self.dump_path:
            print("[!] Error: dumper.ini not found")
            self.can_dump = False
        else:
            self.can_dump = True
            self.force_dump = False

            self.ready()

    def ready(self):
        """
        Make cclass ready to dump
        """

        self.bytes = self.getBytes()

        self.load()

    def read(self, path):
        try:
            return open(path, "r").read()
        except:
            return None

    def write(self, path, content):
        try:
            open(path, "w").write(content)
        except:
            print("[!] Error: can't write to file")

    def parse(self, data):
        """
        Parse the data to dump

        :param data: data to parse
        """
        return json.loads(data)

    def stringify(self):
        """
        Stringify the data to dump
        """
        return json.dumps(self.data)

    def setDumpPath(self, path):
        """
        Set the path to dump all the data

        :param path: path to dump all the data (relative or absolute)
        """
        if os.path.isdir(path):
            self.dump_path = path
            self.write("dumper.ini", path)
        else:
            print("[!] Error: folder doesn't exist")

    def setForceDump(self):
        """
        Set the force dump
        """
        self.force_dump = True

    def load(self):
        """
        Load the data to dump
        """
        self.data = {}
        for paths, dirs, files in os.walk(self.dump_path):
            for f in files:
                fp = os.path.join(paths, f)
                fn = os.path.splitext(f)[0]
                self.data[fn] = open(fp, "r").read()

    def setData(self, key, data):
        """
        Set data to dump

        :param key: key to set the data
        :param data: data to dump
        """
        self.data[key] = data

    def getData(self, key):
        return self.data[key]

    def getBytes(self):
        """
        Get the bytes to dump
        """
        size = 0
        for path, dirs, files in os.walk(self.dump_path):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)

        return size

    def checkIntegrity(self):
        """
        Check if the data to dump is valid
        """

        return self.bytes == self.getBytes()

    def dump(self):
        """
        Dump the data
        """
        if self.checkIntegrity():
            self.dumpToFile()
            print("[+] Dump successful")
        else:
            if self.force_dump:
                self.dumpToFile()
                print("[!] Error: data integrity error, but force dump")

            else:
                rd = self.emergencyDump()
                print("[!] Error: force dump is disabled, emergency dump: " + rd)

    def dumpToFile(self):
        for key, data in self.data.items():
            fp = os.path.join(self.dump_path, key)
            open(f"{fp}.txt", "w").write(data)

    def emergencyDump(self):
        """
        Dump the data to file
        """
        letters = string.ascii_letters
        rd = "".join(random.choice(letters) for i in range(10))
        open(f"{rd}.txt", "w").write(self.stringify())

        return rd
