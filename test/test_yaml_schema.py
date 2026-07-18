import pathlib
from PixieDust.utils.schema import Schema


def test_load_schema_from_yaml():
    yaml_path = pathlib.Path(__file__).parent / "sample_schema.yaml"
    schema = Schema.load_from_yaml(yaml_path)

    assert schema.name == "Demo Schema"
    assert len(schema.fields) == 6

    # Verify field names and types
    assert schema.fields[0].name == "Magic"
    assert schema.fields[0].type == "uint32"

    assert schema.fields[1].name == "Version"
    assert schema.fields[1].type == "uint16"

    assert schema.fields[2].name == "Flags"
    assert schema.fields[2].type == "uint8"

    assert schema.fields[3].name == "Negative"
    assert schema.fields[3].type == "int8"

    assert schema.fields[4].name == "Offset"
    assert schema.fields[4].type == "uint32"

    assert schema.fields[5].name == "Size"
    assert schema.fields[5].type == "uint32"
