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

import subprocess
import os


def generate_animation_recorder_vrml(duration, output):
    return (
        f'DEF ANIMATION_RECORDER_SUPERVISOR Robot {{\n'
        f'  name "animation_recorder_supervisor"\n'
        f'  controller "animation_recorder"\n'
        f'  controllerArgs [\n'
        f'    "--duration={duration}"\n'
        f'    "--output={output}"\n'
        f'  ]\n'
        f'  children [\n'
        f'    Receiver {{\n'
        f'      channel 1024\n'
        f'    }}\n'
        f'  ]\n'
        f'  supervisor TRUE\n'
        f'}}\n'
    )

def record_animation(world_config, destination_directory):
    # Get world name and create directory
    world_name = world_config['file'].split('/')[1]
    subprocess.check_output(['mkdir', '-p', destination_directory])

    # Append `animation_recorder` controller
    animation_recorder_vrml = generate_animation_recorder_vrml(
        duration = world_config['duration'],
        output = os.path.join(os.path.abspath('.'), destination_directory, world_name.replace('.wbt', '.html'))
    )
    with open(world_config['file'], 'r') as f:
        world_content = f.read()
    with open(world_config['file'], 'w') as f:
        f.write(world_content + animation_recorder_vrml)

    # Runs simulation in Webots
    out = subprocess.Popen(
        ['xvfb-run', 'webots', '--stdout', '--stderr', '--batch', '--mode=fast', '--no-rendering', 'worlds/robot_programming.wbt'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    run_flag = False
    while not out.poll():
        stdoutdata = out.stdout.readline()
        if stdoutdata:
            if not run_flag: run_flag = True
            print(stdoutdata.decode('utf-8'))
        else:
            break
    # Removes `animation_recorder` controller
    with open(world_config['file'], 'w') as f:
        f.write(world_content)

    # Return
    return run_flag
