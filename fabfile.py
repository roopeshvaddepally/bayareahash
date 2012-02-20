from fabric.api import env, put, run, local
from fabric.context_managers import cd

#EC2 access information
env.hosts = ['107.21.101.188']
env.user = 'ec2-user'
env.key_filename = '/Users/zengr/dev/amazon/zengr.pem'

temp_path = "/tmp"

local_web = "/Users/zengr/dev/python/bayareahash"
git_exclude = local_web + "/.git/*"

remote_web =  "/var/www/"

def deploy_web():
    '''Deployment of the flask webapp'''
    put(local_web, temp_path)
    with cd(temp_path):
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
