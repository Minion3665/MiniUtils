"""
A module to more easily handle JSON than the python default JSON implementation

This module is simply a wrapper around the python JSON implementation so that repeating lots of code is not needed each time reading/writing from JSON is required
"""
import json
import typing


class Json:
    """
    The base JSON class, representing a JSON file
    """
    def __init__(self, file: str):
        """
        :arg file: Specify the file that you would like to read JSON from. Files have data/ prepended and .json appended so there is no need for you to include those
        :type file str:
        """
        self.file = "data/" + file + ".json"

    def load_data(self):
        """
        Load your JSON file as a python object

        :returns: Your JSON, defaults to an empty dict if there is no JSON
        :rtype: str, int, float, long, dict, list, bool, type(None)
        """
        try:
            with open(self.file) as data_file:
                return json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self, dictionary: typing.Union[str, int, float, dict, list, bool, type(None)]):
        """
        Overwrite your JSON dictionary with new data

        :param dictionary: Specify the dictionary (or other object) that you would like to overwrite the JSON with
        :type dictionary: str, int, float, long, dict, list, bool, type(None)
        """
        with open(self.file, "w") as data_file:
            json.dump(dictionary, data_file)

    def read_key(self, key):
        """
        Load your JSON key as a python object

        :param key: Specify the key that you would like to look at
        :type key: str

        :returns: Your JSON key, defaults to an empty dict if there is no JSON
        :rtype: str, int, float, long, dict, list, bool, type(None)
        """
        try:
            return self.load_data()[str(key)]
        except KeyError:
            return None

    def save_key(self, key, value):
        """
        Overwrite your JSON key with new data

        :param key: Specify the key that you would like to overwrite
        :type key: str

        :param value: Specify the dictionary (or other object) that you would like to overwrite the JSON with
        :type value: str, int, float, long, dict, list, bool, type(None)
        """
        json_data = self.load_data()
        json_data[str(key)] = value
        self.save_data(json_data)
        return json_data

    def remove_key(self, key):
        """
        Delete your key from the JSON

        :param key: The key you would like to delete
        :type key: str
        """
        json_data = self.load_data()
        removed = None
        try:
            removed = json_data.pop(str(key))
            self.save_data(json_data)
        except KeyError:
            pass
        return removed
