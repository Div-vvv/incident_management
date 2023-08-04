import random
from django.utils import timezone


def fill_city_with_alternative(address):
    alternative_city_keys = ["county", "town", "village"]
    if "city" not in address:
        for alt_key in alternative_city_keys:
            if alt_key in address:
                address["city"] = address[alt_key]
                break
    return address


def generate_unique_incident_id():
    random_number = random.randint(10000, 99999)
    unique = []
    if random_number is not unique:
        unique.append(random)

    current_year = timezone.now().year
    incident_id = f"RMG{random_number}{current_year}"
    return incident_id
