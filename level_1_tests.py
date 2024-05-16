import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from timeout_decorator import timeout
import unittest
from cloud_storage_impl import CloudStorageImpl




class Level1Tests(unittest.TestCase):
    """
    The test suit below includes 10 tests for Level 1.


    All have the same score.
    You are not allowed to modify this file,
    but feel free to read the source code
    to better understand what is happening in every specific case.
    """


    failureException = Exception




    @classmethod
    def setUp(cls):
        cls.storage = CloudStorageImpl()


    @timeout(0.4)
    def test_level_1_case_01_add_and_get_file_in_directory(self):
        self.assertTrue(self.storage.add_file('/dir/file.txt', 10))
        self.assertEqual(self.storage.get_file_size('/dir/file.txt'), 10)


    @timeout(0.4)
    def test_level_1_case_02_add_and_get_files(self):
        self.assertTrue(self.storage.add_file('/directory/dir/file1.txt', 15))
        self.assertTrue(self.storage.add_file('/file2', 79))
        self.assertEqual(self.storage.get_file_size('/directory/dir/file1.txt'), 15)
        self.assertEqual(self.storage.get_file_size('/directory/dir/file1.txt'), 15)
        self.assertEqual(self.storage.get_file_size('/file2'), 79)


    @timeout(0.4)
    def test_level_1_case_03_add_copy_and_get_files(self):
        self.assertTrue(self.storage.add_file('/dir/file1.mov', 20))
        self.assertTrue(self.storage.copy_file('/dir/file1.mov', '/file2.mp4'))
        self.assertEqual(self.storage.get_file_size('/dir/file1.mov'), 20)
        self.assertEqual(self.storage.get_file_size('/file2.mp4'), 20)


    @timeout(0.4)
    def test_level_1_case_04_multiple_files_add_get_and_copy(self):
        self.assertTrue(self.storage.add_file('/scratch/main.cpp', 99))
        self.assertEqual(self.storage.get_file_size('/scratch/main.cpp'), 99)
        self.assertTrue(self.storage.copy_file('/scratch/main.cpp', '/src/app.cpp'))
        self.assertTrue(self.storage.add_file('/scratch/foo.h', 14))
        self.assertTrue(self.storage.copy_file('/scratch/foo.h', '/include/header.h'))
        self.assertEqual(self.storage.get_file_size('/scratch/foo.h'), 14)
        self.assertEqual(self.storage.get_file_size('/src/app.cpp'), 99)
        self.assertEqual(self.storage.get_file_size('/include/header.h'), 14)


    @timeout(0.4)
    def test_level_1_case_05_adding_duplicate_file(self):
        self.assertTrue(self.storage.add_file('/dir/file1.mov', 20))
        self.assertEqual(self.storage.get_file_size('/dir/file1.mov'), 20)
        self.assertFalse(self.storage.add_file('/dir/file1.mov', 70))
        self.assertFalse(self.storage.add_file('/dir/file1.mov', 90))
        self.assertEqual(self.storage.get_file_size('/dir/file1.mov'), 20)
        self.assertTrue(self.storage.add_file('/dir2/file1.mov', 11))


    @timeout(0.4)
    def test_level_1_case_06_getting_non_existing_file(self):
        self.assertIsNone(self.storage.get_file_size('/dir/non-existing-file.gif'))
        self.assertTrue(self.storage.add_file('/dir/non-existing-file.gif', 34))
        self.assertIsNone(self.storage.get_file_size('/non-existing-file.gif'))
        self.assertTrue(self.storage.add_file('/non-existing-file.gif', 100000))
        self.assertEqual(self.storage.get_file_size('/non-existing-file.gif'), 100000)


    @timeout(0.4)
    def test_level_1_case_07_copy_non_existing_file_or_copy_to_existing_file(self):
        self.assertFalse(self.storage.copy_file('/from/file', '/to/file'))
        self.assertIsNone(self.storage.get_file_size('/to/file'))
        self.assertTrue(self.storage.add_file('/from/file', 68))
        self.assertFalse(self.storage.copy_file('/to/file', '/file'))
        self.assertTrue(self.storage.add_file('/to/file', 11))
        self.assertFalse(self.storage.copy_file('/from/file', '/to/file'))
        self.assertTrue(self.storage.copy_file('/from/file', '/file'))


    @timeout(0.4)
    def test_level_1_case_08_similar_names(self):
        self.assertTrue(self.storage.add_file('/file/file.txt', 50))
        self.assertTrue(self.storage.add_file('/file.png', 880))
        self.assertIsNone(self.storage.get_file_size('/file/file.txt50'))
        self.assertIsNone(self.storage.get_file_size('/file/file'))
        self.assertIsNone(self.storage.get_file_size('/fil'))
        self.assertEqual(self.storage.get_file_size('/file/file.txt'), 50)
        self.assertTrue(self.storage.copy_file('/file.png', '/file.png880'))
        self.assertTrue(self.storage.add_file('/file.png8', 80))
        self.assertTrue(self.storage.copy_file('/file/file.txt', '/file.pn'))
        self.assertEqual(self.storage.get_file_size('/file.pn'), 50)
        self.assertEqual(self.storage.get_file_size('/file.png'), 880)
        self.assertEqual(self.storage.get_file_size('/file.png8'), 80)
        self.assertEqual(self.storage.get_file_size('/file.png880'), 880)


    @timeout(0.4)
    def test_level_1_case_09_mixed1(self):
        self.assertTrue(self.storage.add_file('/file1', 50))
        self.assertTrue(self.storage.add_file('/file2', 30))
        self.assertTrue(self.storage.add_file('/file3', 60))
        self.assertFalse(self.storage.copy_file('/file1', '/file2'))
        self.assertFalse(self.storage.copy_file('/file2', '/file3'))
        self.assertFalse(self.storage.copy_file('/file3', '/file1'))
        self.assertEqual(self.storage.get_file_size('/file3'), 60)
        self.assertEqual(self.storage.get_file_size('/file2'), 30)
        self.assertEqual(self.storage.get_file_size('/file1'), 50)
        self.assertFalse(self.storage.add_file('/file1', 46))
        self.assertTrue(self.storage.add_file('/dir1/file1', 42))
        self.assertTrue(self.storage.add_file('/dir2/dir1/file1', 60))
        self.assertTrue(self.storage.copy_file('/dir1/file1', '/file4'))
        self.assertTrue(self.storage.copy_file('/file4', '/dir2/file1'))
        self.assertEqual(self.storage.get_file_size('/file1'), 50)
        self.assertEqual(self.storage.get_file_size('/dir1/file1'), 42)


    @timeout(0.4)
    def test_level_1_case_10_mixed2(self):
        self.assertFalse(self.storage.copy_file('/filedir/file', '/dir1/file1'))
        self.assertIsNone(self.storage.get_file_size('/filedir/file'))
        self.assertFalse(self.storage.copy_file('/file2', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/file1'))
        self.assertIsNone(self.storage.get_file_size('/dir2/file1'))
        self.assertTrue(self.storage.add_file('/file2', 17))
        self.assertIsNone(self.storage.get_file_size('/dir2/file2'))
        self.assertFalse(self.storage.copy_file('/dir2/file2', '/dir2/file1'))
        self.assertTrue(self.storage.add_file('/dir2/dir1/file1', 41))
        self.assertFalse(self.storage.copy_file('/filedir/file', '/filedir/dir1/file1'))
        self.assertIsNone(self.storage.get_file_size('/dir2/file1'))
        self.assertTrue(self.storage.add_file('/filedir/file', 67))
        self.assertIsNone(self.storage.get_file_size('/dir2/file1'))
        self.assertFalse(self.storage.add_file('/dir2/dir1/file1', 74))
        self.assertTrue(self.storage.add_file('/file1', 26))
        self.assertFalse(self.storage.add_file('/file2', 25))
        self.assertIsNone(self.storage.get_file_size('/file1file2'))
        self.assertIsNone(self.storage.get_file_size('/file'))
        self.assertFalse(self.storage.copy_file('/file', '/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/file2', '/file1'))
        self.assertIsNone(self.storage.get_file_size('/file1file2'))
        self.assertFalse(self.storage.add_file('/dir2/dir1/file1', 74))
        self.assertFalse(self.storage.add_file('/file1', 2))
        self.assertFalse(self.storage.copy_file('/dir1/file2', '/file'))
        self.assertIsNone(self.storage.get_file_size('/dir1/file1'))
        self.assertTrue(self.storage.copy_file('/filedir/file', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/file1file2', '/dir2/file2'))
        self.assertFalse(self.storage.add_file('/filedir/file', 36))
        self.assertFalse(self.storage.copy_file('/dir2/file1', '/dir1/file1'))
        self.assertTrue(self.storage.add_file('/dir2/file1', 91))
        self.assertTrue(self.storage.add_file('/file1file2', 17))
        self.assertFalse(self.storage.copy_file('/dir2/file1', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.add_file('/file2', 78))
        self.assertTrue(self.storage.add_file('/file3', 25))
        self.assertIsNone(self.storage.get_file_size('/dir1/file1'))
        self.assertFalse(self.storage.add_file('/file2', 15))
        self.assertEqual(self.storage.get_file_size('/file1'), 26)
        self.assertFalse(self.storage.copy_file('/filedir/dir1/file1', '/filedir/file'))
        self.assertTrue(self.storage.copy_file('/dir2/file1', '/dir2/file2'))
        self.assertFalse(self.storage.copy_file('/file1file2', '/file1'))
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/file2'))
        self.assertEqual(self.storage.get_file_size('/file3'), 25)
        self.assertEqual(self.storage.get_file_size('/file1'), 26)
        self.assertTrue(self.storage.add_file('/dir1/file2', 96))
        self.assertFalse(self.storage.add_file('/file2', 43))
        self.assertEqual(self.storage.get_file_size('/filedir/file'), 67)
        self.assertFalse(self.storage.add_file('/filedir/file', 100))
        self.assertEqual(self.storage.get_file_size('/filedir/file'), 67)
        self.assertFalse(self.storage.add_file('/file1', 25))
        self.assertFalse(self.storage.add_file('/file3', 65))
        self.assertTrue(self.storage.copy_file('/file1', '/dir1/file1'))
        self.assertFalse(self.storage.add_file('/filedir/file', 96))
        self.assertTrue(self.storage.copy_file('/dir1/file1', '/file'))
        self.assertFalse(self.storage.add_file('/dir2/file1', 36))
        self.assertFalse(self.storage.add_file('/dir2/file1', 13))
        self.assertFalse(self.storage.add_file('/dir2/dir1/file1', 26))
        self.assertFalse(self.storage.add_file('/file2', 39))
        self.assertFalse(self.storage.add_file('/file3', 50))
        self.assertFalse(self.storage.add_file('/filedir/file', 11))
        self.assertEqual(self.storage.get_file_size('/dir2/file2'), 91)
        self.assertFalse(self.storage.add_file('/dir1/file1', 25))
        self.assertFalse(self.storage.copy_file('/file', '/dir2/file1'))
        self.assertFalse(self.storage.add_file('/file', 27))
        self.assertEqual(self.storage.get_file_size('/dir1/file2'), 96)
        self.assertEqual(self.storage.get_file_size('/dir1/file1'), 26)
        self.assertFalse(self.storage.copy_file('/file1file2', '/file2'))
        self.assertFalse(self.storage.add_file('/file', 8))
        self.assertEqual(self.storage.get_file_size('/filedir/dir1/file1'), 67)
        self.assertFalse(self.storage.copy_file('/file', '/dir2/file1'))
        self.assertEqual(self.storage.get_file_size('/file2'), 17)
        self.assertFalse(self.storage.add_file('/dir1/file2', 61))
        self.assertFalse(self.storage.add_file('/file1', 90))
        self.assertFalse(self.storage.copy_file('/file3', '/file2'))
        self.assertFalse(self.storage.copy_file('/dir1/file2', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/file1', '/dir1/file1'))
        self.assertEqual(self.storage.get_file_size('/file'), 26)
        self.assertFalse(self.storage.copy_file('/file2', '/file1'))
        self.assertFalse(self.storage.add_file('/dir2/dir1/file1', 96))
        self.assertFalse(self.storage.add_file('/dir1/file2', 52))
        self.assertFalse(self.storage.copy_file('/dir1/file2', '/file2'))
        self.assertFalse(self.storage.copy_file('/filedir/dir1/file1', '/file'))
        self.assertEqual(self.storage.get_file_size('/file1'), 26)
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/dir1/file2'))
        self.assertEqual(self.storage.get_file_size('/file3'), 25)
        self.assertEqual(self.storage.get_file_size('/dir2/file1'), 91)
        self.assertEqual(self.storage.get_file_size('/file1'), 26)
        self.assertEqual(self.storage.get_file_size('/file2'), 17)
        self.assertFalse(self.storage.copy_file('/dir2/file2', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.add_file('/dir2/dir1/file1', 38))
        self.assertEqual(self.storage.get_file_size('/filedir/dir1/file1'), 67)
        self.assertEqual(self.storage.get_file_size('/dir2/dir1/file1'), 41)
        self.assertFalse(self.storage.copy_file('/file1', '/filedir/dir1/file1'))
        self.assertFalse(self.storage.add_file('/file2', 96))
        self.assertEqual(self.storage.get_file_size('/file1'), 26)
        self.assertFalse(self.storage.add_file('/dir2/file2', 31))
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/file'))
        self.assertFalse(self.storage.copy_file('/file1', '/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/filedir/dir1/file1', '/file3'))
        self.assertFalse(self.storage.add_file('/file1', 30))
        self.assertEqual(self.storage.get_file_size('/file3'), 25)
        self.assertEqual(self.storage.get_file_size('/dir2/dir1/file1'), 41)
        self.assertEqual(self.storage.get_file_size('/dir2/file1'), 91)
        self.assertFalse(self.storage.copy_file('/file3', '/file1file2'))
        self.assertEqual(self.storage.get_file_size('/file3'), 25)
        self.assertFalse(self.storage.copy_file('/filedir/file', '/file1file2'))
        self.assertEqual(self.storage.get_file_size('/dir1/file2'), 96)
        self.assertFalse(self.storage.add_file('/filedir/file', 64))
        self.assertEqual(self.storage.get_file_size('/filedir/dir1/file1'), 67)
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/dir2/file2'))
        self.assertFalse(self.storage.copy_file('/file1file2', '/dir2/dir1/file1'))
        self.assertEqual(self.storage.get_file_size('/dir1/file1'), 26)
        self.assertEqual(self.storage.get_file_size('/filedir/dir1/file1'), 67)
        self.assertFalse(self.storage.copy_file('/file3', '/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/file1file2', '/filedir/file'))
        self.assertFalse(self.storage.copy_file('/file3', '/file2'))
        self.assertFalse(self.storage.copy_file('/file', '/filedir/file'))
        self.assertFalse(self.storage.add_file('/file3', 25))
        self.assertEqual(self.storage.get_file_size('/dir2/file1'), 91)
        self.assertFalse(self.storage.add_file('/file3', 65))
        self.assertFalse(self.storage.copy_file('/file', '/dir2/file2'))
        self.assertFalse(self.storage.copy_file('/dir1/file1', '/file'))
        self.assertFalse(self.storage.add_file('/dir1/file2', 86))
        self.assertFalse(self.storage.add_file('/dir1/file1', 44))
        self.assertEqual(self.storage.get_file_size('/dir2/dir1/file1'), 41)
        self.assertFalse(self.storage.copy_file('/filedir/dir1/file1', '/file2'))
        self.assertFalse(self.storage.add_file('/file', 34))
        self.assertFalse(self.storage.add_file('/dir1/file1', 39))
        self.assertFalse(self.storage.add_file('/dir2/file2', 6))
        self.assertFalse(self.storage.copy_file('/file1', '/dir2/file2'))
        self.assertEqual(self.storage.get_file_size('/dir2/file1'), 91)
        self.assertFalse(self.storage.copy_file('/file3', '/file1file2'))
        self.assertFalse(self.storage.copy_file('/file2', '/filedir/file'))
        self.assertFalse(self.storage.add_file('/file1file2', 40))
        self.assertFalse(self.storage.copy_file('/file3', '/dir2/file1'))
        self.assertFalse(self.storage.add_file('/dir2/file2', 57))
        self.assertFalse(self.storage.copy_file('/file3', '/dir2/file2'))
        self.assertFalse(self.storage.add_file('/dir1/file1', 25))
        self.assertFalse(self.storage.add_file('/file', 16))
        self.assertFalse(self.storage.add_file('/dir2/file2', 52))
        self.assertEqual(self.storage.get_file_size('/file2'), 17)
        self.assertEqual(self.storage.get_file_size('/filedir/file'), 67)
        self.assertFalse(self.storage.copy_file('/file2', '/dir2/dir1/file1'))
        self.assertFalse(self.storage.copy_file('/dir2/dir1/file1', '/file1file2'))
        self.assertEqual(self.storage.get_file_size('/dir2/dir1/file1'), 41)
        self.assertFalse(self.storage.copy_file('/file', '/dir2/file1'))
        self.assertEqual(self.storage.get_file_size('/file2'), 17)
        self.assertEqual(self.storage.get_file_size('/file3'), 25)
        self.assertFalse(self.storage.add_file('/file1file2', 24))
        self.assertFalse(self.storage.copy_file('/dir1/file2', '/filedir/dir1/file1'))
        self.assertEqual(self.storage.get_file_size('/dir1/file1'), 26)
