from collections import defaultdict
from datetime import date, datetime, timedelta
import os
import pickle
import simplejson
import sys
import time

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *
from src.console import *
from src.dash import *


def pickle_aws(request, name):
    f = open('%s/cache/aws/%s_%s_%s.pickle' % (MEDIA_ROOT, request['tp'], name, request['qs']), 'wb')
    pickle.dump(cache_aws(request), f)
    f.close()

def pickle_git(request):
    f = open('%s/cache/git/%s_%s.pickle' % (MEDIA_ROOT, request['repo'], request['qs']), 'wb')
    pickle.dump(cache_git(request), f)
    f.close()

def pickle_slack(request):
    f = open('%s/cache/slack/%s.pickle' % (MEDIA_ROOT, request['qs']), 'wb')
    pickle.dump(cache_slack(request), f)
    f.close()

def pickle_dropbox(request):
    f = open('%s/cache/dropbox/%s.pickle' % (MEDIA_ROOT, request['qs']), 'wb')
    pickle.dump(cache_dropbox(request), f)
    f.close()


def main():
    t0 = time.time()
    print time.ctime()
    t = time.time()

    # schedule
    print "#6: Requesting Schedule Spreadsheet..."
    f = open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'wb')
    pickle.dump(cache_schedule(), f)
    f.close()
    print "    Schedule finished."

    # cal
    print "#7: Requesting Google Calendar..."
    f = open('%s/cache/calendar.pickle' % MEDIA_ROOT, 'wb')
    pickle.dump(cache_cal(), f)
    f.close()
    print "    Calendar finished."

    # aws init
    print "#1: Requesting AWS..."
    request = {'qs':'init'}
    aws_init = cache_aws(request)
    f = open('%s/cache/aws/init.pickle' % MEDIA_ROOT, 'wb')
    pickle.dump(aws_init, f)
    f.close()
    aws_init = simplejson.loads(aws_init)
    print "    AWS init finished."

    # aws each
    for i, ec2 in enumerate(aws_init['ec2']):
        print "    AWS EC2: %s / %s (%s)..." % (i + 1, len(aws_init['ec2']), ec2['id'])
        request = {'qs':'cpu', 'tp':'ec2', 'id':ec2['id']}
        pickle_aws(request, ec2['id'])
        request.update({'qs':'net'})
        pickle_aws(request, ec2['id'])

    for i, elb in enumerate(aws_init['elb']):
        print "    AWS ELB: %s / %s (%s)..." % (i + 1, len(aws_init['elb']), elb['name'])
        request = {'qs':'lat', 'tp':'elb', 'id':elb['name']}
        pickle_aws(request, elb['name'])
        request.update({'qs':'req'})
        pickle_aws(request, elb['name'])

    for i, ebs in enumerate(aws_init['ebs']):
        print "    AWS EBS: %s / %s (%s)..." % (i + 1, len(aws_init['ebs']), ebs['id'])
        request = {'qs':'disk', 'tp':'ebs', 'id':ebs['id']}
        pickle_aws(request, ebs['id'])

    # ga
    print "#2: Requesting GA..."
    f = open('%s/cache/ga.pickle' % MEDIA_ROOT, 'wb')
    pickle.dump(cache_ga(), f)
    f.close()
    print "    GA init finished."

    # git init
    print "#3: Requesting GIT..."
    request = {'qs':'init'}
    git_init = cache_git(request)
    f = open('%s/cache/git/init.pickle' % MEDIA_ROOT, 'wb')
    pickle.dump(git_init, f)
    f.close()
    git_init = simplejson.loads(git_init)
    print "    GIT init finished."

    # git each
    for i, repo in enumerate(git_init['git']):
        print "    GIT repo: %s / %s (%s)..." % (i + 1, len(git_init['git']), repo['name'])
        request = {'qs':'num', 'repo':repo['name']}
        pickle_git(request)
        request.update({'qs':'c'})
        pickle_git(request)
        request.update({'qs':'ad'})
        pickle_git(request)

    # slack
    print "#4: Requesting SLACK..."
    requests = ['users', 'channels', 'files', 'plot_files', 'plot_msgs', 'home']
    for i, request in enumerate(requests):
        print "    SLACK: %s / %s (%s)..." % (i + 1, len(requests), request)
        request = {'qs':request}
        git_init = cache_slack(request)
        pickle_slack(request)

    # dropbox
    print "#5: Requesting DROPBOX..."
    requests = ['sizes', 'folders', 'history']
    for i, request in enumerate(requests):
        print "    DROPBOX: %s / %s (%s)..." % (i + 1, len(requests), request)
        request = {'qs':request}
        git_init = cache_dropbox(request)
        pickle_dropbox(request)


    print "Time elapsed: %.1f s." % (time.time() - t)
    print


if __name__ == "__main__": 
    main()

# flag = False
# print "#1: Backing up MySQL database..."
# try:
#     subprocess.check_call('mysqldump --quick %s -u %s -p%s > %s/backup/backup_mysql' % (env.db()['NAME'], env.db()['USER'], env.db()['PASSWORD'], MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     subprocess.check_call('gzip -f %s/backup/backup_mysql' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# except subprocess.CalledProcessError:
#     print "    \033[41mERROR\033[0m: Failed to dump \033[94mMySQL\033[0m database."
#     print traceback.format_exc()
#     flag = True
# else:
#     print "    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database dumped."
# print "Time elapsed: %.1f s." % (time.time() - t)

# t = time.time()
# print "#2: Backing up static files..."
# try:
#     subprocess.check_call('cd %s && tar zcf backup/backup_static.tgz data/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# except subprocess.CalledProcessError:
#     print "    \033[41mERROR\033[0m: Failed to archive \033[94mstatic\033[0m files."
#     print traceback.format_exc()
#     flag = True
# else:
#     print "    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files synced."
# print "Time elapsed: %.1f s." % (time.time() - t)

# t = time.time()
# print "#3: Backing up apache2 settings..."
# try:
#     subprocess.check_call('cp -r /etc/apache2 %s/backup' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     subprocess.check_call('cd %s/backup && tar zcf backup_apache.tgz apache2/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# except subprocess.CalledProcessError:
#     print "    \033[41mERROR\033[0m: Failed to archive \033[94mapache2\033[0m settings."
#     print traceback.format_exc()
#     flag = True
# else:
#     print "    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings saved."

# if flag:
#     print "Finished with errors!"
#     print "Time elapsed: %.1f s." % (time.time() - t0)
#     sys.exit(1)
# else:
#     print "All done successfully!"
#     print "Time elapsed: %.1f s." % (time.time() - t0)
#     sys.exit(0)
