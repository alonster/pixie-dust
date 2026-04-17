from PixieDust.schema.schema import Field, Schema


def test_field_size_uint32():
    field = Field("A", "uint32")
    assert field.size == 4

def test_field_size_int8():
    field = Field("A", "int8")
    assert field.size == 1


def test_schema_parse_little_endian():
    schema = Schema(name="test", fields=[
        Field("A", "uint32"),
        Field("B", "uint32")
    ])

    data = b"\x0b\x00\x00\x00" + b"\x12\x34\x56\x78"

    parsed = schema.parse(data)

    assert parsed["A"] == 11
    assert parsed["B"] == 0x78563412


def test_schema_parse_big_endian():
    schema = Schema(name="test", fields=[
        Field("A", "uint32", is_little_endian=False),
        Field("B", "uint32", is_little_endian=False)
    ])

    data = b"\x00\x00\x00\x0b" + b"\x12\x34\x56\x78"

    parsed = schema.parse(data)

    assert parsed["A"] == 11
    assert parsed["B"] == 0x12345678


def test_schema_parse_uint8_with_leftovers():
    schema = Schema(name="test", fields=[
        Field("A", "uint8")
    ])

    data = b"\x05" + b"\x00"

    parsed = schema.parse(data)

    assert parsed["A"] == 5


def test_schema_parse_uint32_with_not_enough_data():
    schema = Schema(name="test", fields=[
        Field("A", "uint32"),
        Field("B", "uint32")
    ])

    data = b"\x0b\x00\x00\x00" + b"\x12\x34\x56"

    parsed = schema.parse(data)

    assert parsed["A"] == 11
    assert parsed["B"] is None
