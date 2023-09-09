from datetime import datetime
from typing import Union, Optional

import json
import numpy as np
import pandas as pd
from main_objects import Data, Parameter, Result
from spectrum import Spectrum

# Latest version: 20221611
# Some docs: https://docs.python.org/3/library/typing.html#typing.Optional
class Measurement:
    def __init__(
        self,
        sample_name: Optional[str] = '',
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        parameters: Union[None, list[Parameter]] = [],
        samples: Optional[list] = [],
        calibration: Optional[list] = []
    ):

        self.sample_name = sample_name
        self.start_datetime = start_datetime 
        self.end_datetime = end_datetime 
        self.parameters = parameters
        self.sample_spectra = samples
        self.calibration_spectra = calibration

    def get_calibration_sources(self):

        all_names = []

        for spectrum in self.calibration_spectra:
            all_names.append(spectrum.get_source_name())

        return list(set(all_names))

    def filter_calibration(self, name):

        result = []

        for spectrum in self.calibration_spectra:
            if name == spectrum.get_source_name():
                result.append(spectrum)

        return result

    def calibration_to_dict(self):

        result = {}

        for name in self.get_calibration_sources():
            result[name] = self.filter_calibration(name)

        return result

    def get_sample_sources(self):

        all_names = []

        for spectrum in self.sample_spectra:
            all_names.append(spectrum.get_source_name())

        return list(set(all_names))

    def filter_sample(self, name):

        result = []

        for spectrum in self.sample_spectra:
            if name == spectrum.get_source_name():
                result.append(spectrum)

        return result

    def samples_to_dict(self):

        result = {}

        for name in self.get_sample_sources():
            result[name] = self.filter_sample(name)

        return result


    def to_dict(self, sample_temperature_setpoint=None):
        
        d = {}
        
        d["sample_name"] = self.sample_name
        d["start_datetime"] = self.start_datetime
        d["end_datetime"] = self.end_datetime
        
        if self.parameters != None:
            d["parameters"] = [parameter.to_dict() for parameter in self.parameters]

        if self.calibration_spectra != None:
            # d["calibration_spectra"] = self.calibration_to_dict()
            d["calibration"] = [calibration.to_dict() for calibration in self.calibration_spectra]

        if self.sample_spectra != None:
            # d["sample"] = self.samples_to_dict() 
            d["sample"] = [sample.to_dict() for sample in self.sample_spectra]

        return d
    
    def from_dict(self, d):

        self.sample_name = d.get("sample_name")
        self.start_datetime = d.get("start_datetime")
        self.end_datetime = d.get("end_datetime")

        self.parameters = [Parameter().from_dict(dd) for dd in d.get("parameters")]
        self.calibration = [Spectrum().from_dict(dd) for dd in d.get("calibration")]
        self.sample_spectra = [Spectrum().from_dict(dd) for dd in d.get("sample")]

        return self

    def to_json(self, sample_temperature_setpoint=None):
        
        d = self.to_dict(sample_temperature_setpoint)
        
        return json.dumps(d, default=str)

    def add_calibration_spectrum(self, spectrum):
        self.calibration_spectra.append(spectrum)

    def add_sample_spectrum(self, spectrum):
        self.sample_spectra.append(spectrum)

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def get_sample_name(self):

        if self.sample_name == None:
            return ""

        else:
            return self.sample_name

if __name__ == '__main__':
    m = Measurement()