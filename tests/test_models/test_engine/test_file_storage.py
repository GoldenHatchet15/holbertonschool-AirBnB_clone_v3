import unittest
from models import storage
from models.state import State


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.state = State(name="New York")
        self.state.save()

    def tearDown(self):
        """Tear down test environment"""
        storage.delete(self.state)

    def test_get_existing_object(self):
        """Test retrieval of an existing object"""
        retrieved = storage.get(State, self.state.id)
        self.assertEqual(retrieved.id, self.state.id)

    def test_get_non_existing_object(self):
        """Test retrieval of a non-existing object"""
        self.assertIsNone(storage.get(State, "nonexistent_id"))

    def test_count_specific_class(self):
        """Test count of objects for a specific class"""
        initial_count = storage.count(State)
        new_state = State(name="California")
        new_state.save()
        self.assertEqual(storage.count(State), initial_count + 1)
        storage.delete(new_state)

    def test_count_all_classes(self):
        """Test count of all objects"""
        initial_count = storage.count()
        new_state = State(name="California")
        new_state.save()
        self.assertEqual(storage.count(), initial_count + 1)
        storage.delete(new_state)


if __name__ == '__main__':
    unittest.main()
