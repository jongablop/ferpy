from typing import Union, Optional
import numpy as np

# Latest version: 20221611
# Some docs: https://docs.python.org/3/library/typing.html#typing.Optional

def numpy_to_python(np_object):
    """This function converts a numpy array to a python list.

    Args:
        np_object (np.array): a np.array.

    Returns:
        list: the np.array converted to a python list.
    """

    if type(np_object) == np.array:
        return [val.item() for val in np_object]
    
    else:
        return np_object.item()

class Register:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        units: str = "",
        setpoint: Optional[float] = None,
        values: Union[int, float, list[int], list[float]] = [],
        axes: list = [],
        standard_uncertainty: Union[int, float, list[int], list[float]] = [],
        correct: Optional[bool] = True,
    ):
        """_summary_

        Args:
            name (str, optional): _description_. Defaults to "".
            description (str, optional): _description_. Defaults to "".
            units (str, optional): _description_. Defaults to "".
            setpoint (Optional[float], optional): _description_. Defaults to None.
            values (Union[int, float, list[int], list[float]], optional): _description_. Defaults to [].
            axes (list, optional): _description_. Defaults to [].
            standard_uncertainty (Union[int, float, list[int], list[float]], optional): _description_. Defaults to [].
            correct (Optional[bool], optional): _description_. Defaults to True.
        """

        self.name = name 
        self.description = description
        self.units = units 
        self.setpoint = setpoint
        self.correct = correct
        self.axes = axes
        self.standard_uncertainty = standard_uncertainty
        # self.last_revision
        # self.changelog

        if type(values) == np.ndarray:
            self.values = [val.item() for val in values]

        else:
            try:
                self.values = values.item()
            except:
                self.values = values

    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["description"] = self.description 
        d["units"] = self.units 
        d["setpoint"] = self.setpoint
        d["correct"] = self.correct

        if type(self.axes) == list:
            d["axes"] = [axis.to_dict() for axis in self.axes]

        d["values"] = self.values
        d["standard_uncertainty"] = self.standard_uncertainty

        return d
    
    def from_dict(self, d):
        self.name = d.get("name")
        self.description = d.get("description")
        self.units = d.get("units")
        self.setpoint = d.get("setpoint")
        self.correct = d.get("correct")
        self.axes = d.get("axes")
        self.values = d.get("values")
        self.standard_uncertainty = d.get("standard_uncertainty")

        return self
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_setpoint(self):
        return self.setpoint
    
    def get_values(self):
        return self.values
    
    def get_units(self):
        return self.units
    
    def get_standard_uncertainty(self):
        return self.standard_uncertainty
    
    def get_axes(self):
        return self.axes
    
    def get_axis(self):
        return self.get_axes[0]
    
    def is_correct(self):
        return self.correct
    
    def set_values(self, new_values):
        if type(new_values) == np.ndarray:
            self.values = [val.item() for val in new_values]

        else:
            try:
                self.values = new_values.item()
            except:
                self.values = new_values
    
class Data(Register):
    pass

    def get_sensor_name(self):
        return super().get_name()
    
class Parameter(Register):
    pass
    

class Result(Register):
    pass
    

    
if __name__ == '__main__':
    pass