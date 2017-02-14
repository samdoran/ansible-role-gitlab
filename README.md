GitLab Community Edition
========
[![Build Status](https://travis-ci.org/samdoran/ansible-role-gitlab.svg?branch=master)](https://travis-ci.org/samdoran/ansible-role-gitlab)
[![Galaxy](https://img.shields.io/badge/galaxy-samdoran.gitlab-blue.svg?style=flat)](https://galaxy.ansible.com/samdoran/gitlab)

The role will install the latest version of GitLab CE from the official repositories.

There is a cron job that creates daily backups of the database and another cron job that deletes backups older than `gitlab_days_old_backups` days.

To only run update tasks, run `ansible-playbook site.yml --tags gitlabupdate`.

Requirements
------------

* SSL private and public keys if using SSL
* Postfix installed and configured to relay mail properly
* Ports 80 and 443 open in firewall

Role Variables
--------------

#### GitLab Variables  ####

There are now far too many variable to describe each individually. I recommend looking through `defaults/main.yml` to see all available options and some useful links for further information.

Here are the variables you will most likely need to set.

| Name           | Default                     | Description                |
|----------------|-----------------------------|----------------------------|
| `gitlab_version` | `[undefined]` | If defined, install a specific version of GitLab. If undefined, install the latest version. This needs to be a string, so be sure to wrap it in double quotes. |
| `gitlab_version_suffix` | `-ce.0` | **Debian only** When specifying `gitlab_version`, an additional suffix is needed. To see valid suffixes, run `aptitude versions gitlab-ce`. Since GitLab 8, the suffix is always `-ce.[012]`. |
|  `gitlab_days_old_backups` | 10 | Passed to `find -time +[n]` in cron job that deletes GitLab backups |
| `gitlab_fqdn` | `"{{ ansible_fqdn }}"` | FQDN of GitLab host |
| `gitlab_nginx_ssl_enabled` | False | Whether or not to configure GitLab to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_nginx_ssl_crt` and `gitlab_nginx_ssl_key`. If `gitlab_nginx_ssl_crt` or `gitlab_nginx_ssl_key` are defined, SSL will be enabled |
| `gitlab_nginx_redirect_http_to_https` | False | Whether or not to redirect HTTP to HTTPS. |
| `gitlab_nginx_ssl_cert_path` | `/etc/pki/tls/certs/` | Directory where GitLab SSL certs are stored. |
| `gitlab_nginx_ssl_key_path` | `/etc/pki/tls/private/` | Directory where GitLab SSL certificate keys are stored. |
| `gitlab_nginx_ssl_filename` | `"{{ ansible_fqdn }}"` | What the SSL certificate and key files will be named. A `.crt` extension is used for the public cert, a `.key` extension is used for the private key. |
| `gitlab_nginx_ssl_port` | 443 | Listening port for HTTPS. |
| `gitlab_nginx_ssl_crt` | Undefined multi-line variable | SSL Public certificate. |
| `gitlab_nginx_ssl_key` | Undefined multi-line variable | SSL Private key. I recommend putting this in an ansible vault. |

#### GitLab CI Variables ####

**Note:** In GitLab 7.8, GitLab CI now uses OAuth for authentication. Here is the rough procedure for setting it up:

  1. Install GitLab
  1. Follow the instructions on the GitLab CI login page to generate an OAuth token for GitLab CI
  1. Put those values in the appropriate variables
  1. Run the playbook with `--tags gitlabrb` in order to update the template and reconfigure GitLab.


Example Playbooks
----------------
Setup GitLab using SSL.
```yaml
- hosts: gitlab
  become: yes

  vars:
     gitlab_days_old_backups: 7

     gitlab_nginx_ssl_crt: "{{ ssl_cert_stored_in_vault }}"
     gitlab_nginx_ssl_key: "{{ ssl_key_stored_in_vault }}"

  roles:
     - role: samdoran.gitlab
```

Install a specific version of GitLab.
```yaml
- hosts: gitlab
  become: yes

  vars:
     gitlab_version: "8.6.9"
     gitlab_version_suffix: "-ce.2"

  roles:
     - role: samdoran.gitlab
```

License
-------

MIT
