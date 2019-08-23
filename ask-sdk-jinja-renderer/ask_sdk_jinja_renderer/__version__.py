#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.
#

__pip_package_name__ = 'ask-sdk-jinja-renderer'
__description__ = ('ask-sdk-jinja-renderer is an SDK package for supporting '
                   'template responses for skill developers, when built using '
                   'ASK Python SDK. It provides jinja framework as a template '
                   'engine to render the response loaded from the template'
                   'and inject the data passed and finally deserialize it to'
                   'a custom response format')
__url__ = 'https://github.com/alexa/alexa-skills-kit-sdk-for-python'
__version__ = '1.0.0'
__author__ = 'Alexa Skills Kit'
__author_email__ = 'ask-sdk-dynamic@amazon.com'
__license__ = 'Apache 2.0'
__keywords__ = ['ASK SDK', 'Alexa Skills Kit', 'Alexa']
__install_requires__ = ["ask-sdk-core>1.10.2", "jinja2>=2.10.1"]