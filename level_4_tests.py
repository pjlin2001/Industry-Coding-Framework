import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from timeout_decorator import timeout
import unittest
from cloud_storage_impl import CloudStorageImpl




class Level4Tests(unittest.TestCase):
    """
    The test suit below includes 10 tests for Level 4.


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
    def test_level_4_case_01_should_compress_single_file(self):
        self.assertTrue(self.storage.add_user('username', 1000))
        self.assertEqual(self.storage.add_file_by('username', '/my/super/file.txt', 100), 900)
        self.assertEqual(self.storage.compress_file('username', '/my/super/file.txt'), 950)
        self.assertIsNone(self.storage.get_file_size('/my/super/file.txt'))
        self.assertEqual(self.storage.get_file_size('/my/super/file.txt.COMPRESSED'), 50)


    @timeout(0.4)
    def test_level_4_case_02_should_decompress_single_file(self):
        self.assertTrue(self.storage.add_user('qwerty', 3333))
        self.assertEqual(self.storage.add_file_by('qwerty', '/foo/bar/xyz/video.mp4', 1000), 2333)
        self.assertEqual(self.storage.compress_file('qwerty', '/foo/bar/xyz/video.mp4'), 2833)
        self.assertIsNone(self.storage.get_file_size('/foo/bar/xyz/video.mp4'))
        self.assertEqual(self.storage.get_file_size('/foo/bar/xyz/video.mp4.COMPRESSED'), 500)
        self.assertEqual(self.storage.decompress_file('qwerty', '/foo/bar/xyz/video.mp4.COMPRESSED'), 2333)
        self.assertEqual(self.storage.get_file_size('/foo/bar/xyz/video.mp4'), 1000)
        self.assertIsNone(self.storage.get_file_size('/foo/bar/xyz/video.mp4.COMPRESSED'))


    @timeout(0.4)
    def test_level_4_case_03_should_not_decompress_if_there_is_a_collision(self):
        self.assertTrue(self.storage.add_user('audiophile', 2000))
        self.assertEqual(self.storage.add_file_by('audiophile', '/music/queen.mp3', 300), 1700)
        self.assertEqual(self.storage.compress_file('audiophile', '/music/queen.mp3'), 1850)
        self.assertIsNone(self.storage.get_file_size('/music/queen.mp3'))
        self.assertEqual(self.storage.add_file_by('audiophile', '/music/queen.mp3', 400), 1450)
        self.assertIsNone(self.storage.decompress_file('audiophile', '/music/queen.mp3.COMPRESSED'))
        self.assertEqual(self.storage.get_file_size('/music/queen.mp3'), 400)
        self.assertEqual(self.storage.get_file_size('/music/queen.mp3.COMPRESSED'), 150)


    @timeout(0.4)
    def test_level_4_case_04_should_not_decompress_file_if_not_enough_space(self):
        self.assertTrue(self.storage.add_user('moderator', 5000))
        self.assertEqual(self.storage.add_file_by('moderator', '/my_file/large_file', 4000), 1000)
        self.assertEqual(self.storage.compress_file('moderator', '/my_file/large_file'), 3000)
        self.assertEqual(self.storage.add_file_by('moderator', '/my_file/medium_file', 2000), 1000)
        self.assertIsNone(self.storage.decompress_file('moderator', '/my_file/large_file.COMPRESSED'))
        self.assertEqual(self.storage.add_file_by('moderator', '/my_file/small_file', 1000), 0)
        self.assertEqual(self.storage.get_file_size('/my_file/large_file.COMPRESSED'), 2000)


    @timeout(0.4)
    def test_level_4_case_05_should_not_compress_if_user_or_file_does_not_exist_or_if_compressed_file_exists(self):
        self.assertTrue(self.storage.add_user('user', 999))
        self.assertEqual(self.storage.add_file_by('user', '/dir/file', 100), 899)
        self.assertIsNone(self.storage.compress_file('non_existing_user', '/dir/file'))
        self.assertEqual(self.storage.get_file_size('/dir/file'), 100)
        self.assertIsNone(self.storage.compress_file('user', '/path/to/nowhere'))
        self.assertEqual(self.storage.compress_file('user', '/dir/file'), 949)
        self.assertEqual(self.storage.add_file_by('user', '/dir/file', 100), 849)
        self.assertIsNone(self.storage.compress_file('user', '/dir/file'))
        self.assertEqual(self.storage.get_file_size('/dir/file'), 100)
        self.assertEqual(self.storage.get_file_size('/dir/file.COMPRESSED'), 50)


    @timeout(0.4)
    def test_level_4_case_06_should_not_decompress_if_user_or_file_does_not_exist(self):
        self.assertTrue(self.storage.add_user('student', 10000))
        self.assertEqual(self.storage.add_file_by('student', '/foo/bar/file.mp3', 10000), 0)
        self.assertIsNone(self.storage.decompress_file('student', '/foo/bar.COMPRESSED'))
        self.assertEqual(self.storage.compress_file('student', '/foo/bar/file.mp3'), 5000)
        self.assertIsNone(self.storage.decompress_file('teacher', '/foo/bar/file.mp3.COMPRESSED'))
        self.assertEqual(self.storage.get_file_size('/foo/bar/file.mp3.COMPRESSED'), 5000)


    @timeout(0.4)
    def test_level_4_case_07_should_not_compress_or_decompress_files_owned_by_other_users(self):
        self.assertTrue(self.storage.add_user('owner', 5000))
        self.assertEqual(self.storage.add_file_by('owner', '/storage/passwords.txt', 1000), 4000)
        self.assertTrue(self.storage.add_user('hacker', 9999))
        self.assertIsNone(self.storage.compress_file('hacker', '/storage/passwords.txt'))
        self.assertEqual(self.storage.compress_file('owner', '/storage/passwords.txt'), 4500)
        self.assertIsNone(self.storage.decompress_file('hacker', '/storage/passwords.txt.COMPRESSED'))
        self.assertEqual(self.storage.decompress_file('owner', '/storage/passwords.txt.COMPRESSED'), 4000)


    @timeout(0.4)
    def test_level_4_case_08_make_copies_of_compressed_files_and_decompress(self):
        self.assertTrue(self.storage.add_user('user1', 5000))
        self.assertTrue(self.storage.add_user('user2', 3000))
        self.assertEqual(self.storage.add_file_by('user1', '/deep/deeper/my_file', 300), 4700)
        self.assertEqual(self.storage.compress_file('user1', '/deep/deeper/my_file'), 4850)
        self.assertTrue(self.storage.copy_file('/deep/deeper/my_file.COMPRESSED', '/my_file.COMPRESSED'))
        self.assertEqual(self.storage.decompress_file('user1', '/my_file.COMPRESSED'), 4550)
        expected = ['/my_file(300)']
        self.assertEqual(self.storage.find_file('/', 'my_file'), expected)
        expected = ['/deep/deeper/my_file.COMPRESSED(150)']
        self.assertEqual(self.storage.find_file('/', 'my_file.COMPRESSED'), expected)
        self.assertEqual(self.storage.add_file_by('user2', '/somewhere/my_file', 1000), 2000)
        self.assertEqual(self.storage.compress_file('user2', '/somewhere/my_file'), 2500)
        self.assertTrue(self.storage.copy_file('/somewhere/my_file.COMPRESSED', '/my_file.COMPRESSED'))
        self.assertTrue(self.storage.copy_file('/somewhere/my_file.COMPRESSED', '/deep/my_file.COMPRESSED'))
        self.assertEqual(self.storage.decompress_file('user2', '/deep/my_file.COMPRESSED'), 1000)
        self.assertEqual(self.storage.add_file_by('user1', '/deep/deeper/my_file', 300), 4250)
        self.assertIsNone(self.storage.compress_file('user1', '/deep/deeper/my_file'))
        expected = ['/deep/my_file(1000)', '/deep/deeper/my_file(300)', '/my_file(300)']
        self.assertEqual(self.storage.find_file('/', 'my_file'), expected)
        expected = ['/my_file.COMPRESSED(500)', '/somewhere/my_file.COMPRESSED(500)', '/deep/deeper/my_file.COMPRESSED(150)']
        self.assertEqual(self.storage.find_file('/', 'my_file.COMPRESSED'), expected)


    @timeout(0.4)
    def test_level_4_case_09_mixed1(self):
        self.assertTrue(self.storage.add_user('user1', 5000))
        self.assertEqual(self.storage.add_file_by('user1', '/user1/file', 2000), 3000)
        self.assertEqual(self.storage.add_file_by('user1', '/user1/file2', 1000), 2000)
        self.assertEqual(self.storage.compress_file('user1', '/user1/file2'), 2500)
        self.assertTrue(self.storage.copy_file('/user1/file2.COMPRESSED', '/common/file.COMPRESSED'))
        self.assertEqual(self.storage.decompress_file('user1', '/user1/file2.COMPRESSED'), 1500)
        self.assertEqual(self.storage.decompress_file('user1', '/common/file.COMPRESSED'), 1000)
        self.assertTrue(self.storage.add_user('user2', 3000))
        self.assertEqual(self.storage.add_file_by('user2', '/user2/file', 1000), 2000)
        self.assertTrue(self.storage.copy_file('/user2/file', '/user2/file2'))
        self.assertIsNone(self.storage.compress_file('user1', '/user2/file2'))
        self.assertEqual(self.storage.compress_file('user2', '/user2/file2'), 1500)
        self.assertTrue(self.storage.copy_file('/user2/file2.COMPRESSED', '/common/file.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user1', '/common/file.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user2', '/common/file.COMPRESSED'))
        self.assertTrue(self.storage.copy_file('/common/file.COMPRESSED', '/common/sub/file.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user2', '/common/file.COMPRESSED'))
        self.assertEqual(self.storage.update_capacity('user2', 5000), 0)
        self.assertIsNone(self.storage.decompress_file('user2', '/common/file.COMPRESSED'))
        expected = ['/user1/file(2000)', '/common/file(1000)', '/user2/file(1000)']
        self.assertEqual(self.storage.find_file('/', 'file'), expected)


    @timeout(0.4)
    def test_level_4_case_10_mixed2(self):
        self.assertTrue(self.storage.add_file('/admin_dir/settings.ini', 1234))
        self.assertFalse(self.storage.copy_file('/admin_dir/settings', '/admin_dir/configs/settings'))
        self.assertFalse(self.storage.add_file('/admin_dir/settings.ini', 239))
        self.assertTrue(self.storage.add_file('/admin_dir/etc.ini', 555))
        self.assertFalse(self.storage.copy_file('/admin_dir/settings.ini', '/admin_dir/etc.ini'))
        self.assertTrue(self.storage.copy_file('/admin_dir/etc.ini', '/admin_dir/configs/settings.ini'))
        self.assertEqual(self.storage.get_file_size('/admin_dir/configs/settings.ini'), 555)
        self.assertIsNone(self.storage.get_file_size('/settings.ini'))
        self.assertTrue(self.storage.add_user('user1', 5000))
        self.assertTrue(self.storage.add_user('user2', 10000))
        self.assertFalse(self.storage.add_user('user1', 10000))
        self.assertIsNone(self.storage.add_file_by('user1', '/admin_dir/settings.ini', 1000))
        self.assertIsNone(self.storage.add_file_by('user3', '/user1_dir/settings.ini', 1500))
        self.assertEqual(self.storage.add_file_by('user1', '/user1_dir/settings.ini', 1000), 4000)
        self.assertIsNone(self.storage.add_file_by('user1', '/user1_dir/trash/video.mp4', 5000))
        self.assertEqual(self.storage.add_file_by('user1', '/user1_dir/games/game2/files/settings.ini', 1000), 3000)
        self.assertEqual(self.storage.add_file_by('user1', '/user1_dir/games/game1/settings.ini', 1500), 1500)
        self.assertEqual(self.storage.add_file_by('user1', '/settings.ini', 300), 1200)
        self.assertEqual(self.storage.add_file_by('user2', '/user2_dir/settings.ini', 1000), 9000)
        self.assertFalse(self.storage.find_file('/foo', 'settings.ini'))
        self.assertFalse(self.storage.find_file('/admin_dir', 'video.mp4'))
        expected = ['/user1_dir/games/game1/settings.ini(1500)', '/user1_dir/games/game2/files/settings.ini(1000)', '/user1_dir/settings.ini(1000)']
        self.assertEqual(self.storage.find_file('/user1_dir', 'settings.ini'), expected)
        expected = ['/user1_dir/games/game1/settings.ini(1500)', '/admin_dir/settings.ini(1234)', '/user1_dir/games/game2/files/settings.ini(1000)', '/user1_dir/settings.ini(1000)', '/user2_dir/settings.ini(1000)', '/admin_dir/configs/settings.ini(555)', '/settings.ini(300)']
        self.assertEqual(self.storage.find_file('/', 'settings.ini'), expected)
        self.assertIsNone(self.storage.update_capacity('user3', 3000))
        self.assertEqual(self.storage.update_capacity('user1', 10000), 0)
        self.assertEqual(self.storage.update_capacity('user1', 3000), 1)
        self.assertIsNone(self.storage.compress_file('user3', '/settings.ini'))
        self.assertIsNone(self.storage.compress_file('user2', '/settings.ini'))
        self.assertEqual(self.storage.compress_file('user1', '/settings.ini'), 850)
        self.assertTrue(self.storage.copy_file('/settings.ini.COMPRESSED', '/user1_dir/settings.ini.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user3', '/user1_dir/settings.ini.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user2', '/user1_dir/settings.ini.COMPRESSED'))
        self.assertIsNone(self.storage.decompress_file('user1', '/user1_dir/settings.ini.COMPRESSED'))
        self.assertTrue(self.storage.copy_file('/settings.ini.COMPRESSED', '/user1_dir/archives/settings.ini.COMPRESSED'))
        self.assertEqual(self.storage.decompress_file('user1', '/user1_dir/archives/settings.ini.COMPRESSED'), 400)
        self.assertEqual(self.storage.compress_file('user1', '/user1_dir/archives/settings.ini'), 550)
        self.assertIsNone(self.storage.add_file_by('user1', '/user1_dir/secret/settings.ini', 600))
        self.assertEqual(self.storage.decompress_file('user1', '/user1_dir/archives/settings.ini.COMPRESSED'), 400)
