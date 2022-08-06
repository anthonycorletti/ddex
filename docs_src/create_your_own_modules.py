from ddex import generate_ddex_module

generate_ddex_module(
    input_path="ern/42/release-notification.xsd",
    module_output_path="my.api.schemas.ern42",
)

# You can then import the module (my.api.schemas.ern42)
# and use it just like any other python module
