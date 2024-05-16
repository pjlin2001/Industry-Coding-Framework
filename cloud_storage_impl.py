from cloud_storage import CloudStorage


class CloudStorageImpl(CloudStorage):


    def __init__(self):
        self.storage = {}
        self.users = {'admin': {'capacity': float('inf'), 'used': 0}}
        self.file_ownership = {}


    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False
        self.users[user_id] = {'capacity': capacity, 'used': 0}
        return True
       
    def add_file(self, name: str, size: int) -> bool:
        return self.add_file_by('admin', name, size) is not None


    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        if user_id not in self.users or name in self.storage:
            return None
        user = self.users[user_id]
        if user['used'] + size > user['capacity']:
            return None
        self.storage[name] = size
        self.file_ownership[name] = user_id
        user['used'] += size
        return user['capacity'] - user['used']


    def copy_file(self, name_from: str, name_to: str) -> bool:
        if name_from not in self.storage or name_to in self.storage:
            return False
        owner_id = self.file_ownership[name_from]
        owner = self.users[owner_id]
        if owner['used'] + self.storage[name_from] > owner['capacity']:
            return False
        self.storage[name_to] = self.storage[name_from]
        self.file_ownership[name_to] = owner_id
        owner['used'] += self.storage[name_from]
        return True
       
    def update_capacity(self, user_id: str, capacity: int) -> int | None:
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        current_capacity = user['used']
        if current_capacity <= capacity:
            user['capacity'] = capacity
            return 0
        files_owned = [(name, size) for name, size in self.storage.items() if self.file_ownership[name] == user_id]
        files_owned.sort(key=lambda x: (-x[1], x[0]))
        files_removed = 0
        while current_capacity > capacity and files_owned:
            name, size = files_owned.pop(0)
            current_capacity -= size
            del self.storage[name]
            del self.file_ownership[name]
            files_removed += 1
            if current_capacity <= capacity:
                break
        user['capacity'] = capacity
        user['used'] = current_capacity
        return files_removed




    def get_file_size(self, name: str) -> int | None:
        return self.storage.get(name)


    def find_file(self, prefix: str, suffix: str) -> list[str]:
        matching_files = [(name, size) for name, size in self.storage.items() if name.startswith(prefix) and name.endswith(suffix)]
        matching_files.sort(key=lambda x: (-x[1], x[0]))
        return [f"{name}({size})" for name, size in matching_files]


    def compress_file(self, user_id: str, name: str) -> int | None:
        if user_id not in self.users or name not in self.storage or self.file_ownership[name] != user_id:
            return None
        compressed_name = name + '.COMPRESSED'
        if compressed_name in self.storage:
            return None
        file_size = self.storage[name]
        compressed_size = file_size // 2
        del self.storage[name]
        self.storage[compressed_name] = compressed_size
        self.file_ownership[compressed_name] = user_id
        self.users[user_id]['used'] += (compressed_size - file_size)
        return self.users[user_id]['capacity'] - self.users[user_id]['used']
       
    def decompress_file(self, user_id: str, name: str) -> int | None:
        if user_id not in self.users or name not in self.storage or not name.endswith('.COMPRESSED'):
            return None
        original_name = name[:-11]
        if original_name in self.storage or self.file_ownership[name] != user_id:
            return None
        compressed_size = self.storage[name]
        original_size = compressed_size * 2
        if self.users[user_id]['used'] + original_size - compressed_size > self.users[user_id]['capacity']:
            return None
        del self.storage[name]
        self.storage[original_name] = original_size
        self.file_ownership[original_name] = user_id
        self.users[user_id]['used'] += (original_size - compressed_size)
        return self.users[user_id]['capacity'] - self.users[user_id]['used']
