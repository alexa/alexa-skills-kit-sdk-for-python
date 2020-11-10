#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights
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

__pip_package_name__ = 'ask-sdk-local-debug'
__description__ = ('The ASK SDK Local Debug package provides Alexa Skills Kit '
                   'debugger functionality')
__url__ = 'https://github.com/alexa/alexa-skills-kit-sdk-for-python'
__version__ = '1.1.0'
__author__ = 'Alexa Skills Kit'
__author_email__ = 'ask-sdk-dynamic@amazon.com'
__license__ = 'Apache 2.0'
__keywords__ = ['ASK SDK', 'Alexa Skills Kit', 'Alexa', 'Debug']
__install_requires__ = ["ask-sdk-model>=1.23.1", "ask-sdk-model-runtime",
                        "autobahn[twisted, encryption]>=20.4.3",
                        "requests"]
