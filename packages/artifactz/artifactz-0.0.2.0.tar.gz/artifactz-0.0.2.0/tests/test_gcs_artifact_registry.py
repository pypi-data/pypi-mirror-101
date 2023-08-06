# Modifications © 2020 Hashmap, Inc
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
from pathlib import Path

from artifactz.artifact_registry import ArtifactRegistry
from tests.test_artifact_registry import TestArtifactRegistry
import artifactz

from providah.factories.package_factory import PackageFactory as pf


class TestGCSArtifactRegistry(TestArtifactRegistry):

    def setUp(self):
        self._registry: ArtifactRegistry = pf.create('GCSArtifactRegistry', configuration={
            'gcp_project': 'ctso-mlops-poc',
            'artifact_stage': 'training_pipelines',
            'project_name': 'mlopz-unit-testing',
        })

    def test_register(self):
        self._registry.register('test', artifact={
            'filename': Path.joinpath(Path.cwd(), '_test_inputs/some_input.zip')
        })
        self._registry.register('test', artifact={
            'filename': Path.joinpath(Path.cwd(), '_test_inputs/other_input.txt')
        })

    def test_retrieve(self):
        self._registry.retrieve_to(name='some_input',
                                   copy_to=str(Path.joinpath(Path.cwd(), '_test_outputs/some_input.zip'))
                                   )

        self._registry.retrieve_to(name='other_input',
                                   copy_to=str(Path.joinpath(Path.cwd(), '_test_outputs/other_input.txt'))
                                   )
