<!---
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
-->

# Trainingopz

This library is a pre-alpha right now

The intent of this package is to work as a back-end build and deploy engine to take - given a configuration and an infrastructure, 
on-demand scientific computing workflows.


## Application Configuration

```yaml
versionon: 1

docker_configuration:
    docker_registry:  REPO_URL
workflow_validation:
type:  YAMLValidator
  conf:
    project_path: /

pipeline_composition:
  type: YAMLPipelineComposer
  conf:
    project_path: /

package:
  type: DockerPackager
  conf:
    project_path: /

build_deployment_artifact:
  type: BuildAirflowArtifact
  conf: null

deploy:
  type: AirflowDeployer
  conf: null

```