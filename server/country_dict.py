import json
import os
from pathlib import Path


# define a class to store all of our dictionaries
class countries():
    def __init__(self):
        # read the JSON
        with open(os.path.join(Path(__file__).parent, "data.json")) as json_file:
            json_dict = json.load(json_file)

        self.all = {}

        for i in range(len(json_dict)):
            self.all[json_dict[i]["countryName"]] = country(json_dict[i]["countryCode"],
                                                            json_dict[i]["countryName"],
                                                            json_dict[i]["currencyCode"])

# define a class to store a single country


class country():
    def __init__(self, code, name, curr):
        self.code = code
        self.name = name
        self.curr = curr
