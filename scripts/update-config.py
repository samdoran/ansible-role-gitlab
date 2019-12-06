#!/usr/bin/env python

import os
import sys
import urllib.request

url = u'https://gitlab.com/gitlab-org/omnibus-gitlab/raw/master/files/gitlab-config-template/gitlab.rb.template'
urllib.request.urlretrieve(url, 'gitlab.rb')
