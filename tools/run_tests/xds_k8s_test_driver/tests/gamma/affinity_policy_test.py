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
from collections import namedtuple

from absl import flags
from absl.testing import absltest

from framework import xds_gamma_testcase
from framework import xds_k8s_testcase
from framework import xds_url_map_testcase

logger = logging.getLogger(__name__)
flags.adopt_module_key_flags(xds_k8s_testcase)

_XdsTestServer = xds_k8s_testcase.XdsTestServer
_XdsTestClient = xds_k8s_testcase.XdsTestClient
RpcTypeUnaryCall = xds_url_map_testcase.RpcTypeUnaryCall

class AffinityTest(xds_gamma_testcase.GammaXdsKubernetesTestCase):
    def test_ping_pong(self):
        REPLICA_COUNT = 3

#        test_servers: List[_XdsTestServer]
#        with self.subTest("01_run_test_server"):
#            test_servers = self.startTestServers(replica_count=REPLICA_COUNT)
#            print("[gina] server[0]: " + test_servers[0].hostname)
#            print("[gina] server[1]: " + test_servers[1].hostname)
#            print("[gina] server[2]: " + test_servers[2].hostname)

#        with self.subTest("02_create_ssa_policy"):
#            self.server_runner.createSessionAffinityPolicy()

        # Default is round robin LB policy.

        # TODO
        with self.subTest("03_start_test_client"):
#            test_client: _XdsTestClient = self.startTestClient(test_servers[0])
            fake_server = namedtuple("Server", ["xds_uri"])
            fake_server.xds_uri = "xds:///ssa-test"
            test_client: _XdsTestClient = self.startTestClient(fake_server)

        cookie = ""
        hostname = ""
        chosenServerIdx = None
        with self.subTest("04_send_first_RPC_and_retrieve_cookie"):
            cookies = self.assertSuccessfulRpcs(test_client, 1)
            print(cookies)
            hostname = next(iter(cookies))
            cookie = cookies[hostname]
            for idx, server in enumerate(test_servers):
                if server.hostname == hostname:
                    chosenServerIdx = idx
                    break
            print("[gina] chosenServerIdx: ", chosenServerIdx)
            print("[gina] hostname: ", hostname)
            print("[gina] cookie: ", cookie)

#        with self.subTest("05_send_RPCs_with_cookie"):
#            print("[gina] update_config.configure")
#            test_client.update_config.configure(
#                rpc_types=(RpcTypeUnaryCall,),
#                metadata=(
#                    (
#                        RpcTypeUnaryCall,
#                        "cookie",
#                        cookie,
#                    ),
#                ),
#            )
#            self.assertRpcsEventuallyGoToGivenServers(
#                test_client, test_servers[chosenServerIdx:chosenServerIdx+1], 10
#            )
#
if __name__ == "__main__":
    absltest.main(failfast=True)
