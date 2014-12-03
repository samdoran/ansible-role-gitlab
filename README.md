GitLab Omnibus
========

Install GitLab CE Omnibus on CentOS 6.

The role will update GitLab if `gitlab_version` does not match the installed version.

There is a cron job that creates daily backups of the database and another cron job that deletes backups older than `gitlab_days_old_backups` days.

To only run update tasks, run `ansible-playbook site.yml --tags gitlabupdate`.

With the addition of GitLab CI, there are more variables that should bo configured before running the role. GitLab CI is disabled by default, but if you enable it and plan to use SSL (which you should), you will also need to look at and/or define the following variables:

    gitalb_ci_enabled
    gitalb_ci_fqdn
    gitalb_ci_ssl_filename
    gitlab_ci_ssl_crt
    gitlab_ci_ssl_key

It is possible to use the same SSL certificates for both listeners (if you are using a wildcard cert, for example) by setting `gitlab_ci_ssl_filename` to `"{{ gitlab_ssl_filename }}"` (double quotes are needed.)

Requirements
------------

* CentOS 6
* SSL private and public keys
* Postfix installed and configured to relay mail properly
* Ports 80 and 443 open in firewall

Role Variables
--------------

**gitlab_version**      Version of Gitlab. Also used to determine if an update is needed.

**gitlab_ssl_enabled** Whether or not to configure GitLab to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_ssl_crt` and `gitlab_ssl_key`. (Default: False)

**gitlab_redirect_http**    Whether or not to redirect HTTP to HTTPS (Default: False)

**gitlab_ssl_cert_path**       Where Gitlab SSL certs are stored

**gitlab_ssl_filename**     What the ssl certificate and key files will be named. A ".crt" extension is used for the public cert, a ".key" extension is used for the private cert. (Default: {{ ansibl_fqdn }})

**gitlab_ssl_port**     Listening port for HTTPS (Default: 443)

**gitlab_ssl_crt**      Public key

**gitlab_ssl_key**      Private key. I recommend putting this in an ansible vault

**gitlab_git_data_dir** Directroy for GitLab data (Default: /var/opt/gitlab/git-data)

**gitlab_user**         User account used by GitLab gitlab-shell login, ownership of the Git data itself, and SSH URL generation on the web interface (Default: git)

**gitlab_group**        Group used by GitLab for  group ownership of the Git data (Default: git)

**gitlab_days_old_backups** Passed to `find -time +[n]` in cron job that deletes GitLab backups (Default: 10)

**gitlab_ldap_enabled**         Whether to enable LDAP authentication (Default: false)

**gitlab_ldap_label**         A human-friendly name for your LDAP server. (Default: LDAP)

**gitlab_ldap_host**            IP or name of LDAP server (Default: _your_ldap_server)

**gitlab_ldap_port**            LDAP port (Default: 636)

**gitlab_ldap_uid**             SAM account used to authenticate to LDAP server (Default: SAMAccountName)

**gitlab_ldap_method**          'ssl' or 'plain' connection method to LDAP server (Default: ssl)

**gitlab_ldap_bind_dn**         Full DN of user that will bind to LDAP server (Default: _the_full_dn_of_the_user_you_will_bind_with)

**gitlab_ldap_password**        Password of the bind user (Default: _the_password_of_the_bind_user)

**gitlab_ldap_ad**        This setting specifies if LDAP server is Active Directory LDAP server. If your LDAP server is not AD, set this to False. (Default: True)

**gitlab_ldap_allow_username_or_email_login**       If you are using "uid: 'userPrincipalName'" on ActiveDirectory you need to disable this setting, because the userPrincipalName contains an '@'. (Default: true)

**gitlab_ldap_base**            Base where we can search for users. Ex. ou=People,dc=gitlab,dc=example (Default: '')

**gitlab_ldap_user_filter**   Filter LDAP users. Format: RFC 4515 http://tools.ietf.org/search/rfc4515. Ex. (employeeType=developer) (Default: '')

**gitlab_ci_enabled**           Whether or not to enable GitLab CI (Default: False)

**gitlab_ci_fqdn**          FQDN of GitLab CI host (Default: ci.{{ ansible_domain }})

**gitlab_ci_ssl_filename** Name of GitLab CI certificate files (Default: gitlab_ci_fqdn) 

**gitlab_ci_ssl_crt**   Public certificate used for GitLab CI server (Default: undefined)

**gitlab_ci_ssl_key**   Private key used for GitLab CI server (Default: undefined)


Example Playbook
----------------

```yaml
- hosts: gitlab
  sudo: yes

  vars:
     gitlab_version: 7.2.2_omnibus-1
     gitlab_days_old_backups: 7
     gitlab_ci_enabled: True
     gitlab_ci_fqdn: "gitlab-ci.{{ ansible_domain }}"
     gitlab_ci_ssl_filename: "{{ gitlab_ssl_filename }}"

  roles:
     - role: sdoran.gitlab
```

License
-------

MIT
