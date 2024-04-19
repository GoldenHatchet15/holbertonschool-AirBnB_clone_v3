#!/usr/bin/python3
""" """
from models.base_model import BaseModel, Base
from datetime import datetime
import unittest
import time
from uuid import UUID
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'basemodel test not supported')
class test_basemodel(unittest.TestCase):
    """ test class for base_model class"""

    def __init__(self, *args, **kwargs):
        """ init the test class of basemodel"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ the set up method of the test class"""
        pass

    def tearDown(self):
        """the teardown method of the ctest class"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Tests the initialization of the model class.
        """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """ default testing of basemodel"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ testing basemodel with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ testing with kwargs again but with int kwargs"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save metthod"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ testing the str method of themodel"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """Testing the to_dict method."""
        mdl = self.value()
        mdl.id = 'u-b34'
        mdl.age = 13
        # Suppose mdl might also have a 'name' attribute
        mdl.name = "Example Name"
        dict_result = mdl.to_dict()

        expected_keys = {'id', 'created_at', 'updated_at', '__class__', 'age', 'name'}
        self.assertEqual(set(dict_result.keys()), expected_keys)
        self.assertEqual(dict_result['id'], 'u-b34')
        self.assertEqual(dict_result['age'], 13)
        self.assertEqual(dict_result['name'], "Example Name")
        self.assertIn('__class__', dict_result)
        self.assertIsInstance(dict_result['created_at'], str)
        self.assertIsInstance(dict_result['updated_at'], str)
        
        # Checking the datetime format
        try:
            datetime.fromisoformat(dict_result['created_at'])
            datetime.fromisoformat(dict_result['updated_at'])
        except ValueError:
            self.fail("created_at or updated_at time format is incorrect")

        # Specific class name test
        self.assertEqual(dict_result['__class__'], mdl.__class__.__name__)


    def test_kwargs_none(self):
        """ testing kwargs again with none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ testing kwargs with one arg"""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """ testing id attr of the model"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ testing created at attr"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Test that 'updated_at' is updated on model update"""
        model = BaseModel()
        old_updated_at = model.updated_at
        time.sleep(1)  # Sleep for a second
        model.name = "New Name"  # Modify the model
        model.save()  # Explicitly save to update the timestamp
        self.assertNotEqual(old_updated_at, model.updated_at, "updated")
