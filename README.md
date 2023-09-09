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

## How to contribute

