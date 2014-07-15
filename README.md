GitLab Omnibus
========

Install GitLab Omnibus edition

Requirements
------------

CentOS 6
SSL private and public keys
Postfix installed and configured to relay mail properly
Ports 80 and 443 open in firewall

Role Variables
--------------

**gitlab_version**      Version of Gitlab. Also used to determine if an update is needed.

**ssl_cert_path**       Where Gitlab SSL certs are stored

**gitlab_ssl_crt**      Public key

**gitlab_ssl_key**      Private key. I recommend putting this in an ansible vault