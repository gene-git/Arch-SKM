# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
Handles key generation.
"""
from ._genkeys_base import GenKeysBase
from .update_config import update_configs
from .make_keys import make_new_keys
from .refresh_needed import refresh_needed


class GenKeys(GenKeysBase):
    """
    Class derived from GenKeysBase.

    Creates out of tree kernel signing keys
    """
    def update_configs(self) -> bool:
        """
        Update configs with new keys if needed
        """
        if not update_configs(self):
            self.okay = False
        return self.okay

    def make_new_keys(self) -> bool:
        """
        Set up before we use openssl to create_new_keys()
        """
        # pylint: disable=
        if self.verb:
            print('Making new keys ')

        if not make_new_keys(self):
            self.okay = False
        return self.okay

    def refresh_needed(self) -> bool:
        """
        check if key refresh is needed
        """
        return refresh_needed(self)
