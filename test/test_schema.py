from PixieDust.utils.schema import Field, Schema


class TestFieldSize:
    @staticmethod
    def test_uint32():
        field = Field("A", "uint32")
        assert field.size == 4

    @staticmethod
    def test_int8():
        field = Field("A", "int8")
        assert field.size == 1

    @staticmethod
    def test_string3():
        field = Field("A", "string3")
        assert field.size == 3


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
    def test_int8():
        schema = Schema(name="test", fields=[
            Field("A", "int8")
        ])

        data = b"\x05"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == 5

    @staticmethod
    def test_int8_negative():
        schema = Schema(name="test", fields=[
            Field("A", "int8")
        ])

        data = b"\xA0"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == 0xA0 - 256

    @staticmethod
    def test_string3():
        schema = Schema(name="test", fields=[
            Field("A", "string3")
        ])

        data = b"\x41\x62\x21"
        schema.parse(data)

        assert schema.fields[0].name == "A"
        assert schema.fields[0].value == "Ab!"

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
    def test_string3():
        f = Field("String", "string3", value="Ab!")
        assert f.format() == "'Ab!'"

    @staticmethod
    def test_none():
        f = Field("Empty", "uint8", value=None)
        assert f.format() == "-"

    @staticmethod
    def test_binary():
        f = Field("Binary", "binary", value=0x41)
        assert f.format() == "01000001"


class TestFieldUpdate:
    @staticmethod
    def test_update_uint8_decimal():
        f = Field("Test", "uint8")
        assert f.update_value_from_string("65") == b"A"

    @staticmethod
    def test_update_uint8_hex():
        f = Field("Test", "uint8")
        assert f.update_value_from_string("0x41") == b"A"

    @staticmethod
    def test_update_uint32_le():
        f = Field("Test", "uint32", is_little_endian=True)
        assert f.update_value_from_string("305419896") == b"\x78\x56\x34\x12"

    @staticmethod
    def test_update_binary():
        f = Field("Test", "binary")
        assert f.update_value_from_string("01000001") == b"A"


class TestFieldEditFormat:
    @staticmethod
    def test_edit_format_int():
        f = Field("Int", "uint8", value=12)
        assert f.edit_format() == "12"

    @staticmethod
    def test_edit_format_float():
        f = Field("Float", "float", value=3.14)
        assert f.edit_format() == "3.1400"

    @staticmethod
    def test_edit_format_string():
        f = Field("String", "string8", value="hello\x00\x00")
        assert f.edit_format() == "hello"

    @staticmethod
    def test_edit_format_binary():
        f = Field("Binary", "binary", value=0x41)
        assert f.edit_format() == "01000001"

    @staticmethod
    def test_edit_format_none():
        f = Field("Empty", "uint32", value=None)
        assert f.edit_format() == "-"
