#!/bin/bash
# Copyright 2018 gRPC authors.
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

# Generate the list of boringssl symbols that need to be renamed based on the
# current boringssl submodule. The script should be run after a boringssl
# upgrade in third_party/boringssl-with-bazel. Note that after the script is
# run, you will typically need to manually upgrade the BoringSSL-GRPC podspec
# (templates/src/objective-c/BoringSSL-GRPC.podspec.template) version and the
# corresponding version number in gRPC-Core podspec
# (templates/gRPC-Core.podspec.template).

set -ev

cd "$(dirname $0)"
cd ../../third_party/boringssl-with-bazel

BORINGSSL_COMMIT=$(git rev-parse HEAD)
BORINGSSL_PREFIX_HEADERS_DIR=src/boringssl

# generate the prefix header
mkdir -p build
cd build
cmake ..
make clean
make -j

[ -f ssl/libssl.a ] || { echo "Failed to build libssl.a" ; exit 1 ; }
[ -f crypto/libcrypto.a ] || { echo "Failed to build libcrypto.a" ; exit 1 ; }

go run ../util/read_symbols.go ssl/libssl.a > ./symbols.txt
go run ../util/read_symbols.go crypto/libcrypto.a >> ./symbols.txt

# generates boringssl_prefix_symbols.h
cmake .. -DBORINGSSL_PREFIX=GRPC -DBORINGSSL_PREFIX_SYMBOLS=symbols.txt
make boringssl_prefix_symbols

[ -f symbol_prefix_include/boringssl_prefix_symbols.h ] || { echo "Failed to build boringssl_prefix_symbols.sh" ; exit 1 ; }

cd ../../..
mkdir -p $BORINGSSL_PREFIX_HEADERS_DIR
echo "// generated by generate_boringssl_prefix_header.sh on BoringSSL commit: $BORINGSSL_COMMIT" > $BORINGSSL_PREFIX_HEADERS_DIR/boringssl_prefix_symbols.h
echo "" >> $BORINGSSL_PREFIX_HEADERS_DIR/boringssl_prefix_symbols.h
cat third_party/boringssl-with-bazel/build/symbol_prefix_include/boringssl_prefix_symbols.h >> $BORINGSSL_PREFIX_HEADERS_DIR/boringssl_prefix_symbols.h

# Regenerated the project
tools/buildgen/generate_projects.sh

exit 0
