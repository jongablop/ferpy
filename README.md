# fer-py

A Python implementation of `fer`: Framework for Experimental Results. 

The aim of fer is to stablish a standard way of **collecting**, **treating**, and **sharing** the experimental results.

## A quick view on `fer`:

`fer` is divided in 4 Python files, which contain 7 Python classes.

- `main_objects.py`: `Register`, `Data`, `Parameter`, `Result`

- `spectrum.py`: `Spectrum`

- `measurement.py`: `Measurement`

- `experiment.py`: `Experiment`

The most relevant characteristics of each class are described below:

- `Register`
   
   It is the smallest unit of information that is considered in our framework. It consists on the following fields:

   - `name`
   - `description`
   - `units`
   - `setpoint`
   - `correct`
   - `axes`
   - `values`
   - `standard_uncertainty`

   This structure is really flexible, and has several advantages compared to previous approaches. Some ideas:

   - `name` and `description` are strings that help to identify the `Register`.

   - `correct` field is used to mark if a `Register` is wrong (a broken sensor,...).

   - `axes` is a list of `Data` objects, each of them corresponding to a coordinate in the configuration space of the `Register` (for example, if a spectrum is recorded at 200ºC and with the sample placed at 20º, those two would be two of the `Data` objects that are present in the `axes` field. The third one would be the spectral axis).

   - Note that this structure can be used represent raw data, fixed parameters that depend on the instrument's configuration, and even results derived from multiple measurements. (this is the elegant part, continue reading)

- `Data`, `Parameter`, `Result`

   These three classea are just a subclass of the class `Register`: they have the exact same fields (and methods) explained above, but each of them can also have their own fields and methods (see a small explanation [here](https://www.codesdope.com/course/python-subclass-of-a-class/)). In this case, there is not any additional field nor method. I created those subclasses just to have different names, so the code is easier to read and to understand.

   This approach solves some of the previous problems:

   - There is no difference between `Data` and `Parameter`.

   - It is easy to maintain.

- `Spectrum`

   This objects are used to represent a spectrum measured by the FTIR. I think that it could be a little bit more general, but this is our current approach:

   - `source_name`

   - `filename`

   - `start_datetime`

   - `end_datetime`

   - `scans`

   - `xpm_file`

   - `surface_temperature`

   - `surrounding_temperature`

   - `polarization`

   - `angle`

   - `signals`

- `Measurement`

    This object is used to represent a set of sample and calibration measurements that can be used to compute some physical property. It has the following fields:

    - `sample_name`

    - `start_datetime`

    - `end_datetime`

    - `parameters`

    - `sample_spectra`

    - `calibration_spectra`

    Having just a few fields makes it easy to maintain. `sample_spectra` and `calibration_spectra` are just lists of `Spectrum` objects. `parameters` is a list of `Parameter` objects.

    This approach is much more general than the previous ones, as there is no reference to our instrument.

- `Experiment`

    This object is used to represent an experiment: its measurements and the results derived from them.

    - `sample_name`

    - `description`

    - `experiment_authors`

    - `publication_bibtex`

    - `measurement`

    - `results`

    Initially is designed to hold the results for a single sample, I'm not sure if it should contain multiple samples in a single file.


## How to install and use it

Using `fer` is really straigthforward:

1. Clone the repository:
   ```
   git clone https://github.com/jongablop/fer-py.git
   ```

2. Get into the folder:
   ```
   cd fer-pyv
   ```

3. Install the requirements via `pip`:
   ```
   pip install -r requirements.txt
   ```

4. Now you can work with the Python files defined at `src`.

## Examples

### Basic usage: How to add some results without raw data or methods

This simple example shows how to create a `Experiment` object that contains the results from a spectral and directional emissivity experiment.

```
from main_objects import Data, Result
from experiment import Experiment

temperature_axis = Data().from_dict({
    "name": "surface_temperature",
    "description": "temperature measurement",
    "units": "Celsius",
    "setpoint": 100,
    "correct": True,
    "axes": [],
    "values": 104.23,
    "standard_uncertainty": 2.2
})

angles = range(10, 90, 10)
angle_axes = []

data_dict = {
    0: [0.85, 0.78, 0.72, 0.67, 0.63, 0.60, 0.57, 0.54, 0.51, 0.48, 0.45],
    1: [0.82, 0.75, 0.69, 0.64, 0.60, 0.57, 0.54, 0.51, 0.48, 0.45, 0.42],
    2: [0.88, 0.82, 0.76, 0.70, 0.65, 0.61, 0.58, 0.55, 0.52, 0.49, 0.46],
    3: [0.79, 0.73, 0.67, 0.62, 0.58, 0.54, 0.51, 0.48, 0.45, 0.42, 0.39],
    4: [0.76, 0.71, 0.66, 0.61, 0.57, 0.53, 0.50, 0.47, 0.44, 0.41, 0.38],
    5: [0.92, 0.86, 0.81, 0.76, 0.72, 0.68, 0.65, 0.62, 0.59, 0.56, 0.53],
    6: [0.70, 0.65, 0.61, 0.57, 0.54, 0.51, 0.48, 0.45, 0.42, 0.39, 0.36],
    7: [0.81, 0.76, 0.71, 0.67, 0.63, 0.59, 0.56, 0.53, 0.50, 0.47, 0.44]
}


results = []

for i, angle in enumerate(angles):

    angle_axis = Data().from_dict(
        {
        "name": "angle",
        "description": "sample orientation",
        "units": "",
        "setpoint": angle,
        "correct": True,
        "axes": [],
        "values": angle,
        "standard_uncertainty": 0.1
        }
    )

    result_1 = Result(
        name = "Spectral emissivity",
        description = "IR emissivity (mock example)",
        units = "",
        values = data_dict.get(i),
        axes = [
            temperature_axis,
            angle_axis,
            Data(
                name="spectral axis",
                description="",
                units="microns",
                correct=True,
                values=[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
            )
        ],
        standard_uncertainty=[0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02],
        correct = True
    )

    results.append(result_1)

experiment = Experiment(
    sample_name = "Aluminum",
    description = """
        Emissivity measurements were conducted on an aluminum sample at a temperature of 100°C. The sample was evaluated at 8 different angles ranging from 10 to 80 degrees. The spectral emissivity data was recorded over a range of wavelengths from 2 to 14 microns. The measurements provide insights into the sample's behavior in response to varying angles and wavelengths, contributing to our understanding of its thermal properties and potential applications.
    """,
    experiment_authors = ["Dr. Emily Smith"],
    publication_bibtex = '@article{smith2023emissivity, author = "Smith, Emily", title = "Emissivity Measurements of Aluminum Samples at Different Angles and Temperatures", journal = "Journal of Thermal Analysis", volume = "45", number = "3", pages = "321-335", year = "2023" }',
    measurement=None,
    results = results
)
```