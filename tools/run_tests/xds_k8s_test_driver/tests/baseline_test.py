# Copyright 2020 gRPC authors.
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

from framework import xds_k8s_testcase
from framework import xds_url_map_testcase

logger = logging.getLogger(__name__)
flags.adopt_module_key_flags(xds_k8s_testcase)

# Type aliases
_XdsTestServer = xds_k8s_testcase.XdsTestServer
_XdsTestClient = xds_k8s_testcase.XdsTestClient
RpcTypeUnaryCall = xds_url_map_testcase.RpcTypeUnaryCall

class BaselineTest(xds_k8s_testcase.RegularXdsKubernetesTestCase):
    def test_traffic_director_grpc_setup(self):
        with self.subTest("0_create_health_check"):
            self.td.create_health_check()

        with self.subTest("1_create_backend_service"):
            self.td.create_backend_service()

        with self.subTest("2_create_url_map"):
            self.td.create_url_map(self.server_xds_host, self.server_xds_port)

        with self.subTest("3_create_target_proxy"):
            self.td.create_target_proxy()

        with self.subTest("4_create_forwarding_rule"):
            self.td.create_forwarding_rule(self.server_xds_port)

        with self.subTest("5_start_test_server"):
            # test_server: _XdsTestServer = self.startTestServers()[0]
            test_servers: _XdsTestServer = self.startTestServers(3)
            print("[gina]" + test_servers[0].hostname)
            print("[gina]" + test_servers[1].hostname)
            print("[gina]" + test_servers[2].hostname)

        with self.subTest("6_add_server_backends_to_backend_service"):
            self.setupServerBackends()

        with self.subTest("7_start_test_client"):
            test_client: _XdsTestClient = self.startTestClient(test_servers[0])

        with self.subTest("8_test_client_xds_config_exists"):
            self.assertXdsConfigExists(test_client)

        cookie = ""
        hostname = ""
        chosenServerIdx = None
        with self.subTest("9_test_server_received_rpcs_from_test_client"):
            print("[gina] baseline_test.py")
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

        with self.subTest("10_test_chosen_server"):
            print("[gina] update_config.configure")
            test_client.update_config.configure(
                rpc_types=(RpcTypeUnaryCall,),
                metadata=(
                    (
                        RpcTypeUnaryCall,
                        "cookie",
                        cookie,
                    ),
                ),
            )
            self.assertRpcsEventuallyGoToGivenServers(
                test_client, test_servers[chosenServerIdx:chosenServerIdx+1], 10
            )

if __name__ == "__main__":
    absltest.main(failfast=True)
