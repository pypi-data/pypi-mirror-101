# Copyright 1996-2021 Cyberbotics Ltd.
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
import shutil
import os
import sys
from multiprocessing import Process
from ._utils import get_tmp_dir, get_random_string, get_webots_home, handle_webots_installation
from .controller import Supervisor


class Webots:
    def __init__(self):
        self.__webots_process = None
        self.__temp_directory = get_tmp_dir()
        self.__temp_world_path = None
        os.mkdir(self.__temp_directory)

    @staticmethod
    def create_from_string(world_string):
        wb = Webots()
        wb.__start_simulation_from_string(world_string)
        return wb

    @staticmethod
    def create_from_file(world_file):
        wb = Webots()
        wb.__start_simulation_from_file(world_file)
        return wb

    def __start_simulation_from_string(self, world_string, gui=True):
        filepath = os.path.join('/tmp', 'webots_' + get_random_string() + '.wbt')
        self.__temp_world_path = filepath
        with open(filepath, 'w') as f:
            f.write(world_string.strip())
        self.__start_simulation_from_file(filepath, gui=gui)

    def __start_simulation_from_file(self, world_file, gui=True, mode='run'):
        if self.__webots_process is not None:
            raise Exception('You cannot start the simulation multiple times')

        webots_path = get_webots_home(show_warning=True)
        if webots_path is None:
            handle_webots_installation()

        # Add `webots` executable to command
        if sys.platform == 'win32':
            webots_path = os.path.join(webots_path, 'msys64', 'mingw64', 'bin')
        command = [os.path.join(webots_path, 'webots')]

        # Add `world`
        command += [world_file]
        command += [
            '--stdout',
            '--stderr',
            '--batch',
        ]
        command += ['--mode=' + mode]

        # Add parameters to hide GUI if needed
        if not gui:
            command += [
                '--minimize',
                '--no-rendering'
            ]

        # Spin the instance
        os.environ['WEBOTS_TMPDIR'] = self.__temp_directory
        self.__webots_process = subprocess.Popen(command, stdout=subprocess.PIPE)

    def get_supervisor(self):
        os.environ['WEBOTS_TMPDIR'] = self.__temp_directory
        return Supervisor()

    def __del__(self):
        if self.__webots_process:
            self.__webots_process.terminate()
        if os.path.exists(self.__temp_directory):
            shutil.rmtree(self.__temp_directory)
        if self.__temp_world_path is not None and os.path.exists(self.__temp_world_path):
            os.remove(self.__temp_world_path)
