#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

sampling_service = None


def get_sampling_service():
    global sampling_service
    if not sampling_service:
        init(True)
    return sampling_service


def init(force: bool = False):
    """
    If the sampling service is not initialized, initialize it.
    if force, we are in a fork(), we force re-initialization
    """
    from skywalking.sampling.sampling_service import SamplingService

    global sampling_service
    if sampling_service and not force:
        return

    sampling_service = SamplingService()
    sampling_service.start()
