=========
CHANGELOG
=========

0.1
-------

* Initial release of alexa skills kit core sdk.

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

* Production release of ASK SDK Core Package.


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



1.5.0
~~~~~~~

This release contains the following changes :

- Refactor Python version dependencies for Python 3.7 support `50 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/50>`__


1.6.0
~~~~~~~

This release contains the following changes :

- Update DefaultSerializer to let generic classes to be added as session attributes `60 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/60>`__.


1.7.0
~~~~~~~

This release contains the following changes :

- Add optional `play_behavior` attribute to `speak` and `ask` methods in response builder `61 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/61>`__. 


1.8.0
~~~~~~~

This release contains the following changes : 

- Allow Default API Client to invoke Alexa APIs that require other than 'application/json' body type.



1.9.0
~~~~~~~

This release includes the following : 

- Request utility methods which makes it easier to retrieve common properties from an incoming request.


1.10.0
~~~~~~~

This release contains the following changes : 

- Viewport Utils support for Echo Show 5 (HUB_LANDSCAPE_SMALL).
- Add check for device information in 'get_device_id' utility function.
- Add 'get_user_id' utility function.


1.10.1
^^^^^^^

This release contains the following : 

- Fix the regression bug on `response_interceptors`.



1.10.2
^^^^^^^

This release contains the following changes :

- `Bug fix <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/99>`__ on delete persistence attributes, to delete attributes without checking if they are set.
- Fix `type hints <https://github.com/alexa/alexa-skills-kit-sdk-for-python/pull/95>`__ on lambda_handler.
