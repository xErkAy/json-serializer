# JSON Serializer
### Inspired by Django Rest Framework serializers. Project is being made in education purposes


## Project uses:
* Ruff - a Python linter
* Mypy - a static type checker for Python
```
make check - check your project
make fmt - format your project
make lint - check & format your project
```

## An example
```python
import fields
from serializers import BaseSerializer
from validators import MinMaxValueValidator


class TestSerializer(BaseSerializer):
    id = fields.IntegerField()
    amount = fields.IntegerField(default=20, validators=[MinMaxValueValidator(12, 30)])
    full_name = fields.CharField(max_length=128)
    is_admin = fields.BooleanField(default=False)


if __name__ == "__main__":
    request_data = [
        {
            "id": 1,
            "amount": 220,
            "full_name": "Testinggg",
        },
        {
            "id": 2,
            "amount": 30,
            "full_name": "Testinggg",
            "is_admin": None,
        },
    ]
    validator = TestSerializer(data=request_data, many=True)
    validator.is_valid()
    print(validator.errors)
    print(validator.data)
```

```
{'amount': ValidationError('Value 220 is not in range from 12 to 30')}
[{'id': 1, 'full_name': 'Testinggg', 'is_admin': False}]
```
