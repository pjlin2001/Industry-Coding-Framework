import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from timeout_decorator import timeout
import unittest
from cloud_storage_impl import CloudStorageImpl




class Level3Tests(unittest.TestCase):
    """
    The test suit below includes 10 tests for Level 3.


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
    def test_level_3_case_01_should_add_files_by_users(self):
        self.assertTrue(self.storage.add_user('username', 1000))
        self.assertEqual(self.storage.add_file_by('username', '/username/file.txt', 100), 900)
        self.assertEqual(self.storage.add_file_by('username', '/common/username_file.txt', 200), 700)
        self.assertTrue(self.storage.add_user('moderator', 100))
        self.assertEqual(self.storage.add_file_by('moderator', '/moderator/file.txt', 50), 50)
        self.assertEqual(self.storage.add_file_by('moderator', '/common/moderator_file.txt', 30), 20)
        self.assertEqual(self.storage.add_file_by('username', '/file.txt', 50), 650)


    @timeout(0.4)
    def test_level_3_case_02_should_not_add_files_if_run_out_of_capacity(self):
        self.assertTrue(self.storage.add_user('user100', 100))
        self.assertTrue(self.storage.add_user('user1000', 1000))
        self.assertEqual(self.storage.add_file_by('user100', '/dir/file2', 80), 20)
        self.assertIsNone(self.storage.add_file_by('user100', '/dir/file2', 50))
        self.assertIsNone(self.storage.add_file_by('user1000', '/dir/file2', 1500))
        self.assertIsNone(self.storage.add_file_by('user1000', '/dir/file2', 500))
        self.assertEqual(self.storage.add_file_by('user1000', '/dir/file3', 500), 500)
        self.assertIsNone(self.storage.add_file_by('user1000', '/dir/file4', 600))


    @timeout(0.4)
    def test_level_3_case_03_should_copy_files_of_specific_user_only(self):
        self.assertTrue(self.storage.add_user('new_user', 100))
        self.assertTrue(self.storage.add_user('super_user', 100))
        self.assertEqual(self.storage.add_file_by('new_user', '/tmp/file.txt', 60), 40)
        self.assertEqual(self.storage.add_file_by('super_user', '/tmp/super/file.txt', 40), 60)
        self.assertTrue(self.storage.add_file('/tmp/root/file.txt', 150))
        self.assertFalse(self.storage.copy_file('/tmp/file.txt', '/file.txt'))
        self.assertTrue(self.storage.copy_file('/tmp/super/file.txt', '/super/file.txt'))
        self.assertTrue(self.storage.copy_file('/tmp/root/file.txt', '/root/file.txt'))


    @timeout(0.4)
    def test_level_3_case_04_should_update_capacity(self):
        self.assertTrue(self.storage.add_user('owner', 1000))
        self.assertEqual(self.storage.add_file_by('owner', '/foo/bar/large_file', 600), 400)
        self.assertEqual(self.storage.add_file_by('owner', '/foo/small_file', 200), 200)
        self.assertIsNone(self.storage.add_file_by('owner', '/foo/medium_file', 400))
        self.assertEqual(self.storage.update_capacity('owner', 1500), 0)
        self.assertEqual(self.storage.update_capacity('owner', 800), 0)
        self.assertEqual(self.storage.update_capacity('owner', 500), 1)
        self.assertEqual(self.storage.update_capacity('owner', 100), 1)


    @timeout(0.4)
    def test_level_3_case_05_should_not_add_user_with_existing_user_id(self):
        self.assertTrue(self.storage.add_user('user1', 1000))
        self.assertTrue(self.storage.add_user('user2', 1000))
        self.assertFalse(self.storage.add_user('user1', 500))
        self.assertFalse(self.storage.add_user('user2', 1500))
        self.assertEqual(self.storage.add_file_by('user1', '/user1_file', 700), 300)
        self.assertIsNone(self.storage.add_file_by('user2', '/user2_file', 1200))


    @timeout(0.4)
    def test_level_3_case_06_should_not_add_file_if_it_already_exists_or_user_does_not_exist(self):
        self.assertTrue(self.storage.add_user('user1', 700))
        self.assertTrue(self.storage.add_user('user2', 500))
        self.assertEqual(self.storage.add_file_by('user1', '/super/secret/file.txt', 300), 400)
        self.assertIsNone(self.storage.add_file_by('user2', '/super/secret/file.txt', 400))
        self.assertIsNone(self.storage.add_file_by('user1', '/super/secret/file.txt', 200))
        self.assertIsNone(self.storage.add_file_by('non-existed', '/super/secret/file.txt', 200))
        self.assertEqual(self.storage.get_file_size('/super/secret/file.txt'), 300)


    @timeout(0.4)
    def test_level_3_case_07_should_not_update_capacity_for_non_existing_user(self):
        self.assertTrue(self.storage.add_user('user1', 1000))
        self.assertIsNone(self.storage.update_capacity('user2', 5000))
        self.assertIsNone(self.storage.add_file_by('user1', '/file', 5000))
        self.assertTrue(self.storage.add_user('user2', 2000))
        self.assertIsNone(self.storage.add_file_by('user2', '/file', 5000))
        self.assertEqual(self.storage.add_file_by('user2', '/file', 2000), 0)
        self.assertIsNone(self.storage.update_capacity('non-existing-user', 1000))


    @timeout(0.4)
    def test_level_3_case_08_should_find_files_added_by_different_users(self):
        self.assertTrue(self.storage.add_user('user1', 1000))
        self.assertTrue(self.storage.add_user('user2', 2000))
        self.assertEqual(self.storage.add_file_by('user1', '/path/to/file.txt', 100), 900)
        self.assertEqual(self.storage.add_file_by('user2', '/path/to/another/file.txt', 200), 1800)
        self.assertEqual(self.storage.add_file_by('user1', '/path/file.txt', 200), 700)
        self.assertIsNone(self.storage.add_file_by('user2', '/path/to/file.txt', 300))
        expected = ['/path/to/another/file.txt(200)', '/path/to/file.txt(100)']
        self.assertEqual(self.storage.find_file('/path/to', 'file.txt'), expected)
        self.assertEqual(self.storage.add_file_by('user1', '/path/to/file3.txt', 300), 400)
        self.assertEqual(self.storage.add_file_by('user2', '/file.txt', 200), 1600)
        expected = ['/path/file.txt(200)', '/path/to/another/file.txt(200)', '/path/to/file.txt(100)']
        self.assertEqual(self.storage.find_file('/path', 'file.txt'), expected)
        self.assertEqual(self.storage.get_file_size('/path/file.txt'), 200)
        expected = ['/file.txt(200)', '/path/file.txt(200)', '/path/to/another/file.txt(200)', '/path/to/file.txt(100)']
        self.assertEqual(self.storage.find_file('/', 'file.txt'), expected)
        self.assertEqual(self.storage.get_file_size('/path/to/file.txt'), 100)


    @timeout(0.4)
    def test_level_3_case_09_should_calculate_remaining_capacity_properly(self):
        self.assertTrue(self.storage.add_user('client', 5555))
        self.assertEqual(self.storage.add_file_by('client', '/client_folder/very_large_file', 5500), 55)
        self.assertTrue(self.storage.add_file('/client_folder/admins_file', 55))
        self.assertEqual(self.storage.add_file_by('client', '/client_folder/small_file', 50), 5)
        self.assertIsNone(self.storage.add_file_by('client', '/client_folder/massive_file_which_does_not_fit', 3000))
        self.assertEqual(self.storage.add_file_by('client', '/client_folder/tiny_file', 5), 0)
        self.assertIsNone(self.storage.add_file_by('client', '/client_folder/super_tiny_file_but_it_does_not_fit', 1))
        self.assertIsNone(self.storage.get_file_size('/client_folder/super_tiny_file_but_it_does_not_fit'))
        self.assertEqual(self.storage.update_capacity('client', 5500), 1)
        self.assertIsNone(self.storage.add_file_by('client', '/client_folder/large_file_which_does_not_fit', 5499))
        self.assertEqual(self.storage.update_capacity('client', 5), 1)
        self.assertEqual(self.storage.get_file_size('/client_folder/tiny_file'), 5)
        self.assertIsNone(self.storage.add_file_by('client', '/client_folder/tiny_file', 5))


    @timeout(0.4)
    def test_level_3_case_10_mixed(self):
        self.assertTrue(self.storage.add_file('/path/to/file.txt', 1234))
        self.assertTrue(self.storage.add_file('/path/to/video.mp4', 12345))
        self.assertTrue(self.storage.add_user('mom', 5000))
        self.assertTrue(self.storage.copy_file('/path/to/video.mp4', '/mom/video.mp4'))
        self.assertTrue(self.storage.add_user('dad', 100000))
        self.assertEqual(self.storage.add_file_by('mom', '/mom/videos/video.mp4', 3500), 1500)
        self.assertFalse(self.storage.copy_file('/mom/videos/video.mp4', '/dad/video.mp4'))
        self.assertEqual(self.storage.get_file_size('/path/to/video.mp4'), 12345)
        self.assertEqual(self.storage.get_file_size('/mom/video.mp4'), 12345)
        expected = ['/mom/video.mp4(12345)', '/path/to/video.mp4(12345)', '/mom/videos/video.mp4(3500)']
        self.assertEqual(self.storage.find_file('/', 'video.mp4'), expected)
        self.assertEqual(self.storage.update_capacity('mom', 10000), 0)
        expected = ['/mom/video.mp4(12345)', '/path/to/video.mp4(12345)', '/mom/videos/video.mp4(3500)']
        self.assertEqual(self.storage.find_file('/', 'video.mp4'), expected)
        self.assertEqual(self.storage.update_capacity('mom', 2000), 1)
        expected = ['/mom/video.mp4(12345)', '/path/to/video.mp4(12345)']
        self.assertEqual(self.storage.find_file('/', 'video.mp4'), expected)
        self.assertEqual(self.storage.get_file_size('/mom/video.mp4'), 12345)
        self.assertIsNone(self.storage.add_file_by('mom', '/mom/videos/video.mp4', 2500))
        self.assertEqual(self.storage.add_file_by('mom', '/mom/videos/video.mp4', 2000), 0)
