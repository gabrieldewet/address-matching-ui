from attrs import define, field
from Levenshtein import distance, editops, ratio


@define
class Address:
    raw_text: str = ""
    street_name: str = ""
    street_number: str = ""
    box_number: str = ""
    zipcode: str = ""
    city: str = ""
    country: str = ""

    def update_field(self, field_name: str, value: str):
        """Update a specific field in the address"""
        if hasattr(self, field_name):
            setattr(self, field_name, value)
            if field_name != "raw_text":
                self.update_raw_text()
            else:
                self.udpate_address_fields()

    def update_raw_text(self) -> str:
        """Convert structured fields to raw text"""
        parts = [self.street_name, self.street_number]
        if self.box_number:
            parts[1] += f"/{self.box_number}"
        parts += [self.zipcode, self.city, self.country]
        self.raw_text = " ".join(part for part in parts if part)

    def udpate_address_fields(self):
        parts = [p.strip() for p in self.raw_text.replace(",", " ".replace("/", " ")).split()]

        # Try to extract parts in expected order
        if len(parts) >= 1:
            self.street_name = parts[0]
        if len(parts) >= 2:
            self.street_number = parts[1]
        if len(parts) >= 6:  # If we have all fields including box number
            self.box_number = parts[2]
            self.zipcode = parts[3]
            self.city = parts[4]
            self.country = parts[5]
        elif len(parts) >= 5:  # If we have all fields except box number
            self.zipcode = parts[2]
            self.city = parts[3]
            self.country = parts[4]


@define
class FieldComparison:
    value_left: str
    value_right: str
    lev_similarity: float = field(init=False)
    lev_distance: int = field(init=False)
    lev_edit_ops: list = field(init=False)

    def __attrs_post_init__(self):
        """Calculate Levenshtein similarity, distance, and edit operations"""
        self.lev_distance = distance(self.value_left, self.value_right)
        self.lev_similarity = ratio(self.value_left, self.value_right)
        self.lev_edit_ops = editops(self.value_left, self.value_right)


@define
class AddressComparison:
    address1: Address = field()
    address2: Address = field()
    results: dict[str, FieldComparison] = field(init=False)

    def __attrs_post_init__(self):
        self.similarity_ratios = compare_addresses(self.address1, self.address2)


def compare_addresses(addr1: Address, addr2: Address) -> dict[str, FieldComparison]:
    """Compare two addresses and return similarity ratios for each field"""
    return {
        "raw_text": FieldComparison(addr1.raw_text, addr2.raw_text),
        "street_name": FieldComparison(addr1.street_name, addr2.street_name),
        "street_number": FieldComparison(addr1.street_number, addr2.street_number),
        "box_number": FieldComparison(addr1.box_number, addr2.box_number),
        "zipcode": FieldComparison(addr1.zipcode, addr2.zipcode),
        "city": FieldComparison(addr1.city, addr2.city),
        "country": FieldComparison(addr1.country, addr2.country),
    }
