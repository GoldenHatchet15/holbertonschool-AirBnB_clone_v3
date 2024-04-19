#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        cls_name = cls.__name__
        dct = {}
        for key in self.__objects.keys():
            if key.split('.')[0] == cls_name:
                dct[key] = self.__objects[key]
        return dct

    def new(self, obj):
        """Add the object to the storage dictionary."""
        # Ensure the object has an ID
        if obj.id is None:
            raise ValueError("Object ID cannot be None")
        # Generate a key based on the object's class and ID
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj  # Store the object using the generated key



    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        ''' deletes the object obj from the attribute
            __objects if it's inside it
        '''
        if obj is None:
            return
        obj_key = obj.to_dict()['__class__'] + '.' + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]

    def get(self, cls, id):
        """Retrieve one object based on class and its ID."""
        if cls and id:
            # Construct the key using the class and id
            key = f"{cls.__name__}.{id}"
            return self.__objects.get(key, None)
        return None

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class."""
        if cls:
            # Count objects of the given class
            cls_name = cls.__name__
            return sum(1 for obj in self.__objects.values()
                       if obj.__class__.__name__ == cls_name)
        else:
            # Count all objects
            return len(self.__objects)

    def close(self):
        """Call the reload method"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object based on class and its ID."""
        if cls and id:
            # Construct the key using the class and id
            key = f"{cls.__name__}.{id}"
            return self.__objects.get(key, None)
        return None
    
    def count(self, cls=None):
        """Count the number of objects in storage matching the given class."""
        if cls:
            # Count objects of the given class
            cls_name = cls.__name__
            return sum(1 for obj in self.__objects.values()
                       if obj.__class__.__name__ == cls_name)
        else:
            # Count all objects
            return len(self.__objects)
