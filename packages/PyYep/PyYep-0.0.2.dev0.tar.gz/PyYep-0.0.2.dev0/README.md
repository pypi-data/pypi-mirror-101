# PyYep

PyYep is a python schema builder for value parsing and validation. Define a schema, transform a value to match and validate the inputs with existing validator or custom functions.

PyYep is heavily inspired by [Yup](https://github.com/jquense/yup)

[Docs](https://daniel775.github.io/PyYep/)

## Install

```sh
pip install PyYep
```


## Usage

You define and create schema objects with its inputs and validation methods. Then use the verify method to check the schema. A ValidationError will be raised if some input value does not match the validation.

```python
from PyYep import Schema, InputItem, ValidationError

schema = Schema([
	InputItem('name', input_object, 'path-to-input_object-value-property-or-method').string().email(),
	InputItem('name', input_object, 'path-to-input_object-value-property-or-method').number().min(10).max(100),
], abort_early=False) 

// check validity

try:
	result = schema.validate()
	# handle result
except ValidationError:
	# handle fail
```
