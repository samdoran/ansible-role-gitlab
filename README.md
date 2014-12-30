GitLab Omnibus
========
[![Galaxy](https://img.shields.io/badge/galaxy-sdoran.gitlab-blue.svg?style=flat)](https://galaxy.ansible.com/list#/roles/1759)

The role will install GitLab Omnibus CE or update GitLab if `gitlab_version` does not match the installed version.

There is a cron job that creates daily backups of the database and another cron job that deletes backups older than `gitlab_days_old_backups` days.

To only run update tasks, run `ansible-playbook site.yml --tags gitlabupdate`.

With the addition of GitLab CI, there are more variables that should bo configured before running the role. GitLab CI is disabled by default, but if you enable it and plan to use SSL (which you should), you will also need to look at and/or define the following variables:

```shell
gitalb_ci_enabled
gitalb_ci_fqdn
gitlab_ci_nginx_ssl_filename
gitlab_ci_nginx_ssl_crt
gitlab_ci_nginx_ssl_key
```

It is possible to use the same SSL certificates for both listeners (if you are using a wildcard cert, for example) by setting `gitlab_ci_nginx_ssl_filename` to `"{{ gitlab_nginx_ssl_filename }}"` (double quotes are needed.)

Requirements
------------

* CentOS 6
* SSL private and public keys if using SSL
* Postfix installed and configured to relay mail properly
* Ports 80 and 443 open in firewall

Role Variables
--------------

**Note:** Variable names have changed. `gitlab_ssl_*` is now `gitlab_nginx_ssl_*` and `gitlab_ci_ssl_*` is now `gitlab_ci_nginx_ssl_*`.

#### GitLab Variables  ####

There are now far to many variable to describe each individually. I recommend looking through `defaults/main.yml` to see all available options and some useful links for further information.

Here are the variables you will most likely need to set.

**gitlab_version**: Version of GitLab to install. Also used to determine if an update is needed.

**gitlab_days_old_backups**: Passed to `find -time +[n]` in cron job that deletes GitLab backups (Default: 10)

**gitlab_nginx_ssl_enabled**: Whether or not to configure GitLab to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_nginx_ssl_crt` and `gitlab_nginx_ssl_key`. (Default: False)

**gitlab_nginx_redirect_http_to_https**: Whether or not to redirect HTTP to HTTPS (Default: False)

**gitlab_nginx_ssl_cert_path**: Directory where Gitlab SSL certs are stored (Default: /etc/pki/tls/certs/)

**gitlab_nginx_ssl_key_path**: Directory where Gitlab SSL certificate keys are stored (Default: /etc/pki/tls/private/)

**gitlab_nginx_ssl_filename**: What the SSL certificate and key files will be named. A `.crt` extension is used for the public cert, a `.key` extension is used for the private key. (Default: {{ ansibl_fqdn }})

**gitlab_nginx_ssl_port**: Listening port for HTTPS (Default: 443)

**gitlab_nginx_ssl_crt**: SSL Public key. Look at `defaults/main.yml` for an example of how to store this in a variable.

**gitlab_nginx_ssl_key**: SSL Private key. Look at `defaults/main.yml` for an example of how to store this in a variable. I recommend putting this in an ansible vault

#### GitLab CI Variables ####

These are the same variables as above but with a `gitlab_ci_` prefix.

**gitlab_ci_enabled**: Whether or not to enable GitLab CI (Default: False)

**gitlab_ci_fqdn**: FQDN of GitLab CI host (Default: ci.{{ ansible_domain }})

**gitlab_ci_nginx_ssl_enabled**: Whether or not to configure GitLab CI to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_ci_nginx_ssl_crt` and `gitlab_ci_nginx_ssl_key`. (Default: False)

**gitlab_ci_nginx_redirect_http_to_https**: Whether or not to redirect HTTP to HTTPS (Default: False)

**gitlab_ci_nginx_ssl_cert_path**: Directory where Gitlab CI  SSL certs are stored (Default: {{ gitlab_nginx_ssl_cert_path }})

**gitlab_ci_nginx_ssl_key_path**: Directory where Gitlab CI SSL certificate keys are stored (Default: {{ gitlab_nginx_ssl_key_path }})

**gitlab_ci_nginx_ssl_filename**: Name of GitLab CI certificate files. A `.crt` extension is used for the public cert, a `.key` extension is used for the private key. (Default: gitlab_ci_fqdn)

**gitlab_ci_nginx_ssl_port**: Listening port for GitLab CI HTTPS (Default: 443)

**gitlab_ci_nginx_ssl_crt**: Public certificate used for GitLab CI server (Default: undefined)

**gitlab_ci_nginx_ssl_key**: Private key used for GitLab CI server (Default: undefined)


Example Playbooks
----------------
Setup GitLab using SSL.
```yaml
- hosts: gitlab
  sudo: yes

  vars:
     gitlab_version: 7.2.2_omnibus-1
     gitlab_days_old_backups: 7

     gitlab_nginx_ssl_crt: "{{ ssl_cert_stored_in_vault }}"
     gitlab_nginx_ssl_key: "{{ ssl_key_stored_in_vault }}"

  roles:
     - role: sdoran.gitlab
```

Setup GitLab and GitLab CI using SSL with a shared certificate. Also redirect HTTP to HTTPS and set a custom FQDN for the CI server.
```yaml
- hosts: gitlab
  sudo: yes

  vars:
    gitlab_version: 7.2.2_omnibus-1
    gitlab_days_old_backups: 7

    gitlab_nginx_ssl_crt: "{{ ssl_cert_stored_in_vault }}"
    gitlab_nginx_ssl_key: "{{ ssl_key_stored_in_vault }}"
    gitlab_nginx_ssl_filename: "gitlab_{{ ansible_domain }}"
    gitlab_nginx_redirect_http_to_https: True

    gitlab_ci_enabled: True
    gitlab_ci_fqdn: "gitlab-ci.{{ ansible_domain }}"
    gitlab_ci_nginx_ssl_crt: "{{ gitlab_nginx_ssl_crt }}"
    gitlab_ci_nginx_ssl_key: "{{ gitlab_nginx_ssl_key }}"
    gitlab_ci_ssl_filename: "{{ gitlab_nginx_ssl_filename }}"
    gitlab_ci_nginx_redirect_http_to_https: True

  roles:
    - role: sdoran.gitlab
```

License
-------

MIT
