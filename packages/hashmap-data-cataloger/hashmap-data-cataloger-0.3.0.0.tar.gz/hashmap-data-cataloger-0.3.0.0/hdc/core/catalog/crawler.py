#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
# TODO: Module description
"""
import logging

from pandas import DataFrame


class Crawler:

    def __init__(self, **kwargs):
        self.__logger = self._get_logger()
        self._conf = kwargs.get("conf")  # Shared property in Crawler hierarchy

    def obtain_catalog(self) -> DataFrame:
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _get_logger(self):
        return logging.getLogger(".".join([class_type.__name__ for class_type in self.__class__.mro()[-2::-1]]))
