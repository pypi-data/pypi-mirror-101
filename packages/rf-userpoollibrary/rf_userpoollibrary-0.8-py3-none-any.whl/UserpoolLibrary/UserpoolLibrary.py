# Copyright (C) 2019 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import requests
import logging
import json
import socket
from os import environ
from UserpoolLibrary.Utils import retry
from UserpoolLibrary.version import VERSION

from robotlibcore import (HybridCore,
                          keyword)

__version__ = VERSION

LOGGER = logging.getLogger(__name__)


class UserpoolLibrary(HybridCore):
    """
    A test library providing user pool support for testing.

        ``UserpoolLibrary`` is a Robot Framework third party library that \
            enables test to borrow available user from a user pool. These \
                allows test to run in CI server without user conflict and \
                    lessen setup and maintenance on a project.

        - borrowing an available user from the user pool and returning it.
        - retrieving a user from the user pool by user id
        - updating user password

        == Table of contents ==

        - `Usage`
        - `Borrowed User Object`
        - `Author`
        - `Developer Manual`
        - `Importing`
        - `Shortcuts`
        - `Keywords`


    = Usage =

    == Adding this Library to your Test Suite ==

    | =Settings= | =Value=         | =Parameter=                        |
    | Library    | UserpoolLibrary | base_url/operator_id               |

    You can import this library in your robot test suite by using the       \
        syntax below.
    For the parameters on import. Read `Importing`.

    *Example:*
    | =Settings= | =Value=         | =Parameter=                        |
    | Library    | UserpoolLibrary | http://myhost.com/userpoolapi/129  |


    == Borrowing User ==

    ``currency_code`` and ``category`` are optional parameter in `Borrow User`

    *Example:*
     - Borrow any FREE User
    |               |               | =currency_code=   | =category=    |
    | ${user1}      | `Borrow User` |                   |               |
    | `Return User` | ${user}       |                   |               |

    | ${user1} = {
    |             "id": 4,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "USD",
    |             "category": "CAT1,CAT2",
    |             "status": "ACTIVE",
    |             "email": "user@email.com",
    |             "mobileNo": "12345678910",
    |             "ip": "192.168.1.1",
    |             "hostName": "hostname",
    |             "modifiedDate": "2020-01-13T06:02:25.0850053Z"
    |           }


    - Borrow USER by ``currency_code``
    |               |               | =currency_code=   | =category=    |
    | ${user2}      | `Borrow User` | RMB               |               |
    | `Return User` | ${user}       |                   |               |

    | ${user2} = {
    |             "id": 2,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "RMB",
    |             "category": "CAT1,CAT2,CAT3",
    |             "status": "ACTIVE",
    |             "email": "user@email.com",
    |             "mobileNo": "12345678910",
    |             "ip": "192.168.1.1",
    |             "hostName": "hostname",
    |             "modifiedDate": "2020-01-13T06:02:25.0850053Z"
    |           }


    - Borrow User by ``currency_code`` and ``category``
    | ${user3}      | `Borrow User` | RMB               | CAT1          |
    | `Return User` | ${user}       |                   |               |

    | ${user3} = {
    |             "id": 2,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "RMB",
    |             "category": "CAT1,CAT2,CAT3",
    |             "status": "ACTIVE",
    |             "email": "user@email.com",
    |             "mobileNo": "12345678910",
    |             "ip": "192.168.1.1",
    |             "hostName": "hostname",
    |             "modifiedDate": "2020-01-13T06:02:25.0850053Z"
    |           }


    - Borrow User by ``category``
    | ${user4}      | `Borrow User` | ${EMPTY}          | CAT1          |
    | `Return User` | ${user}       |                   |               |

    | ${user4} = {
    |             "id": 1,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "IDR",
    |             "category": "CAT1,CAT2",
    |             "status": "ACTIVE",
    |             "email": "user@email.com",
    |             "mobileNo": "12345678910",
    |             "ip": "192.168.1.1",
    |             "hostName": "hostname",
    |             "modifiedDate": "2020-01-13T06:02:25.0850053Z"
    |           }

    = Borrowed User Object =

    Borrow User returns a json object containing the following information:
    | =Attribute=           | =Type=    | =Description=                 |
    | id                    | int       | Unique User ID                |
    | operatorId            | int       | The User Operator Id          |
    | userName              | string    | User's username               |
    | passWord              | string    | User's password               |
    | currencyCode          | string    | User's currency code          |
    | category              | string    | User's category               |
    | status                | string    | User's current status         |
    | email                 | string    | User's email address          |
    | mobileNo              | string    | User's Mobile Number          |
    | ip                    | string    | The Borrower's IP Address     |
    | hostName              | string    | The Borrower's Hostname       |
    | modifiedDate          | string    | Indicated when the user's \
                                          data been last modified       |

    *JSON Representation:*
    | {
    |   "id": "userId",
    |   "operatorId": 10001,
    |   "userName": "sampleUserName",
    |   "passWord": "userpassword",
    |   "currencyCode": "PHP",
    |   "category": "NORMAL",
    |   "status": "ACTIVE",
    |   "email": "user@email.com",
    |   "mobileNo": "12345678910",
    |   "ip": "192.168.1.1",
    |   "hostName": "hostname",
    |   "modifiedDate": "2020-01-13T06:02:25.0850053Z"
    | }

    == Accessing User Data ==

    The borrowed user data can be accessed by using either the dot(.) \
        syntax or by invoking the key inside a square bracket(['key']).

    *Example:*
    | ${user}               | `Borrow User` | #Borrow any available user |
    | Log To Console        | ${user}[userName]                          |
    | Input Text            | usernameField | ${user}[userName]          |
    | Input Password        | passwordField | ${user}[passWord]          |

    = Author =

    Created: 09/10/2019

    Author: Shiela Buitizon | email:shiela.buitizon@mnltechnology.com

    Company: Spiralworks Technologies Inc.

    = Developer Manual =

        Compiling this pip package:
            - python setup.py bdist_wheel

        Uploading build to pip
            - python -m twine upload dist/*
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, base_url=None):
        """
        Initialize with  base url.
        """
        libraries = []
        HybridCore.__init__(self, libraries)
        self.base_url = base_url
        self.machineHostName = self._append_test_trigger_category()
        self.machineIp = self._get_machine_ip()

    @keyword
    @retry(Exception, tries=3)
    def borrow_user(self, currency_code=None, category=None):
        """Borrows a FREE user from the user pool given `currency_code`
        and 'category` and sets it to ACTIVE

        - param ``currency_code``: (optional)
        - param ``category``: (optional)
        - return: free user from the user pool as json object with \
        status set to ACTIVE.

        Refer to `Borrowed User Object` for
        more information.

        Example:
        | ${user}   | `Borrow User`     |                               |
        | ${user}   | `Borrow User`     | currency=RMB                  |
        | ${user}   | `Borrow User`     | category=TEST                 |
        | ${user}   | `Borrow User`     | currency=USD \
                                        | category=TEST                 |

         - Borrowing user with multiple categories. The library supports
            comma separated params for the user\
             ``category``.
        | ${user}   | `Borrow User`     | category=TEST,FT,SAMPLE       |
        """
        return self._get_free_user(currency_code, category)

    @keyword
    def return_user(self, user):
        """
        Returns an ACTIVE user to the user pool and sets it back to FREE.

        - param ``user``: user object to return to the user pool
        - return: count of record updated
        """
        if user:
            user_id = user['id']
            return self._free_user(user_id)
        raise TypeError("Cannot Return NoneType User")

    @keyword
    def get_user(self, user_id):
        """
        Returns a user given user id.

        - param ``user_id``: user id
        - return: user json object

        Example:
        | ${user}       | `Get User` | 16 |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |           }
        """
        return self._get_user(user_id)

    @keyword
    def update_user_password(self, user, new_password):
        """
        Update user password.

        - param ``user``: user json object to update
        - param ``new_password``: new password value
        - return: count of record updated

        Example:
        | ${user}   | `Get User`                | 16                    |
        | ${count}  | `Update User Password`    | ${user} | newpassword |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |           }
        | ${count} = 1
        """
        user_id = user['id']
        old_password = user['passWord']

        return self._update_user_password(user_id, old_password, new_password)

    @keyword
    def update_user_profile(self, user, email=None, mobileNo=None):
        """
        Update user profile.

        - param ``user``: user json object to update
        - param ``email``: email
        - param ``mobileNo``: mobileNo
        - return: count of record updated or raises TypeError for invalid
        email or mobile no

        Example:
        | ${user}       | `Get User`            | 16                        |
        | ${count}      | `Update User Profile` | ${user}               \
                                                | newemail              \
                                                | newmobileno               |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |             "email": null,
        |             "mobileNo": null
        |           }
        | ${count} = 1
        """
        user_id = user['id']

        return self._update_user_profile(user_id, email, mobileNo)

    def _get_free_user(self, currency_code=None, category=None):
        request_url = self.base_url + "/borrow/single"

        LOGGER.info(f'Retrying user')

        params = {'currencyCode': '',
                  'category': '',
                  'ip': self.machineIp,
                  'hostName': self.machineHostName}

        if currency_code:
            params.update({"currencyCode": currency_code})
        if category:
            category = (category.replace(' ', '')).split(',')
            params.update({"category": category})

        LOGGER.debug(f'Params {params}')

        response = requests.get(request_url, params=params)
        response.raise_for_status()

        json_response = response.json()
        LOGGER.debug(f'Retrieved free user {json_response}')

        if bool(json_response):
            return json_response

        raise Exception('No user found')

    def _free_user(self, user_id):
        request_url = self.base_url + "/return/single/" + str(user_id)

        response = requests.post(request_url)
        response.raise_for_status()

        return response.text

    def _update_user_password(self, user_id, old_password, new_password):
        request_url = self.base_url + "/update/password/" + str(user_id)

        headers = {'Content-Type': 'application/json'}
        payload = {'oldPassword': old_password, 'newPassword': new_password}

        response = requests.post(request_url,
                                 headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()

        return response.text

    def _update_user_profile(self, user_id, email=None, mobileNo=None):
        request_url = self.base_url + "/update/info/" + str(user_id)

        headers = {'Content-Type': 'application/json'}

        payload = {}
        if email:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                payload.update({'email': email})
            else:
                raise TypeError("Invalid email")
        if mobileNo:
            if re.match(r"\d{10}$", mobileNo):
                payload.update({'mobileNo': mobileNo})
            else:
                raise TypeError("Invalid mobile number")

        response = requests.post(request_url,
                                 headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()

        return response.text

    def _get_user(self, user_id):
        request_url = self.base_url + "/get/user/" + str(user_id)

        response = requests.get(request_url)
        response.raise_for_status()

        json_response = response.json()
        LOGGER.debug(f'Retrieved free user {json_response}')

        if bool(response):
            return json_response

        return None

    def _get_machine_hostname(self):
        """Uses python 3 socket library to get the machine IP and hostname.
        """
        try:
            hostName = socket.gethostname()
            return hostName
        except Exception as err:
            raise err

    def _append_test_trigger_category(self):
        """Appends test trigger category to machine hostname.
        """
        if environ.get('CI_RUNNER_DESCRIPTION') is not None:
            hostName = environ.get('CI_RUNNER_DESCRIPTION')
        else:
            hostName = self._get_machine_hostname()
        return hostName[:50] if len(hostName) > 50 else hostName

    def _get_machine_ip(self, hostName=None):
        """Uses python 3 socket library to obtain machine IP Address.
        Takes machine hostName as parameter
        """
        try:
            hostIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hostIp.connect(("8.8.8.8", 80))
            sockname = hostIp.getsockname()[0]
            hostIp.close()
            return sockname
        except Exception as err:
            raise err
