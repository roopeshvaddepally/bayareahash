from fabric.api import env, put, run, local
from fabric.context_managers import cd

#EC2 access information
env.hosts = ['107.21.101.188']
env.user = 'ec2-user'
env.key_filename = '/Users/zengr/dev/amazon/zengr.pem'

remote_temp_path = "/tmp"
remote_web =  "/var/www/"

local_temp_path = "/tmp/"
local_web = "/Users/zengr/dev/python/bayareahash"

def deploy_web():
    '''Deployment of the flask webapp'''
    local("cp -R " + local_web + " " + local_temp_path)
    local("rm -rf /tmp/bayareahash/.git");
    local("rm -rf /tmp/bayareahash/*.pyc");
    put(local_temp_path + "/bayareahash", remote_temp_path)

    with cd(remote_temp_path):
        run('sudo cp -R bayareahash/ /var/www/flaskapps/')
        clean()
    with cd('/var/www/'):
        run('sudo chown -R apache flaskapps')

def clean():
    run('sudo rm -rf bayareahash')

def restart_services():
    run('sudo /etc/init.d/httpd stop')
    run('sudo /etc/init.d/httpd start')

def deploy():
    deploy_web()
    restart_services()
