from ddex import xml_to_ddex

ddex = xml_to_ddex(path="Audio.xml")
ddex.assert_valid()
