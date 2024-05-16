import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from timeout_decorator import timeout
import unittest
from cloud_storage_impl import CloudStorageImpl




class Level2Tests(unittest.TestCase):
    """
    The test suit below includes 10 tests for Level 2.


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
    def test_level_2_case_01_find_single_file_in_directory(self):
        self.assertTrue(self.storage.add_file('/dir/file.txt', 10))
        expected = ['/dir/file.txt(10)']
        self.assertEqual(self.storage.find_file('/dir', 'file.txt'), expected)


    @timeout(0.4)
    def test_level_2_case_02_find_single_file_in_nested_directory(self):
        self.assertTrue(self.storage.add_file('/file.txt', 5))
        self.assertTrue(self.storage.add_file('/dir/file.txt', 10))
        self.assertTrue(self.storage.add_file('/dir/dir/file.txt', 15))
        expected = ['/dir/dir/file.txt(15)', '/dir/file.txt(10)']
        self.assertEqual(self.storage.find_file('/dir', 'file.txt'), expected)


    @timeout(0.4)
    def test_level_2_case_03_find_several_files_in_nested_directory(self):
        self.assertTrue(self.storage.add_file('/dir/file.txt', 23))
        self.assertTrue(self.storage.add_file('/dir/another_dir/file.txt', 35))
        self.assertTrue(self.storage.add_file('/dir/dir2/file.txt', 37))
        self.assertTrue(self.storage.add_file('/dir/dir/file.txt', 11))
        self.assertTrue(self.storage.add_file('/file.txt', 12))
        expected = ['/dir/dir2/file.txt(37)', '/dir/another_dir/file.txt(35)', '/dir/file.txt(23)', '/dir/dir/file.txt(11)']
        self.assertEqual(self.storage.find_file('/dir', 'file.txt'), expected)
        self.assertEqual(self.storage.get_file_size('/dir/file.txt'), 23)


    @timeout(0.4)
    def test_level_2_case_04_find_files_with_same_size_in_path(self):
        self.assertTrue(self.storage.add_file('/foo/foo/file', 10))
        self.assertTrue(self.storage.add_file('/foo/file', 20))
        self.assertTrue(self.storage.add_file('/foo/bar/xyz/file', 15))
        self.assertTrue(self.storage.add_file('/bar/xyz/file', 10))
        self.assertTrue(self.storage.add_file('/foo/bar/file', 10))
        self.assertTrue(self.storage.add_file('/foo/foo/bar/file', 20))
        self.assertTrue(self.storage.add_file('/file', 5))
        self.assertTrue(self.storage.add_file('/dir/dir/file.html', 25))
        expected = ['/foo/file(20)', '/foo/foo/bar/file(20)', '/foo/bar/xyz/file(15)', '/foo/bar/file(10)', '/foo/foo/file(10)']
        self.assertEqual(self.storage.find_file('/foo', 'file'), expected)


    @timeout(0.4)
    def test_level_2_case_05_find_files_in_root_path(self):
        self.assertTrue(self.storage.add_file('/file.html', 15))
        self.assertTrue(self.storage.add_file('/dir/file.html', 25))
        self.assertTrue(self.storage.add_file('/filex.html', 15))
        self.assertTrue(self.storage.add_file('/dir/dir/file.html', 15))
        expected = ['/dir/file.html(25)', '/dir/dir/file.html(15)', '/file.html(15)']
        self.assertEqual(self.storage.find_file('/', 'file.html'), expected)


    @timeout(0.4)
    def test_level_2_case_06_given_path_does_not_exist(self):
        self.assertTrue(self.storage.add_file('/foo/file.png', 10))
        self.assertTrue(self.storage.add_file('/foo/bar/file.png', 10))
        self.assertTrue(self.storage.add_file('/file.png', 10))
        self.assertTrue(self.storage.add_file('/foo/bar/file2.png', 10))
        self.assertTrue(self.storage.add_file('/foo/file2.png', 10))
        self.assertFalse(self.storage.find_file('/bar', 'file.png'))


    @timeout(0.4)
    def test_level_2_case_07_file_is_not_found(self):
        self.assertTrue(self.storage.add_file('/file.html', 10))
        self.assertTrue(self.storage.add_file('/dir/file.png', 20))
        self.assertTrue(self.storage.add_file('/directory/file.txt', 30))
        self.assertTrue(self.storage.add_file('/folder/file.jpg', 40))
        self.assertTrue(self.storage.add_file('/folder/another/file.css', 50))
        self.assertFalse(self.storage.add_file('/folder/another/file.css', 30))
        self.assertTrue(self.storage.add_file('/file.mp3', 10))
        self.assertFalse(self.storage.find_file('/', 'file'))


    @timeout(0.4)
    def test_level_2_case_08_tree_easy(self):
        self.assertTrue(self.storage.add_file('/file1.txt', 7))
        self.assertTrue(self.storage.add_file('/file2.txt', 5))
        self.assertTrue(self.storage.add_file('/file3.txt', 3))
        self.assertTrue(self.storage.copy_file('/file1.txt', '/file4.txt'))
        self.assertTrue(self.storage.copy_file('/file3.txt', '/file5.txt'))
        self.assertEqual(self.storage.get_file_size('/file2.txt'), 5)
        self.assertEqual(self.storage.get_file_size('/file4.txt'), 7)
        expected = ['/file1.txt(7)']
        self.assertEqual(self.storage.find_file('/', 'file1.txt'), expected)
        self.assertFalse(self.storage.find_file('/', 'file6.txt'))
        self.assertFalse(self.storage.find_file('/dir', 'file1.txt'))


    @timeout(0.4)
    def test_level_2_case_09_tree_medium(self):
        self.assertTrue(self.storage.add_file('/file1', 5))
        self.assertTrue(self.storage.add_file('/file2', 3))
        self.assertTrue(self.storage.add_file('/dir/file1', 23))
        self.assertTrue(self.storage.copy_file('/dir/file1', '/dir/file2'))
        self.assertTrue(self.storage.add_file('/dir/dir/file1', 12))
        self.assertTrue(self.storage.add_file('/dir/dir/file2', 3))
        self.assertIsNone(self.storage.get_file_size('/dir'))
        self.assertEqual(self.storage.get_file_size('/dir/file1'), 23)
        self.assertEqual(self.storage.get_file_size('/dir/file2'), 23)
        expected = ['/dir/file1(23)', '/dir/dir/file1(12)']
        self.assertEqual(self.storage.find_file('/dir', 'file1'), expected)
        expected = ['/dir/file2(23)', '/dir/dir/file2(3)']
        self.assertEqual(self.storage.find_file('/dir', 'file2'), expected)


    @timeout(0.4)
    def test_level_2_case_10_tree_hard(self):
        self.assertTrue(self.storage.add_file('/file1.txt', 7))
        self.assertTrue(self.storage.add_file('/file2.txt', 15))
        self.assertTrue(self.storage.add_file('/dir/file1.txt', 23))
        self.assertTrue(self.storage.add_file('/dir/dir1/file2.txt', 30))
        self.assertTrue(self.storage.add_file('/dir/dir2/file1.txt', 15))
        self.assertTrue(self.storage.add_file('/dir/dir1/fl.html', 59))
        self.assertTrue(self.storage.add_file('/file3.txt', 150))
        self.assertTrue(self.storage.copy_file('/file1.txt', '/dir/dir/dir/dir/file2.txt'))
        self.assertTrue(self.storage.add_file('/dir/dir1/dir/file1.txt', 1))
        self.assertTrue(self.storage.add_file('/dir/dir1/dir/file2.txt', 1))
        self.assertTrue(self.storage.copy_file('/dir/dir2/file1.txt', '/dir/dir/dir2/file2.txt'))
        self.assertTrue(self.storage.add_file('/file3', 50))
        expected = ['/file3(50)']
        self.assertEqual(self.storage.find_file('/', 'file3'), expected)
        expected = ['/dir/dir1/fl.html(59)']
        self.assertEqual(self.storage.find_file('/dir', 'fl.html'), expected)
        expected = ['/dir/dir1/file2.txt(30)', '/dir/dir1/dir/file2.txt(1)']
        self.assertEqual(self.storage.find_file('/dir/dir1', 'file2.txt'), expected)
        expected = ['/dir/dir2/file1.txt(15)']
        self.assertEqual(self.storage.find_file('/dir/dir2', 'file1.txt'), expected)
        expected = ['/dir/dir1/file2.txt(30)', '/dir/dir/dir2/file2.txt(15)', '/dir/dir/dir/dir/file2.txt(7)', '/dir/dir1/dir/file2.txt(1)']
        self.assertEqual(self.storage.find_file('/dir/dir', 'file2.txt'), expected)
        expected = ['/dir/dir/dir2/file2.txt(15)', '/dir/dir/dir/dir/file2.txt(7)']
        self.assertEqual(self.storage.find_file('/dir/dir/dir', 'file2.txt'), expected)
