# Copyright 2018 Datawire. All rights reserved.
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
# limitations under the License

from typing import TYPE_CHECKING
from typing import cast as typecast

from ...ir.irtracing import IRTracing

if TYPE_CHECKING:
    from . import V2Config


class V2Tracing(dict):
    def __init__(self, config: 'V2Config') -> None:
        # We should never be instantiated unless there is, in fact, defined tracing stuff.
        assert config.ir.tracing

        super().__init__()

        tracing = typecast(IRTracing, config.ir.tracing)

        name = tracing['driver']

        if not name.startswith('envoy.'):
            name = 'envoy.%s' % (name.lower())

        self['http'] = {
            "name": name,
            "config": tracing['driver_config'],
        }

    @classmethod
    def generate(cls, config: 'V2Config') -> None:
        config.tracing = None

        if config.ir.tracing:
            config.tracing = config.save_element('tracing', config.ir.tracing, V2Tracing(config))
