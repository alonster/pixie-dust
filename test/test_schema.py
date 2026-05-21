from PixieDust.schema.schema import Field, Schema


class TestFieldSize:
    @staticmethod
    def test_uint32():
        field = Field("A", "uint32")
        assert field.size == 4

    @staticmethod
    def test_int8():
        field = Field("A", "int8")
        assert field.size == 1


class TestSchemaParse:
    @staticmethod
    def test_little_endian():
        schema = Schema(name="test", fields=[
            Field("A", "uint32"),
            Field("B", "uint32")
        ])

        data = b"\x0b\x00\x00\x00" + b"\x12\x34\x56\x78"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == 11

        assert schema.fields[1].name == "B"
        assert schema.fields[1].value == 0x78563412

    @staticmethod
    def test_big_endian():
        schema = Schema(name="test", fields=[
            Field("A", "uint32", is_little_endian=False),
            Field("B", "uint32", is_little_endian=False)
        ])

        data = b"\x00\x00\x00\x0b" + b"\x12\x34\x56\x78"
        schema.parse(data)

        assert schema.fields[1].name == "B"
        assert schema.fields[1].value == 0x12345678

    @staticmethod
    def test_uint8_with_leftovers():
        schema = Schema(name="test", fields=[
            Field("A", "uint8")
        ])

        data = b"\x05" + b"\x00"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == 5

    @staticmethod
    def test_uint32_with_not_enough_data():
        schema = Schema(name="test", fields=[
            Field("A", "uint32"),
            Field("B", "uint32")
        ])

        data = b"\x0b\x00\x00\x00" + b"\x12\x34\x56"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == 11

        assert schema.fields[1].name == "B"
        assert schema.fields[1].value is None


def test_schema_field_offsets():
    schema = Schema(name="test", fields=[
        Field("A", "uint32"),
        Field("B", "uint16"),
        Field("C", "uint8"),
    ])

    assert schema.fields[0].offset == 0
    assert schema.fields[0].name == "A"

    assert schema.fields[1].offset == 4
    assert schema.fields[1].name == "B"

    assert schema.fields[2].offset == 6
    assert schema.fields[2].name == "C"


class TestFieldFormat:
    @staticmethod
    def test_uint8():
        f = Field("Byte", "uint8", value=0x41)
        assert f.format() == "65 | 0x41"

    @staticmethod
    def test_int8():
        f = Field("Negative", "int8", value=-30)
        assert f.format() == "-30"

    @staticmethod
    def test_uint32():
        f = Field("Big Number", "uint32", value=0x12345678)
        assert f.format() == "305419896 | 0x12345678"

    @staticmethod
    def test_float():
        f = Field("Float", "float", value=3.14159)
        assert f.format() == "3.1416"

    @staticmethod
    def test_double():
        f = Field("Double", "double", value=3.14159)
        assert f.format() == "3.1416"

    @staticmethod
    def test_none():
        f = Field("Empty", "uint8", value=None)
        assert f.format() == "-"
