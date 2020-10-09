=========
CHANGELOG
=========

0.1
---

* Initial release of Alexa Skills Kit Webservice Support Package.


0.1.2
-----

This release contains the following changes : 

- Fix setting the custom user agent on the skill instance, when initializing the handler.
 
 
1.0.0
-------
 
This release contains the following changes :
 
- Move the webservice adapters to GA.
 
 

1.1.0
~~~~~~~

This release contains the following changes : 

- Timestamp verifier checks the total number of seconds between request timestamp and server timestamp.
- Add context management to urlopen method used in request verification.


1.2.0
~~~~~

This release contains the following changes : 

- Case-insensitive header value retrieval for request verification. `136 <https://github.com/alexa/alexa-skills-kit-sdk-for-python/issues/136>`__


1.3.0
~~~~~

This release contains the following changes :

- Certificate chain validation in request verification, to check the certificate chain validates to a trusted root CA.


1.3.1
~~~~~

This release contains the following changes :

- Fix the dependencies in the setup file, for cert validation.


1.3.2
~~~~~

This release contains the following changes :

- Fix timestamp verifier maximum tolerance value for skill events and normal skill requests.


