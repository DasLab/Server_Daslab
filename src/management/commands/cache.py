import pickle
import simplejson
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import *
from src.dash import *


class Command(BaseCommand):
    help = 'Caches Dashboard information on an 3/15/30 minutes interval. Cache files are saved to cache/. Existing files will be overwritten.'

    def pickle_aws(self, request, name):
        f_name = '%s/cache/aws/%s_%s_%s.pickle' % (MEDIA_ROOT, request['tp'], name, request['qs'])
        pickle.dump(cache_aws(request), open(f_name + '_tmp', 'wb'))
        subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def pickle_ga(self, request):
        f_name = '%s/cache/ga/%s_%s.pickle' % (MEDIA_ROOT, request['id'], request['qs'])
        pickle.dump(cache_ga(request), open(f_name + '_tmp', 'wb'))
        subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def pickle_git(self, request):
        f_name = '%s/cache/git/%s_%s.pickle' % (MEDIA_ROOT, request['repo'].replace('/', '+'), request['qs'])
        pickle.dump(cache_git(request), open(f_name + '_tmp', 'wb'))
        subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def pickle_slack(self, request):
        if request['qs'] in ['plot_files', 'plot_msgs']:
            f_name = '%s/cache/slack/%s.pickle' % (MEDIA_ROOT, request['qs'])
            pickle.dump(cache_slack(request), open(f_name + '_tmp', 'wb'))
        else:
            f_name = '%s/cache/slack/%s.json' % (MEDIA_ROOT, request['qs'])
            result = cache_slack(request)
            if result:
                simplejson.dump(result, open(f_name + '_tmp', 'wb'), sort_keys=True, indent=' ' * 4)
            else:
                return
        subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def pickle_dropbox(self, request):
        if request['qs'] == 'history':
            f_name = '%s/cache/dropbox/%s.pickle' % (MEDIA_ROOT, request['qs'])
            pickle.dump(cache_dropbox(request), open(f_name + '_tmp', 'wb'))
        else:
            f_name = '%s/cache/dropbox/%s.json' % (MEDIA_ROOT, request['qs'])
            simplejson.dump(cache_dropbox(request), open(f_name + '_tmp', 'wb'), sort_keys=True, indent=' ' * 4)
        subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    def add_arguments(self, parser):
        parser.add_argument('--item', nargs='+', type=int, help='List of interval items, choose from (3, 15, 30).')

    def handle(self, *args, **options):
        if not BOT['CACHE']['IS_CACHE']: return
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))

        if options['item']:
            is_3 = 3 in options['item']
            is_15 = 15 in options['item']
            is_30 = 30 in options['item']
        else:
            is_3, is_15, is_30 = True, True, True

        try:
            if is_3:
                # slack
                self.stdout.write("#4: Requesting \033[94mSLACK\033[0m...")
                requests = ['home']
                for i, request in enumerate(requests):
                    self.stdout.write("    SLACK: %s / %s (%s)..." % (i + 1, len(requests), request))
                    request = {'qs': request}
                    self.pickle_slack(request)
                    self.stdout.write(" \033[92mSUCCESS\033[0m")
            else:
                self.stdout.write("#4: Skip SLACK \033[94mhome\033[0m...")


            if is_15:
                # aws init
                self.stdout.write("#1: Requesting \033[94mAWS\033[0m...")
                request = {'qs': 'init'}
                aws_init = cache_aws(request)
                simplejson.dump(aws_init, open('%s/cache/aws/init.json' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
                self.stdout.write("    AWS \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m.")

                # aws each
                for i, ec2 in enumerate(aws_init['ec2']):
                    self.stdout.write("    AWS \033[94mEC2\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['ec2']), ec2['id']), ending='')
                    request = {'qs': 'cpu', 'tp': 'ec2', 'id': ec2['id']}
                    self.pickle_aws(request, ec2['id'])
                    request.update({'qs': 'net'})
                    self.pickle_aws(request, ec2['id'])
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                for i, elb in enumerate(aws_init['elb']):
                    self.stdout.write("    AWS \033[94mELB\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['elb']), elb['name']), ending='')
                    request = {'qs': 'lat', 'tp': 'elb', 'id': elb['name']}
                    self.pickle_aws(request, elb['name'])
                    request.update({'qs': 'req'})
                    self.pickle_aws(request, elb['name'])
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                for i, ebs in enumerate(aws_init['ebs']):
                    self.stdout.write("    AWS \033[94mEBS\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['ebs']), ebs['id']), ending='')
                    request = {'qs': 'disk', 'tp': 'ebs', 'id': ebs['id']}
                    self.pickle_aws(request, ebs['id'])
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                # ga init
                self.stdout.write("#2: Requesting \033[94mGA\033[0m...")
                request = {'qs': 'init'}
                (ga_init, access_token) = cache_ga(request)
                simplejson.dump(ga_init, open('%s/cache/ga/init.json' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
                self.stdout.write("    GA \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m.")

                # ga each
                for i, ga in enumerate(ga_init['projs']):
                    self.stdout.write("    GA \033[94mtracker\033[0m: %s / %s (%s)..." % (i + 1, len(ga_init['projs']), ga['track_id']), ending='')
                    request = {'qs': 'sessions', 'id': ga['id'], 'access_token': access_token}
                    self.pickle_ga(request)
                    request.update({'qs': 'percentNewSessions'})
                    self.pickle_ga(request)
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

            else:
                self.stdout.write("#1: Skip \033[94mAWS\033[0m...")
                self.stdout.write("#2: Skip \033[94mGA\033[0m...")


            if is_30:
                # git init
                self.stdout.write("#3: Requesting \033[94mGIT\033[0m...")
                request = {'qs': 'init'}
                git_init = cache_git(request)
                simplejson.dump(git_init, open('%s/cache/git/init.json' % MEDIA_ROOT, 'w'), sort_keys=True, indent=' ' * 4)
                self.stdout.write("    GIT \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m.")

                # git each
                for i, repo in enumerate(git_init['git']):
                    self.stdout.write("    GIT \033[94mrepo\033[0m: %s / %s (%s/%s)..." % (i + 1, len(git_init['git']), repo['org'], repo['name']), ending='')
                    request = {'qs': 'num', 'repo': '%s/%s' % (repo['org'], repo['name'])}
                    self.pickle_git(request)
                    request.update({'qs': 'c'})
                    self.pickle_git(request)
                    request.update({'qs': 'ad'})
                    self.pickle_git(request)
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                # slack
                self.stdout.write("#4: Requesting \033[94mSLACK\033[0m...")
                requests = ['users', 'channels', 'files', 'plot_files', 'plot_msgs']
                for i, request in enumerate(requests):
                    self.stdout.write("    SLACK: %s / %s (%s)..." % (i + 1, len(requests), request), ending='')
                    request = {'qs': request}
                    self.pickle_slack(request)
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                # dropbox
                self.stdout.write("#5: Requesting \033[94mDROPBOX\033[0m...")
                requests = ['sizes', 'folders', 'history']
                for i, request in enumerate(requests):
                    self.stdout.write("    DROPBOX: %s / %s (%s)..." % (i + 1, len(requests), request), ending='')
                    request = {'qs': request}
                    self.pickle_dropbox(request)
                    self.stdout.write(" \033[92mSUCCESS\033[0m")

                # schedule
                self.stdout.write("#6: Requesting \033[94mSchedule Spreadsheet\033[0m...")
                f_name = '%s/cache/schedule.json' % MEDIA_ROOT
                simplejson.dump(cache_schedule(), open(f_name + '_tmp', 'w'), sort_keys=True, indent=' ' * 4)
                subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                self.stdout.write("    Schedule finished with \033[92mSUCCESS\033[0m.")

                # duty
                self.stdout.write("#7: Requesting \033[94mDuty Spreadsheet\033[0m...")
                f_name = '%s/cache/duty.json' % MEDIA_ROOT
                simplejson.dump(cache_duty(), open(f_name + '_tmp', 'w'), sort_keys=True, indent=' ' * 4)
                subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                self.stdout.write("    Duty finished with \033[92mSUCCESS\033[0m.")

                # cal
                self.stdout.write("#8: Requesting \033[94mGoogle Calendar\033[0m...")
                f_name = '%s/cache/calendar.json' % MEDIA_ROOT
                simplejson.dump(cache_cal(), open(f_name + '_tmp', 'w'), sort_keys=True, indent=' ' * 4)
                subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                self.stdout.write("    Calendar finished with \033[92mSUCCESS\033[0m.")
            else:
                self.stdout.write("#3: Skip \033[94mGIT\033[0m...")
                self.stdout.write("#4: Skip \033[94mSLACK\033[0m...")
                self.stdout.write("#5: Skip \033[94mDROPBOX\033[0m...")
                self.stdout.write("#6: Skip \033[94mSchedule Spreadsheet\033[0m...")
                self.stdout.write("#7: Skip \033[94mDuty Spreadsheet\033[0m...")
                self.stdout.write("#8: Skip \033[94mGoogle Calendar\033[0m...")
        except Exception:
            tb = traceback.format_exc()
            if IS_SLACK and not DEBUG:
                if ('pickle_git' in tb or 'cache_git' in tb) and ('ConnectionError' in tb or 'SSLError' in tb or 'timed out' in tb):
                    if os.path.exists('%s/cache/git/init.json' % MEDIA_ROOT):
                        t = datetime.fromtimestamp(os.path.getmtime('%s/cache/git/init.json' % MEDIA_ROOT))
                        if ((now - t).seconds >= 60 * 2.5 * 60):
                            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback": 'ERROR', "mrkdwn_in": ["text"], "color": "ff69bc", "text": '*`ERROR`*: *pickle_git()* Connection/SSL Error @ _%s_\n' % time.ctime()}])
                elif ('pickle_slack' in tb or 'cache_slack' in tb) and ('500' in tb and 'Internal Server Error' in tb) or ('503' in tb and 'Service' in tb and 'Unavailable' in tb) or ('504' in tb and 'gateway' in tb.lower()) or ('HTTPSConnectionPool' in tb):
                    if os.path.exists('%s/cache/slack/users.json' % MEDIA_ROOT):
                        t = datetime.fromtimestamp(os.path.getmtime('%s/cache/slack/users.json' % MEDIA_ROOT))
                        if ((now - t).seconds >= 60 * 2.5 * 60):
                            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback": 'ERROR', "mrkdwn_in": ["text"], "color": "ff69bc", "text": '*`ERROR`*: *pickle_slack()* Connection/SSL Error @ _%s_\n' % time.ctime()}])
                elif ('pickle_dropbox' in tb or 'cache_dropbox' in tb) and ('502' in tb and 'Bad Gateway' in tb) or ('503' in tb and 'Service Unavailable' in tb):
                    if os.path.exists('%s/cache/dropbox/folders.json' % MEDIA_ROOT):
                        t = datetime.fromtimestamp(os.path.getmtime('%s/cache/dropbox/folders.json' % MEDIA_ROOT))
                        if ((now - t).seconds >= 60 * 2.5 * 60):
                            send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback": 'ERROR', "mrkdwn_in": ["text"], "color": "ff69bc", "text": '*`ERROR`*: *pickle_dropbox()* Connection/SSL Error @ _%s_\n' % time.ctime()}])
                else:
                    send_error_slack(tb, 'Cache Dashboard Results', ' '.join(sys.argv), 'log_cron_cache.log')
            else:
                print tb
            self.stdout.write("Finished with \033[41mERROR\033[0m!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)

        self.stdout.write("Finished with \033[92mSUCCESS\033[0m!")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))


