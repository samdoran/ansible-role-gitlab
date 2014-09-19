GitLab Omnibus
========

Install GitLab CE Omnibus on CentOS 6.
The role will update GitLab if `gitlab_version` does not match the installed version.
There is a cron job that creates daily backups of the database and another cron job that deletes backups older than `gitlab_days_old_backups` days.

Requirements
------------

* CentOS 6
* SSL private and public keys
* Postfix installed and configured to relay mail properly
* Ports 80 and 443 open in firewall

Role Variables
--------------

**gitlab_version**      Version of Gitlab. Also used to determine if an update is needed.

**gitlab_ssl_cert_path**       Where Gitlab SSL certs are stored

**gitlab_ssl_filename**     What the ssl certificate and key files will be named. A ".crt" extension is used for the public cert, a ".key" extension is used for the private cert. (Default: {{ ansibl_fqdn }})

**gitlab_ssl_crt**      Public key

**gitlab_ssl_key**      Private key. I recommend putting this in an ansible vault

**gitlab_git_data_dir** Directroy for GitLab data (Default: /var/opt/gitlab/git-data)

**gitlab_user**         User account used by GitLab gitlab-shell login, ownership of the Git data itself, and SSH URL generation on the web interface (Default: git)

**gitlab_group**        Group used by GitLab for  group ownership of the Git data (Default: git)

**gitlab_days_old_backups** Passed to `find -time +[n]` in cron job that deletes GitLab backups (Default: 10)

**gitlab_ldap_enabled**         Whether to enable LDAP authentication (Default: false)

**gitlab_ldap_host**            IP or name of LDAP server (Default: _your_ldap_server)

**gitlab_ldap_port**            LDAP port (Default: 636)

**gitlab_ldap_uid**             SAM account used to authenticate to LDAP server (Default: SAMAccountName)

**gitlab_ldap_method**          'ssl' or 'plain' connection method to LDAP server (Default: ssl)

**gitlab_ldap_bind_dn**         Full DN of user that will bind to LDAP server (Default: _the_full_dn_of_the_user_you_will_bind_with)

**gitlab_ldap_password**        Password of the bind user (Default: _the_password_of_the_bind_user)

**gitlab_ldap_allow_username_or_email_login**       If you are using "uid: 'userPrincipalName'" on ActiveDirectory you need to disable this setting, because the userPrincipalName contains an '@'. (Default: true)

**gitlab_ldap_base**            Base where we can search for users. Ex. ou=People,dc=gitlab,dc=example (Default: '')


Example Playbook
----------------

    - hosts: servers

      vars:
         gitlab_version: 7.2.2_omnibus-1
         gitlab_days_old_backups: 7

      roles:
         - role: sdoran.gitlab


License
-------

MIT
