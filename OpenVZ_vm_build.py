#!/usr/bin/env python

import urllib2
import os
import subprocess
from sys import argv as sysarg

global php_version, container_type

def run (vzid, vzip, vzhostname, php_version, container_type):
#       get_template(php_version, container_type)
        if create_container (vzid, vzip, vzhostname, php_version, container_type):
                print ("Well done")
        else:
                print ("Something goes wrong")

def create_container(vzid, vzip, vzhostname, php_version, container_type):
        template = 'debian' + php_version + container_type
        create_vz = subprocess.Popen (['vzctl', 'create', vzid, '--ostemplate', template, '--ipadd', vzip, '--hostname', vzhostname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = create_vz.communicate(b"input data that is passed to subprocess' stdin")
        retcode = create_vz.returncode
        print('OUTPUT', output)
        print ('ERROR', err)
        print ('Return Code', retcode)
        if retcode:
                return False
        else:
                return True
                
def get_template(php_version, container_type):
        template_path="/var/lib/vz/template/cache/"
        template_name=template_path+'debian'+php_version+container_type+'.tar.gz'
        if not os.path.exists (template_name):
                subprocess.call ('scp  dola@titan30:{0} {1}'.format(template_name, template_path), shell=True)

if __name__ == "__main__":
        run(sysarg[1], sysarg[2], sysarg[3], sysarg[4], sysarg[5])
