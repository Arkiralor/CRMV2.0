from django.core.validators import RegexValidator

PHONE_VALID = RegexValidator(r'^([0-9]){10}', "Phone number invalid.")

PIN_VALID = RegexValidator(r'^([0-9]){6}', 'Pincode Invalid')