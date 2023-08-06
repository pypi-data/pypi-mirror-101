# Client library in1
This package allows querying Sobolt's in1 supersampling service from Python.

## How do I get set up as a user?
Install the package using pip: `pip install in1`. Then simply import the library's supersampling module and go wild!

```python
import in1

in1.sisr("path/to/sentinel2_raster.tif", "api-key-please-contact-us")
```
The Python client library also installs an in1 executable that allows super-resolving directly from the terminal.

```shell
in1 upsample --source path/to/source.tif --result path/to/result.tif --api <IN1_API_KEY>
```

## How do I get set up as an in1 developer?
From inside the `python-client-in1` directory install the package using pip: `pip
install -e .`  -- then import in1 to start using the super-sampling module (see _How do I
get set up as a user_).

Please install pre-commits to ensure consistent code on the repository. You can do so
using the command `pip install pre-commit && pre-commit install`
