=========
CHANGELOG
=========

0.1
-------

* Initial release of ASK SDK Standard package.

0.1.1
~~~~~

* Docstring changes for generated docs.

0.1.2
~~~~~

* unicode_type = six.text_type and define long in Python 3 (#1)
* Use feature detection instead of version detection (#10)
* Send stringified raw data to Alexa APIs (#12)

0.1.3
~~~~~~~

* Remove inspect.getargspec from sb decorators. Closes `#20 <https://github.com/alexa-labs/alexa-skills-kit-sdk-for-python/issues/20>`_

1.0.0
-----

* Production release of ASK SDK Standard Package.


1.1.0
~~~~~~~

This release contains the following changes:

- Introducing runtime layer (`#41 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/41>`__)
- Send data to service clients only if present (`#39 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/39>`__)





1.2.0
~~~~~~~

This release contains the following changes : 

- Add support for Alexa Presentation Language (Public Beta). The Alexa Presentation Language (APL) enables you to build interactive voice experiences that include graphics, images, slideshows, and to customize them for different device types.


1.3.0
~~~~~~~

This release contains the following features : 

- Support for [Name-free Interactions, using CanFulfill Intent in responses](https://developer.amazon.com/docs/custom-skills/implement-canfulfillintentrequest-for-name-free-interaction.html).


1.4.0
~~~~~~~

This release contains the following changes : 

- Add helper function for matching CanFulfill Intent name `#46 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/46>`
- Deserialize only if payload is not None `48 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/48>`

