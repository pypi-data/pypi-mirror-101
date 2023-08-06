# Copyright (C) 2021 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class AdminService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def sign_in(
            self,
            identifier,
            password):
        """
        Sign in an administrator of an organization managing one or more
        school campuses


        :param identifier: The identifier of the account of a user:

            * An e-mail address. E-mail address is not case sensitive.
            * A phone number in `E.164 numbering plan, formatted according to the
              Extensible Provisioning Protocol (EPP) Contact Mapping.
            * A username.  Username is case sensitive.

        :param password: The password associated to the user's account.


        :return: An object corresponding to the login session of the user, and
            other information.


        :raise AuthenticationFailureException: If the given contact
            information and/or password don't match any account registered
            against the platform.

        :raise DeletedObjectException: If the user account has been deleted.

        :raise DisabledObjectException: If the user account has been disabled.

        :raise UnverifiedContactException: If the contact of this user has not
            been verified yet, while the parameter `allow_unverified_contact`
            has been passed with the value `False`.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/admin/account/session',
                arguments={
                    'identifier': identifier,
                    'password': password,
                },
                authentication_required=False,
                signature_required=True))
