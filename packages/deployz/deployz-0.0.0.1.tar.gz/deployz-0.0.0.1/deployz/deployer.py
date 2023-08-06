# Copyright © 2021 Hashmap, Inc
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
import os
from typing import Optional

from providah.factories.package_factory import PackageFactory as pf
import yaml
from fastapi import FastAPI
from pydantic import BaseModel

from deployz.executors.executor import Executor

deployer = FastAPI()


@deployer.get("/")
def read_root():
    return {"Hello": "World"}


class MaasServePacket(BaseModel):
    project_name: str
    version: int


class TrainPacket(BaseModel):
    project_name: str
    version: Optional[int]


@deployer.post("/serve/{project_id}")
def serve(project_id: str, to_serve_packet: MaasServePacket = None):
    executor = _get_servz()
    executor.run()
    return {"item_id": project_id, "packet": to_serve_packet}


@deployer.post("/train/")
def train(to_train_packet: TrainPacket = None):
    executor = _get_autotrainz()
    executor.run(artifact=to_train_packet.project_name,
                 version=to_train_packet.version)
    return {"packet": to_train_packet}


# -------------------------------------------------- #
# ------------------ Support Code ------------------ #
# -------------------------------------------------- #


def _get_servz() -> Executor:
    config: dict = _get_configuration()
    servz_config = config['servz']
    registry = pf.create(key=servz_config['artifact_registry']['name'],
                         configuration=servz_config['artifact_registry']['conf'])
    executor_config = servz_config['executor']['conf']
    executor_config['registry'] = registry
    executor = pf.create(key=servz_config['executor']['name'],
                         configuration=executor_config)

    return executor


def _get_autotrainz() -> Executor:
    config: dict = _get_configuration()
    autotrainz_config = config['autotrainz']
    registry = pf.create(key=autotrainz_config['artifact_registry']['name'],
                         configuration=autotrainz_config['artifact_registry']['conf'])
    executor_config = autotrainz_config['executor']['conf']
    executor_config['registry'] = registry
    executor = pf.create(key=autotrainz_config['executor']['name'],
                         configuration=executor_config)

    return executor


def _get_configuration() -> dict:
    path = os.getenv('DEPLOYZ_CONF')
    if not path:
        path = 'deployz.yml'

    with open(path, 'r') as stream:
        configuration = yaml.safe_load(stream)

    return configuration
