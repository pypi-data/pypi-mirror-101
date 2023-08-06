**Encryption at rest made easy**

cf-crypt is a package to help you keep all you data resting on disk
secure. It make encrypting your data at rest as easy as reading and
writing from a file.

   >>> from cfcrypt import CryptFileTextIO
   >>> with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:
   ...         fh.write('Super secret, secret squirrel plans.')


Install
*******

Install the package from pypi.org/project/cf-crypt using "pip"

   $ python -m pip install cf-crypt
   [...]
   Successfully installed cf-crypt


Quick Start
***********


Generate Keys
=============

These keys are generated securely in memory.

Like all in memory variables they will disappear when your script
ends. We really need our keys to stick around for as long as we want
to decrypt our data.

   >>> from cfcrypt.rsa.key_helpers import generate_private_key
   >>> encryption_key = generate_private_key()
   >>> identity_key = generate_private_key()


Save Keys
=========

Keys can be serialized to the PEM format and saved to disk.

   >>> from cfcrypt.rsa.key_helpers import private_key_to_pem_file
   >>> private_key_to_pem_file('./my_encryption_key.pem', encryption_key)
   >>> private_key_to_pem_file('./my_identity_key.pem', identity_key)

These *PEM* files are quite literally the keys to your data.


Load Keys
=========

If you set a password on the *PEM* files you will need it to load them
from disk.

   >>> from cfcrypt.rsa.key_helpers import pem_file_to_private_key
   >>> encryption_key = pem_file_to_private_key('./my_encryption_key.pem')
   >>> identity_key = pem_file_to_private_key('./my_identity_key.pem')


Encrypt
=======

Encryption is really easy, just use "CryptFileTextIO" like a regular
file interface.

   >>> from cfcrypt import CryptFileTextIO
   >>> with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:
   ...         fh.write('Super secret, secret squirrel plans.')


Decrypt
=======

Decryption is also really easy, just use "CryptFileTextIO" like a
regular file interface.

   >>> from cfcrypt import CryptFileTextIO
   >>> with CryptFileTextIO('./my_file.crpt', 'r', encryption_key, identity_key) as fh:
   ...     data = fh.read()
   >>> data
   'Super secret, secret squirrel plans.'


More...
*******

There are a bunch of other useful encryption related tools in the
module. See the documentation (cf-crypt.readthedocs.io/en/latest) for
details.

   * String encryption

   * Python object serialization + encryption

   * RSA signing & verification

   * File & folder encryption

   * Key management.
