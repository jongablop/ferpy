from main_objects import Data
from datetime import datetime
from typing import Union, Optional
import numpy as np

class Spectrum:
    def __init__(
        self,
        source_name: str = "",
        filename: str = "",
        start_datetime: datetime = "",
        end_datetime: datetime = "",
        scans: int = 0,
        xpm_file: str = "",
        surface_temperature: list = [],
        surrounding_temperature: list = [],
        polarization: str = "",
        angle: Optional[Data] = None,
        signal: Optional[Data] = None
    ):

        self.source_name = source_name
        self.filename = filename
        self.start_datetime = start_datetime 
        self.end_datetime = end_datetime 
        self.scans = scans
        self.xpm_file = xpm_file 
        self.surface_temperature = surface_temperature 
        self.surrounding_temperature = surrounding_temperature 
        self.polarization = polarization
        self.angle = angle 
        
        self.signals = []

        # Signals are also stored in microns, because all the data processing is done in
        # those units

        signal_axis = signal.get_axis()
        microns_axis = Data(
            name = signal_axis.get_name(),
            description = signal_axis.get_description(),
            units = "microns",
            setpoint = signal_axis.get_setpoint(),
            values = np.divide(1_000, signal_axis.get_values())
        )
        
        signal_microns = Data(
            name = signal.get_name(),
            description = signal.get_description(),
            units = "",
            setpoint = signal.get_setpoint(),
            axes = [microns_axis],
            values = np.divide(np.multiply(10000, signal.get_values()), np.power(microns_axis.get_values(),2)),
            standard_uncertainty = signal.get_standard_uncertainty()
        )
        
        self.signals = [signal, signal_microns]

    def get_signals(self):
        return self.signals

    def filter_signal(self, space="lambda"):

        space_units_dict = {
            "lambda": "microns",
            "sigma": "cm-1"
        }

        units = space_units_dict.get(space)

        for signal in self.get_signals():

            if signal.get_units == units:
                return signal
        
    def get_source_name(self):
        return self.source_name
    
    def change_source_name(self, new_source_name):
        self.source_name = new_source_name
    
    def get_surface_setpoint(self):
        return float(self.surface_temperature[0].setpoint)
    
    def get_angle_setpoint(self):
        return float(self.angle.setpoint)
        
    def get_surface_temperatures(self):
        
        d = {}
        
        for temperature in self.surface_temperature:
        
            values = temperature.get_values()
            
            if len(values) != 0:
                mean = round(np.mean(values), 2)
        
            else:
                mean = np.nan
        
            d[temperature.sensor_name] = {
                'values': values,
                'mean': mean
            }
            
        return d
    
    def get_surrounding_temperatures(self):
        
        d = {}
        
        for temperature in self.surrounding_temperature:
        
            values = temperature.get_values()
        
            d[temperature.sensor_name] = {
                'values': values,
                'mean': round(np.mean(values), 2)
            }
            
        return d
    
    def set_temperature(self, sensor_name, new_temperatures):
        
        if self.surface_temperature != None:
            for temperature in self.surface_temperature:
                
                if temperature.get_sensor_name() == sensor_name:
                    if type(new_temperatures) != list:
                        new_temperatures = [new_temperatures]
                        
                    temperature.set_values(new_temperatures)
                    return True
            
        if self.surrounding_temperature != None:
            for temperature in self.surrounding_temperature:
                
                if temperature.get_sensor_name() == sensor_name:
                    temperature.set_values(new_temperatures)
                    return True
                
        return False
        
    def to_dict(self):

        d = {}

        d["source_name"] = self.source_name
        d["filename"] = self.filename
        d["start_datetime"] = self.start_datetime
        d["end_datetime"] = self.end_datetime
        d["scans"] = int(self.scans)
        d["xpm_file"] = self.xpm_file

        d["data"] = {}
        
        d["data"]["surface_temperature"] = [
            data.to_dict() for data in self.surface_temperature
        ]
        d["data"]["surrounding_temperature"] = [
            data.to_dict() for data in self.surrounding_temperature
        ]
        d["data"]["angle"] = self.angle.to_dict()
        d["data"]["signals"] = [
            data.to_dict() for data in self.signals
        ]

        return d
    
    def from_dict(self, d):

        self.sample_name = d.get("sample_name")
        self.filename = d.get("filename")
        self.start_datetime = d.get("start_datetime")
        self.end_datetime = d.get("end_datetime")
        self.scans = d.get("scans")
        self.xpm_file = d.get("xpm_file")

        if d["data"].get("surface_temperature") is not None:
            self.surface_temperature = [Data().from_dict(dd) for dd in d["data"].get("surface_temperatures")]
            
        if d["data"].get("surrounding_temperature") is not None:
            self.surrounding_temperature = [Data().from_dict(dd) for dd in d["data"].get("surrounding_temperature")]
            
        if d["data"].get("angle") is not None:
            self.angle = Data().from_dict(d["data"].get("angle"))
            
        if d["data"].get("signals") is not None:    
            self.surrounding_temperature = [Data().from_dict(dd) for dd in d["data"].get("signals")]
            
        return self
        
    def set_negative_signal(self, indexes):
        
        for i, space, data in enumerate(zip(["sigma", "lambda"], self.get_signals())):

            for j in range(len(data)):
                if j in indexes:
                    self.signals[i].values[j] = np.multiply(-1, np.abs(self.filter_signal(space=space)[j]))
                    
                else:
                    self.signals[i].values[j] = np.abs(self.filter_signal(space=space)[j])


    def set_positive_signal(self, indexes):
        
        for i, space, data in enumerate(zip(["sigma", "lambda"], self.get_signals())):

            for j in range(len(data)):
                if j in indexes:
                    self.signals[i].values[j] = np.abs(self.filter_signal(space=space)[j])
                    
                    
                else:
                    self.signals[i].values[j] = np.multiply(-1, np.abs(self.filter_signal(space=space)[j]))
