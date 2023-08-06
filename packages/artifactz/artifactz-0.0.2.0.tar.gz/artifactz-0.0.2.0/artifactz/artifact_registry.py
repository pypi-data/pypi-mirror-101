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


class ArtifactRegistry:

    def __init__(self, **kwargs):
        self._project_name = kwargs.pop('project_name')
        self._artifact_stage = kwargs.pop('artifact_stage')

    def register(self, name: str, artifact: dict, version: int = None):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def retrieve_to(self, name: str, copy_to: str, version: int = None):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')
