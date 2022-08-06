## XML Support

As you probably already know, DDEX relies heavily on XML.

This package is a lightweight, generic module you can use to easily create and validate DDEX XML documents – for any schema that python can parse.

For example, we can create a DDEX XML document from a Python object:

```Python
{!../docs_src/generate_simple_ddex_document.py!}
```

Schemas can be automatically generated or can be manually submitted.

```Python
{!../docs_src/generate_xml_schema_and_document.py!}
```

## JSON Support

```Python
{!../docs_src/generate_xml_schema_and_document_from_json.py!}
```

## Creating your own python modules

You might also find it useful to create your own modules for DDEX objects.

It's not a great idea to constantly load and create DDEX objects, for one reason that they don't change often, and secondly because you can save lots of time and work by not constantly downloading files.

```Python
{!../docs_src/create_your_own_modules.py!}
```

&nbsp;

&nbsp;
