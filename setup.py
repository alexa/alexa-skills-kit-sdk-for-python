# -*- coding: utf-8 -*-
#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights
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
from __future__ import print_function
import glob
import os
import sys
import copy
import runpy

here = os.path.abspath(os.path.dirname(__file__))

packages = [
    os.path.dirname(p) for p in glob.glob(
        os.path.join("ask-sdk*", "setup.py"))]

for pkg in packages:
    pkg_folder = os.path.join(here, pkg)
    pkg_setup_path = os.path.join(pkg_folder, "setup.py")

    current_dir = os.getcwd()
    current_path = sys.path

    try:
        os.chdir(pkg_folder)
        sys.path = [pkg_setup_path] + copy.copy(sys.path)

        print("Installing package: {}".format(pkg))
        runpy.run_path(pkg_setup_path)
    except Exception as e:
        print("Installation failed for package: {}".format(pkg))
        print("Exception raised: {}".format(e))
    finally:
        os.chdir(current_dir)
        sys.path = current_path
