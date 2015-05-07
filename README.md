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

Version of GitLab to install. Also used to determine if an update is needed.

    gitlab_version: 7.8.2_omnibus.1-1

Passed to `find -time +[n]` in cron job that deletes GitLab backups

    gitlab_days_old_backups: 10

FQDN of GitLab host

    gitlab_fqdn: "{{ ansible_fqdn }}"

Whether or not to configure GitLab to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_nginx_ssl_crt` and `gitlab_nginx_ssl_key`. If `gitlab_nginx_ssl_crt` or `gitlab_nginx_ssl_key` are defined, SSL will be enabled.

    gitlab_nginx_ssl_enabled: False

Whether or not to redirect HTTP to HTTPS.

    gitlab_nginx_redirect_http_to_https: False

Directory where Gitlab SSL certs are stored.

    gitlab_nginx_ssl_cert_path: /etc/pki/tls/certs/

Directory where Gitlab SSL certificate keys are stored.

    gitlab_nginx_ssl_key_path: /etc/pki/tls/private/


What the SSL certificate and key files will be named. A `.crt` extension is used for the public cert, a `.key` extension is used for the private key.

    gitlab_nginx_ssl_filename: "{{ ansible_fqdn }}"

Listening port for HTTPS.

    gitlab_nginx_ssl_port: 443

SSL Public certificate.

    gitlab_nginx_ssl_crt: |
      -----BEGIN CERTIFICATE-----
      public cert goes here
      -----END CERTIFICATE-----

SSL Private key. I recommend putting this in an ansible vault.

    gitlab_nginx_ssl_key: |
      -----BEGIN RSA PRIVATE KEY-----
      private cert goes here
      -----END RSA PRIVATE KEY-----

#### GitLab CI Variables ####

**Note:** In GitLab 7.8, GitLab CI now uses OAuth for authentication. Here is the rough procedure for setting it up:

  1. Install GitLab
  1. Follow the instructions on the GitLab CI login page to generate an OAuth token for GitLab CI
  1. Put those values in the appropriate variables
  1. Run the playbook with `--tags gitlabrb` in order to update the template and reconfigure GitLab.

These are the same variables as above but with a `gitlab_ci_` prefix.

Whether or not to enable GitLab CI.

    gitlab_ci_enabled: False

FQDN of GitLab CI host

    gitlab_ci_fqdn: "ci.{{ ansible_domain }}"

Whether or not to configure GitLab CI to use SSL. This is meant to be used when the SSL certificates are installed using an additional role and not defined inside `gitlab_ci_nginx_ssl_crt` and `gitlab_ci_nginx_ssl_key`.

    gitlab_ci_nginx_ssl_enabled: False

Whether or not to redirect HTTP to HTTPS

    gitlab_ci_nginx_redirect_http_to_https: False

Directory where Gitlab CI  SSL certs are stored

    gitlab_ci_nginx_ssl_cert_path: "{{ gitlab_nginx_ssl_cert_path }}"

Directory where Gitlab CI SSL certificate keys are stored

    gitlab_ci_nginx_ssl_key_path: "{{ gitlab_nginx_ssl_key_path }}"

Name of GitLab CI certificate files. A `.crt` extension is used for the public cert, a `.key` extension is used for the private key.

    gitlab_ci_nginx_ssl_filename: "{{ gitlab_ci_fqdn }}"

Listening port for GitLab CI HTTPS

    gitlab_ci_nginx_ssl_port: 443

Public certificate used for GitLab CI server

    gitlab_ci_nginx_ssl_crt: |
      -----BEGIN CERTIFICATE-----
      public cert goes here
      -----END CERTIFICATE-----

Private key used for GitLab CI server

    gitlab_ci_nginx_ssl_key: |
      -----BEGIN RSA PRIVATE KEY-----
      private cert goes here
      -----END RSA PRIVATE KEY-----

OAuth token configuration for GitLab CI.

    gitlab_ci_gitlab_server:
      url: "https://{{ ansible_fqdn }}"
      app_id: '066527ae25ce2fe21831a44f0840a7f0c3f94de6ad593425b04080f929a5c887'
      app_secret: '35bc899dd1e48ac84b8f5b776106c55639842549fab48e55669badb087756077'

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

    gitlab_ci_gitlab_server:
      url: "https://{{ ansible_fqdn }}"
      app_id: '066527ae25ce2fe21831a44f0840a7f0c3f94de6ad593425b04080f929a5c887'
      app_secret: '35bc899dd1e48ac84b8f5b776106c55639842549fab48e55669badb087756077'

  roles:
    - role: sdoran.gitlab
```

License
-------

MIT
