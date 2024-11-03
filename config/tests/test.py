import unittest
import shutil
import os
import sys
sys.path.append(os.getcwd())
import main
from unittest.mock import patch

class TestShellCommands(unittest.TestCase):
    def setUp(self):
        main.PATH = "D:\\DAN\\proga\\config\\tests\\test_dir.tar"
        os.remove("D:\\DAN\\proga\\config\\tests\\test_dir.tar")
        shutil.copy("root.tar", "D:\\DAN\\proga\\config\\tests\\test_dir.tar")
        shutil.copy("mode.json", "D:\\DAN\\proga\\config\\tests\\mode.json")
    # тест ls
    def test_ls_empty(self):
        main.current_path = "root/folder_1/"
        self.assertEqual(main.ls(), 'folder/\n' 
                                    'text_1.txt')
    def test_ls_empty_with_flag(self):
        main.current_path = "root/folder_2/folder_1/"
        self.assertEqual(main.ls(1), 'drw-rw-rw- Petya admins folder_1\n'
                                      '-rw-rw-rw- users2 users hello.py\n'
                                      '-rw-rw-rw- Kolya admins text_1.txt')
    def test_ls_absolute_with_flag(self):
        self.assertEqual(main.ls(1, "root/folder_2/folder_1/folder_1/"), '-rw-rw-rw- Vasya users text_1.txt')
    def test_ls_relative(self):
        main.current_path = "root/"
        self.assertEqual(main.ls(0, "folder_3"),    'text_1.txt\n'
                                                    'text_2.txt\n'
                                                    'text_3.txt\n'
                                                    'text_4.txt\n'
                                                    'text_5.txt')
    
    # тест cd
    def test_cd_absolute_path(self):
        main.current_path = "root/"
        self.assertEqual(main.cd("root/folder_2/folder_1"), "Перешли в директорию root/folder_2/folder_1/")
    def test_cd_higher(self):
        main.current_path = "root/folder_2/folder_1"
        self.assertEqual(main.cd(".."), "Перешли в директорию root/folder_2/")
    def test_cd_higher_plus_path(self):
        main.current_path = "root/folder_2/"
        self.assertEqual(main.cd("../folder_3"), "Перешли в директорию root/folder_3/")
    def test_higher_with_root(self):
        main.current_path = "root/"
        self.assertEqual(main.cd(".."), "Вы в корневой папке")
    
    #тест chmod
    def test_chmod_error(self):
        main.current_path = "root/folder_1"
        self.assertEqual(main.chmod("7524", "text_1.txt"), "Неправильный формат прав доступа")
    def test_chmod_file(self):
        main.current_path = "root/"
        main.chmod("777", "folder_1/text_1.txt")
        self.assertEqual(main.ls(1, "folder_1"), "drwx--x--x Vasya admins folder\n"
                                                 "-rwxrwxrwx Vasya users text_1.txt")
    def test_chmod_dir(self):
        main.current_path = "root/folder_2/"
        main.chmod("733", "folder_1")
        self.assertEqual(main.ls(1), "drwx-wx-wx users2 users folder_1\n"
                                      "drw-rw-rw- Petya users folder_2")
    # тест pwd
    def test_pwd_1(self):
        main.current_path = "root/folder_2/folder_1/folder_1/"
        self.assertEqual(main.pwd(), "root/folder_2/folder_1/folder_1/")
    def test_pwd_2(self):
        main.current_path = "root/"
        self.assertEqual(main.pwd(), "root/")
        
    # тест rm
    def test_rm_error(self):
        main.current_path = "root/"
        self.assertEqual(main.rm("folder_1/folder_3"), "Файл root/folder_1/folder_3/ не существует")
    def test_rm_file(self):
        main.current_path = "root/"
        main.rm("folder_3/text_3.txt")
        self.assertEqual(main.ls(0, "folder_3"), 'text_1.txt\n'
                                                'text_2.txt\n'
                                                'text_4.txt\n'
                                                'text_5.txt')
if __name__ == "__main__":
    unittest.main()