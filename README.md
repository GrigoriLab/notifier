# Notifier
The purpose of this module is to provide a way to notify an external API when something of interest has happened in our system.

When something changes (any change) on any supported entity - this module gets used.

## Installation
* ``pip install git+https://git@github.com/grigorilab/notifier.git``


## Run test
```bash
python -m unittest discover notifier
```

## Example
```python
from notifier import Company, MyObserver

company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")
company.attach(MyObserver())
company.employees_min = 0
company.is_deleted = True
```
This snippet should notify to API about Company creation and `is_deleted` field change.
