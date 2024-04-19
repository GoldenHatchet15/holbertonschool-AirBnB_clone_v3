import unittest
from models import storage
from models.state import State


class TestDBStorage(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.state = State(name="New York")
        self.state.save()
        self.assertIsNotNone(self.state.id, "ID was not assigned upon saving.")


    def tearDown(self):
        """Tear down test environment"""
        storage.delete(self.state)


    def test_get_existing_object(self):
        """Test retrieval of an existing object"""
        obj = State(name="New York")
        storage.new(obj)
        storage.save()
        retrieved = storage.get(State, obj.id)
        self.assertEqual(retrieved, obj)


    def test_get_non_existing_object(self):
        """Test retrieval of a non-existing object"""
        self.assertIsNone(storage.get(State, "nonexistent_id"))


    def test_count_specific_class(self):
        """Test count of objects for a specific class"""
        initial_count = storage.count(State)
        obj = State(name="California")
        storage.new(obj)
        storage.save()
        self.assertEqual(storage.count(State), initial_count + 1)


    def test_count_all_classes(self):
        """Test count of all objects"""
        initial_count = storage.count()
        obj = State(name="California")
        storage.new(obj)
        storage.save()
        self.assertEqual(storage.count(), initial_count + 1)

        
if __name__ == '__main__':
    unittest.main()
