from datetime import datetime
from typing import Union, Optional

import ujson as json
import numpy as np
import pandas as pd
from main_objects import Data, Parameter, Result
from spectrum import Spectrum 
from measurement import Measurement

# Latest version: 20221611
# Some docs: https://docs.python.org/3/library/typing.html#typing.Optional
class Experiment:
    def __init__(
        self,
        sample_name: str = "",
        description: str = "",
        experiment_authors: Optional[list] = [],
        publication_bibtex: Optional[str] = "",
        measurement: Optional[Measurement] = None,
        results: Optional[list] = [],
    ):

        self.sample_name = sample_name
        self.description = description 
        self.experiment_authors = experiment_authors 
        self.publication_bibtex = publication_bibtex
        self.measurement = measurement
        self.results = results

    def get_sample_name(self):
        return self.sample_name

    def get_description(self):
        return self.description

    def get_publication_bibtex(self):
        return self.publication_bibtex

    def get_results(self):
        return self.results

    def to_dict(self):

        d = {}
        d["sample_name"] = self.sample_name
        d["description"] = self.description 
        d["experiment_authors"] = self.experiment_authors 
        d["publication_bibtex"] = self.publication_bibtex

        if type(self.measurement) == Measurement:
            d["measurement"] = self.measurement.to_dict()

        d["results"] = [result.to_dict() for result in self.results]

        return d

    def from_dict(self, d):

        self.sample_name = d.get("sample_name")
        self.description = d.get("description")
        self.experiment_authors = d.get("experiment_authors")
        self.publication_bibtex = d.get("publication_bibtex")

        self.measurement = Measurement().from_dict(d.get("measurement"))
        self.results = [Result().from_dict(dd) for dd in d.get("results")]

        return self
    
    def to_json(self):

        d = self.to_dict()
        return json.dumps(d, default=str)
    
    def get_result_names(self):

        all_names = []

        for result in self.get_results():
            all_names.append(result.get_name())

        return list(set(all_names))
    
    def filter_results(self, name):

        results = []

        for result in self.get_results():

            if result.get_name() == name:
                results.append(result)

        return results
    
    def results_to_nested_dict(self):

        main_dict = {}

        results_names = self.get_result_names()

        for result_name in results_names:

            d = {}
            list_axis = {}

            results = self.filter_results(name = result_name)

            for result in results:

                temp_d = {}

                temp_d.setdefault("sample", []).append(self.get_sample_name())
                temp_d.setdefault("property", []).append(result.get_name())

                for axis in result.get_axes():
                    
                    if type(axis.get_values()) == list: # this is a spectral axis

                        list_axis[axis.get_name()] = len(axis.get_values())

                        for v in axis.get_values():
                            temp_d.setdefault(axis.get_name(), []).append(v)
                    else:
                        temp_d.setdefault(axis.get_name(), []).append(axis.get_values())

                # now find the longest axis and repeat the other values to match its length
                longest_key = max(temp_d, key=lambda key: len(temp_d[key]))
                max_length = len(temp_d[longest_key])

                for key, value in temp_d.items():
                    if len(value) < max_length:
                        repetitions = int(max_length // len(value))
                        remaining = int(max_length % len(value))
                        repeated_values = value * int(repetitions) + value[:remaining]
                        temp_d[key] = repeated_values

                temp_d["value"] = result.get_values()
                print(temp_d["value"]) 
                for key, value in temp_d.items():
                    for val in value:
                        d.setdefault(key, []).append(val)

            for k, v in d.items():
                print(k, len(v))

            main_dict[result_name] = d

        return main_dict
        
    def results_to_dataframe_dict(self):

        d = self.results_to_nested_dict()
        sample_name = self.get_sample_name()
        result_dict = {}

        for property, dd in d.items():
            name_list = sample_name.split() + property.split()
            name = '_'.join(name_list)
            result_dict[name] = pd.DataFrame(dd)

        return result_dict
    
    def results_to_single_dataframe(self):

        dataframes = list(self.results_to_dataframe_dict().values())
        df = pd.concat(dataframes, ignore_index=True)   

        return df  
    
    def write_results_to_single_csv(self):

        df = self.results_to_single_dataframe()
        filename = self.get_sample_name() + '.csv'

        df.to_csv(filename, index=False)

    def write_results_to_csv(self):

        d = self.results_to_dataframe_dict()

        for name, dataframe in d.items():

            filename =  name + '.csv'
            dataframe.to_csv(filename, index=False)

        

if __name__ == '__main__':
    experiment = Experiment()