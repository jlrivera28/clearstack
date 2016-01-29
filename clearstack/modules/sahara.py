#
# Copyright (c) 2015 Intel Corporation
#
# Author: Jose Luis Rivera <jose.luis.rivera.magallon@intel.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from modules.openstack import OpenStackService
from modules.conf import CONF
from common import util
from common.util import LOG
from common.singleton import Singleton


@Singleton
class Sahara(OpenStackService):
    _name = "sahara"
    _bundle = "openstack-data-processing"
    _services = ["sahara-all"]
    _type = "data-processing"
    _description = "OpenStack Data Processing"
    _public_url = ("http://{0}:8386/v1.1/%\(tenant_id\)s"
                   .format(CONF['CONFIG_CONTROLLER_HOST']))

    def sync_database(self):
        LOG.debug("syncing database")
        util.run_command("su -s /bin/sh -c \"sahara-db-manage upgrade head\" sahara")

    def ceilometer_enable(self, configfile):
        self.config_rabbitmq(configfile)
        config = ("[DEFAULT]\n"
                  "notification_driver = messagingv2\n")
        util.write_config(configfile, config)
