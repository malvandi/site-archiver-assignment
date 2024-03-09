import json
from typing import Dict

from model.metadata import Metadata, metadata_encoder, metadata_decoder


class JsonDB:
    filename: str

    def __init__(self, directory: str):
        self.filename = directory

    def read_json(self) -> Dict[str, Metadata]:
        """Reads data from a JSON file and returns it as a Python dictionary."""
        try:
            with open(self.filename, 'r') as file:
                print('Im here')
                data = json.load(file, object_hook=metadata_decoder)
                print('Im here, after')
        except FileNotFoundError:
            data = {}
        return data

    def write_json(self, data: Dict[str, Metadata]):
        """Writes data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4, default=metadata_encoder)

    def add_record(self, record: Metadata):
        """Adds a new record to the JSON file."""
        data = self.read_json()
        data[record.url] = record
        self.write_json(data)

    def delete_record(self, key: str):
        """Deletes a record from the JSON file."""
        data = self.read_json()
        if key in data:
            del data[key]
            self.write_json(data)
            print("Record deleted successfully.")
        else:
            print("Record with key '{}' not found.".format(key))

    def update_record(self, new_record: Metadata):
        """Updates an existing record in the JSON file."""
        data = self.read_json()
        data[new_record.url] = new_record
        self.write_json(data)
