from ddex import json_to_ddex

ddex = json_to_ddex(path="Audio.json")
ddex.assert_valid()

ddex.to_json(output_file="Audio_output.json")
