# Copyright 2020 DeepMind Technologies Limited. All rights reserved.
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

"""Launches consumer-producer example on GCP."""


import os

from absl import app
from absl import flags
import launchpad as lp
from launchpad.examples.consumer_producers.program import make_program
from launchpad.nodes.python import xm_docker

_NUM_PRODUCERS = flags.DEFINE_integer('num_producers', 2,
                                      'The number of concurrent producers.')


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  docker_code_directory = os.getcwd()
  dir_path = os.path.dirname(os.path.realpath(__file__))
  docker_requirements = os.path.join(dir_path, 'requirements.txt')
  docker_config = xm_docker.DockerConfig(docker_code_directory,
                                         docker_requirements)
  resources = {'producer': docker_config, 'consumer': docker_config}

  program = make_program(num_producers=_NUM_PRODUCERS.value)
  lp.launch(
      program,
      launch_type=lp.LaunchType.CAIP,
      local_resources=resources)


if __name__ == '__main__':
  app.run(main)
