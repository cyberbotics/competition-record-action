#!/usr/bin/env python3
#
# Copyright 1996-2022 Cyberbotics Ltd.
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

import requests

def upload_file(repository, token, file):
    print(f'Posting: repository={repository} file={file}')
    data = {'repository': repository, 'token': token}
    with open(file, 'rb') as f:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post('https://webots.cloud/ajax/project/upload.php', files={file: f}, json=data, headers=headers)
        print(response.text)
