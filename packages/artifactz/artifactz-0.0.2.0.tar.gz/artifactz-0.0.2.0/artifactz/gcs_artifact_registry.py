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
from typing import List

from google.cloud import storage
from google.cloud.storage import Bucket, Client
from google.oauth2 import service_account

from artifactz.artifact_registry import ArtifactRegistry


class GCSArtifactRegistry(ArtifactRegistry):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gcp_project = kwargs.pop('gcp_project')

    def register(self, name: str, artifact: dict, version: int = None) -> None:
        """ Register a new artifact

        Args:
            name: Name given to the artifact
            artifact: structure containing the artifact.
            version: version number to be assigned to the artifact. Default results in incrementing the version autoatmically.

        """
        client = storage.Client(project=self._gcp_project)
        bucket = client.get_bucket(self._project_name)
        path = Path(artifact['filename'])
        object_root = f'{self._artifact_stage}/{path.stem}'
        if not version:
            version = self._next_version(client, bucket, object_root)

        object_path = f"{object_root}/version_{version}{path.suffix}"
        blob = bucket.blob(object_path)

        result = blob.upload_from_filename(artifact['filename'])

        return result

    def retrieve_to(self, name: str, copy_to: str, version: int = None) -> None:
        """ Retrieve an artifact from the registry and store it locally.

        Args:
            name: Name of artifact to retrieve
            copy_to: Location (local) to copy the artifact to
            version: Version of the artifact to retrieve

        """
        client = storage.Client(project=self._gcp_project)
        bucket = client.get_bucket(self._project_name)
        object_root = f'{self._artifact_stage}/{name}'
        if not version:
            version = self._get_max_version(client, bucket, object_root)

        extension = self._get_extension(client=client, bucket=bucket, object_root=object_root)
        blob = bucket.blob(f'{object_root}/version_{version}{extension}')
        blob.download_to_filename(filename=copy_to)

    @classmethod
    def _next_version(cls, client: Client, bucket: Bucket, object_root: str) -> int:
        return cls._get_max_version(client, bucket, object_root) + 1

    @classmethod
    def _get_max_version(cls, client: Client, bucket: Bucket, object_root: str) -> int:
        blobs = list(client.list_blobs(bucket_or_name=bucket, prefix=object_root + '/version'))
        versions: List[int] = [int(Path(blob.name).stem.split('.')[-1].split('_')[-1]) for blob in blobs]

        if len(versions) > 0:
            return max(versions)

        return 0

    @classmethod
    def _get_extension(cls, client, bucket, object_root):
        blobs = list(client.list_blobs(bucket_or_name=bucket, prefix=object_root + '/version', max_results=1))
        return [Path(blob.name).suffix for blob in blobs][0]
