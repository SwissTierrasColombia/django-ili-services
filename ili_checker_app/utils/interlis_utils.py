import xml.etree.ElementTree as CET

TRANSFERFILE_MODELS_BLACKLIST = [
    "CHBaseEx_MapCatalogue_V1",
    "CHBaseEx_WaterNet_V1",
    "CHBaseEx_Sewage_V1",
    "CHAdminCodes_V1",
    "AdministrativeUnits_V1",
    "AdministrativeUnitsCH_V1",
    "WithOneState_V1",
    "WithLatestModification_V1",
    "WithModificationObjects_V1",
    "GraphicCHLV03_V1",
    "GraphicCHLV95_V1",
    "NonVector_Base_V2",
    "NonVector_Base_V3",
    "NonVector_Base_LV03_V3_1",
    "NonVector_Base_LV95_V3_1",
    "GeometryCHLV03_V1",
    "GeometryCHLV95_V1",
    "InternationalCodes_V1",
    "Localisation_V1",
    "LocalisationCH_V1",
    "Dictionaries_V1",
    "DictionariesCH_V1",
    "CatalogueObjects_V1",
    "CatalogueObjectTrees_V1",
    "AbstractSymbology",
    "CodeISO",
    "CoordSys",
    "GM03_2_1Comprehensive",
    "GM03_2_1Core",
    "GM03_2Comprehensive",
    "GM03_2Core",
    "GM03Comprehensive",
    "GM03Core",
    "IliRepository09",
    "IliSite09",
    "IlisMeta07",
    "IliVErrors",
    "INTERLIS_ext",
    "RoadsExdm2ben",
    "RoadsExdm2ben_10",
    "RoadsExgm2ien",
    "RoadsExgm2ien_10",
    "StandardSymbology",
    "StandardSymbology",
    "Time",
    "Units",
    # Hidden models from colombia
    "ISO19107_PLANAS_V3_0",
    "ISO19107_PLANAS_V3_1",
    "LADM_COL_v_4_0_1_Nucleo",
    "LADM_COL_V3_1",
    "LADM_COL_V3_0",
]


def get_xtf_models(xtf_path):
    """
    Get model names from an XTF file. Since XTF can be very large, we follow this strategy:
    1. Parse line by line.
        1.a. Compare parsed line with the regular expression to get the Header Section. (escape after 100 lines)
        1.b. If found, stop parsing the XTF file and go to 2. If not found, append the new line to parsed lines and go
            to next line.
    2. Give the Header Section to an XML parser and extract models. Note that we don't give the full XTF file to the XML
    parser because it will read it completely, which may be not optimal.
    :param xtf_path: Path to an XTF file
    :return: List of model names from the datafile
    """
    models = []

    # parse models from XTF
    start_string = "<HEADERSECTION"
    end_string = "</HEADERSECTION>"
    text_found = ""
    with open(xtf_path) as f:
        lines = ""
        for line_number, line in enumerate(f):
            lines += line
            start_pos = lines.find(start_string)
            end_pos = lines.find(end_string)
            if end_pos > start_pos:
                text_found = lines[start_pos : end_pos + len(end_string)]
                break
            if line_number > 100:
                break

    if text_found:
        try:
            root = CET.fromstring(text_found)
            element = root.find("MODELS")
            if element:
                for sub_element in element:
                    if (
                        "NAME" in sub_element.attrib
                        and sub_element.attrib["NAME"]
                        not in TRANSFERFILE_MODELS_BLACKLIST
                    ):
                        model = dict()
                        model["name"] = sub_element.attrib["NAME"]
                        models.append(model)
        except CET.ParseError as e:
            raise Exception(
                "Could not parse transferfile file `{file}` ({exception})".format(
                        file=xtf_path, exception=str(e)
                    )
            )
            
    return models
