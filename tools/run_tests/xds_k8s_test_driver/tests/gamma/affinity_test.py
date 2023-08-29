# Copyright 2023 gRPC authors.
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
import logging

from absl import flags
from absl.testing import absltest

from framework import xds_gamma_testcase
from framework import xds_k8s_testcase

logger = logging.getLogger(__name__)
flags.adopt_module_key_flags(xds_k8s_testcase)

_XdsTestServer = xds_k8s_testcase.XdsTestServer
_XdsTestClient = xds_k8s_testcase.XdsTestClient


class AffinityTest(xds_gamma_testcase.GammaXdsKubernetesTestCase):
    def test_ping_pong(self):
        REPLICA_COUNT = 3

        test_servers: List[_XdsTestServer]
        with self.subTest("01_run_test_server"):
            test_servers = self.startTestServers(replica_count=REPLICA_COUNT)

        with self.subTest("02_create_ssa_policy"):
#            self.server_runner.k8s_namespace.get_gamma_mesh('test')
            self.server_runner.createSessionAffinityPolicy()

        # Default is round robin LB policy.

        with self.subTest("03_start_test_client"):
            test_client: _XdsTestClient = self.startTestClient(test_servers[0])

        #4 send 1st RPC
        #5 retrives cookie from rpc header
        with self.subTest("04_test_server_received_rpcs_from_test_client"):
            cookie = self.assertSuccessfulRpcs(test_client)

        #5 retrives cookie from rpc header
        #6 send 10 RPCs with cookie
        #7 ensure all are sending to the same backend


if __name__ == "__main__":
    absltest.main(failfast=True)
