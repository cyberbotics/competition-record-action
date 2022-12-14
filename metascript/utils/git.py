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

import os
import requests
import subprocess


def init():
    username = os.environ['GITHUB_ACTOR']
    headers = {'Authorization': 'token ' + os.environ['INPUT_REPO_TOKEN']}

    user_info = requests.get(f'https://api.github.com/users/{username}', headers=headers).json()

    subprocess.check_output(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
    subprocess.check_output(['git', 'config', '--global', '--add', 'safe.directory', '/root/repo'])
    result = subprocess.run('git config --list | grep user.name', shell=True, check=False)
    if result.returncode != 0:
        email = '{}+{}@users.noreply.github.com'.format(user_info['id'], username)
        subprocess.check_output(['git', 'config', '--global', 'user.name', user_info['name'] or username])
        subprocess.check_output(['git', 'config', '--global', 'user.email', email])


def push(message='Updated competition recordings'):
    github_repository = 'https://{}:{}@github.com/{}'.format(
        os.environ['GITHUB_ACTOR'],
        os.environ['INPUT_REPO_TOKEN'],
        os.environ['GITHUB_REPOSITORY']
    )
    print(f'GitHub repository: https://github.com/{os.environ["GITHUB_REPOSITORY"]}')
    try:
        if os.path.exists('participants.json'):
            subprocess.check_output(['git', 'add', '-A', 'participants.json'])
        if os.path.exists('storage'):
            subprocess.check_output(['git', 'add', '-A', 'storage'])
        print(subprocess.check_output(['git', 'commit', '-m', message], stderr=subprocess.STDOUT).decode('utf-8'))
        print(subprocess.check_output(['git', 'push', '-f', github_repository]).decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print('Nothing to commit and push.')


def clone(repo, path):
    subprocess.check_output(['git', 'clone', repo, path])
