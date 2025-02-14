from src import fields
from src.serializers import BaseSerializer
from src.validators import MinMaxValueValidator


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
