from ddex import load_ddex_xsd_schema, xml_to_ddex

schema = load_ddex_xsd_schema(path="release-notification.xsd")
ddex = xml_to_ddex(path="Audio.xml", schema=schema)

ddex.assert_valid()
