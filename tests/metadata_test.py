from mastrsql.metadata import metadata_dict

def test_metadatadict():
    assert type(metadata_dict)==dict
    assert type(metadata_dict["einheitensolar"])==dict
