# Copyright 2017 SuccessOps, LLC All rights reserved.
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

def GenerateConfig(context):

  project = context.env['project']
  project_number = context.env['project_number']
  resources = []

  for service in context.properties['backend-services']:
    name = service['name']
    enableCdn = service['enableCdn']
    health_checks = []
    for health_check in service['health-checks']:
      health_checks.append('$(ref.{}.selfLink)'.format(health_check))

    backends = []
    for backend in service['backends']:
      temp = '$(ref.{}.instanceGroup)'.format(backend['group'])
      backends.append({
        'balancingMode': backend['mode'],
        'capacityScaler': backend['capacityScaler'],
        'group': temp,
        'maxRatePerInstance': backend['maxRatePerInstance'],
        'maxUtilization': backend['maxUtilization'],
      })

    resources.append(
      {
        'name': name,
        'type': 'compute.v1.backendService',
        'properties': {
          'healthChecks': health_checks,
          'protocol': 'HTTP',
          'enableCDN': enableCdn,
          'backends': backends
        }
      })

  return {'resources': resources}
