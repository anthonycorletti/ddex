<p align="center">
  <a href="https://ddex.corletti.xyz"><img src="https://ddex.net/wp-content/uploads/2018/10/ddex-logo-strapline-rgb.png" alt="DDEX"></a>
</p>
<p align="center">
    <em>A Python DDEX implementation.</em>
</p>
<p align="center">
<a href="https://github.com/anthonycorletti/ddex/actions?query=workflow%3Atest" target="_blank">
    <img src="https://github.com/anthonycorletti/ddex/workflows/test/badge.svg" alt="Test">
</a>
<a href="https://github.com/anthonycorletti/ddex/actions?query=workflow%3Apublish" target="_blank">
    <img src="https://github.com/anthonycorletti/ddex/workflows/publish/badge.svg" alt="publish">
</a>
<a href="https://codecov.io/gh/anthonycorletti/ddex" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/anthonycorletti/ddex?color=%2334D058" alt="Coverage">
</a>
</p>

---

**Documentation**: <a href="https://ddex.corletti.xyz" target="_blank">https://ddex.corletti.xyz</a>

**Source Code**: <a href="https://github.com/anthonycorletti/ddex" target="_blank">https://github.com/anthonycorletti/ddex</a>

---

A Python DDEX implementation.

Some tasty features are:

* **XML Support**: Create and validate DDEX XML documents.
* **JSON**: Transform DDEX documents to JSON documents and vice versa.
* **Python Objects**: Create and validate DDEX documents with python objects and vice versa.

## Requirements

Python 3.8+

## Installation

```sh
pip install ddex
```

## A Quick Example

```Python
from ddex import xml_to_ddex

ddex = xml_to_ddex(path="Audio.xml")
ddex.assert_valid()
```

## What is DDEX?

DDEX is a standard for the exchange of data between parties. Data specifically for digitial content supply chains. Think of it as the metadata standard for describing how digital content is distributed around to the services that supply the world with movies, music, and multimedia.

To learn more about DDEX, visit the following links:

- DDEX Website: [https://ddex.net](https://ddex.net)
- DDEX Knowledge Base: [https://kb.ddex.net](https://kb.ddex.net)
- DDEX XML Content Library: [http://service.ddex.net/xml/](http://service.ddex.net/xml/)

## So what can I do with this library?

Install it and use it in a server-side api for validating and creating DDEX documents and schemas, or for a batch processing service that's transforming data from one  multimedia metadata content standard to another. This library should support all DDEX content standards that python can parse.

## How can I help?

Please open an [issue](https://github.com/anthonycorletti/ddex/issues/new/choose) on GitHub. Pull requests are also very welcome. Checkout our [contributing guide](contributing.md) to get started.

&nbsp;

&nbsp;
