#!/usr/bin/env python3
#
# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
from glob import glob
from pathlib import Path
import subprocess
from benchmark_record_action.config import RESOURCES_DIRECTORY
import benchmark_record_action.utils.git as git

def test_push():
    print("Listing directories and files in repository: ", os.environ['GITHUB_REPOSITORY'], " (on branch: ", os.environ['GITHUB_REF'].split('/')[-1], ")")
    for path in Path('').glob('*'):
        path = str(path)
        print('path: ', path)

    print("\nMoving directory...")

    for path in Path('').glob('*'):
        path = str(path)
        if path == 'AxjD2FU':
            shutil.move(path, 'storage')

    print("\nListing files after move:")
    for path in Path('').glob('*'):
        path = str(path)
        print('path: ', path)

    print("Commit ad push changes to branch: ", os.environ['GITHUB_REF'].split('/')[-1])
    git.push(message="change file location")

