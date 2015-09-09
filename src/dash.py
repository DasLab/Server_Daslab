from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from datetime import date, datetime, timedelta
import operator
# import os
import simplejson
import subprocess
# import sys
from time import sleep, mktime

import boto.ec2.cloudwatch
import gviz_api
from github import Github
from slacker import Slacker

from src.console import *
from src.settings import *


def dash_aws(request):
    if request.GET.has_key('qs') and request.GET.has_key('id') and request.GET.has_key('tp') and request.GET.has_key('tqx'):
        qs = request.GET.get('qs')
        id = request.GET.get('id')
        tp = request.GET.get('tp')
        req_id = request.GET.get('tqx').replace('reqId:', '')

        if qs == 'init':
            dict_aws = {'ec2':[], 'elb':[], 'ebs':[], 'table':[]}
            conn = boto.ec2.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)

            resvs = conn.get_only_instances()
            for i, resv in enumerate(resvs):
                sub_conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
                data = sub_conn.get_metric_statistics(600, datetime.now() - timedelta(hours=2), datetime.now(), 'CPUCreditBalance', 'AWS/EC2', 'Average', {'InstanceId': resv.id}, 'Count')
                avg = 0
                for d in data:
                    avg += d[u'Average']
                avg = avg / len(data)
                name = ''
                if resv.tags.has_key('Name'): name = resv.tags['Name']
                dict_aws['ec2'].append({'name':name, 'type':resv.instance_type, 'dns':resv.dns_name, 'status':resv.state_code, 'arch':resv.architecture, 'region':resv.placement, 'credit': '%.1f' % avg, 'id':resv.id})

            resvs = conn.get_all_volumes()
            for i, resv in enumerate(resvs):
                name = ''
                if resv.tags.has_key('Name'): name = resv.tags['Name']
                dict_aws['ebs'].append({'name':name, 'size':resv.size, 'type':resv.type, 'region':resv.zone, 'encrypted':resv.encrypted, 'status':resv.status, 'id':resv.id})

            conn = boto.ec2.elb.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
            resvs = conn.get_all_load_balancers()
            for i, resv in enumerate(resvs):
                sub_conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
                data = sub_conn.get_metric_statistics(300, datetime.now() - timedelta(minutes=30), datetime.now(), 'HealthyHostCount', 'AWS/ELB', 'Maximum', {'LoadBalancerName': resv.name}, 'Count')
                status = True
                for d in data:
                    if d[u'Maximum'] < 1: 
                        status = False
                        break
                dict_aws['elb'].append({'name':resv.name, 'dns':resv.dns_name, 'region': ', '.join(resv.availability_zones), 'status':status})

            dict_aws['ec2'] = sorted(dict_aws['ec2'], key=operator.itemgetter(u'name'))
            dict_aws['ebs'] = sorted(dict_aws['ebs'], key=operator.itemgetter(u'name'))
            dict_aws['elb'] = sorted(dict_aws['elb'], key=operator.itemgetter(u'name'))

            for i in range(max(len(dict_aws['ec2']), len(dict_aws['elb']), len(dict_aws['ebs']))):
                temp = {}
                if i < len(dict_aws['ec2']):
                    temp.update({'ec2': {'name':dict_aws['ec2'][i]['name'], 'status':dict_aws['ec2'][i]['status'], 'id':dict_aws['ec2'][i]['id']}})
                if i < len(dict_aws['ebs']):
                    temp.update({'ebs': {'name':dict_aws['ebs'][i]['name'], 'status':dict_aws['ebs'][i]['status'], 'id':dict_aws['ebs'][i]['id']}})
                if i < len(dict_aws['elb']):
                    temp.update({'elb': {'name':dict_aws['elb'][i]['name'], 'status':dict_aws['elb'][i]['status']}})
                dict_aws['table'].append(temp)
            return simplejson.dumps(dict_aws)

        else:
            conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
            if tp in ['ec2', 'elb', 'ebs']:
                args = {'period':3600, 'start_time':datetime.now() - timedelta(days=1), 'end_time':datetime.now()}
            else:
                return HttpResponseBadRequest("Invalid query.")

            if qs == 'lat':
                args.update({'metric':['Latency'], 'namespace':'AWS/ELB', 'cols':['Maximum'], 'dims':{}, 'unit':'Seconds', 'calc_rate':False})
            elif qs == 'req':
                args.update({'metric':['RequestCount'], 'namespace':'AWS/ELB', 'cols':['Sum'], 'dims':{}, 'unit':'Count', 'calc_rate':False})
            elif qs == 'net':
                args.update({'metric':['NetworkIn', 'NetworkOut'], 'namespace':'AWS/EC2', 'cols':['Sum'], 'dims':{}, 'unit':'Bytes', 'calc_rate':True})
            elif qs == 'cpu':
                args.update({'metric':['CPUUtilization'], 'namespace':'AWS/EC2', 'cols':['Average'], 'dims':{}, 'unit':'Percent', 'calc_rate':False})
            elif qs == 'disk':
                args.update({'metric':['VolumeWriteBytes', 'VolumeReadBytes'], 'namespace':'AWS/EBS', 'cols':['Sum'], 'dims':{}, 'unit':'Bytes', 'calc_rate':True})
            else:
                return HttpResponseBadRequest("Invalid query.")
    else:
        return HttpResponseBadRequest("Invalid query.")

    if args['namespace'] == 'AWS/ELB':
        args['dims'] = {'LoadBalancerName': id}
    elif args['namespace'] == 'AWS/EC2':
        args['dims'] = {'InstanceId': id}
    elif args['namespace'] == 'AWS/EBS':
        args['dims'] = {'VolumeId': id}

    return aws_call(conn, args, req_id, qs)


def dash_ga(request):
    access_token = subprocess.Popen('curl --silent --request POST "https://www.googleapis.com/oauth2/v3/token" --data "refresh_token=%s" --data "client_id=%s" --data "client_secret=%s" --data "grant_type=refresh_token"' % (GA['REFRESH_TOKEN'], GA['CLIENT_ID'], GA['CLIENT_SECRET']), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
    access_token = simplejson.loads(access_token)['access_token']

    list_proj = subprocess.Popen('curl --silent --request GET "https://www.googleapis.com/analytics/v3/management/accountSummaries?access_token=%s"' % (access_token), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
    list_proj = simplejson.loads(list_proj)['items'][0]['webProperties'][::-1]

    dict_ga = {'access_token':access_token, 'client_id':GA['CLIENT_ID'], 'projs':[]}
    for proj in list_proj:
        dict_ga['projs'].append({'id':proj['profiles'][0]['id'], 'track_id':proj['id'], 'name':proj['name'], 'url':proj['websiteUrl']})
    for j, proj in enumerate(dict_ga['projs']):
        for i in ('sessionDuration', 'bounceRate', 'pageviewsPerSession', 'pageviews', 'sessions', 'users'):
            temp = subprocess.Popen('curl --silent --request GET "https://www.googleapis.com/analytics/v3/data/ga?ids=ga%s%s&start-date=30daysAgo&end-date=yesterday&metrics=ga%s%s&access_token=%s"' % (urllib.quote(':'), proj['id'], urllib.quote(':'), i, access_token), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip()
            temp = simplejson.loads(temp)['rows'][0][0]

            if i in ('bounceRate', 'pageviewsPerSession'):
                temp = '%.2f' % float(temp)
            elif i == 'sessionDuration':
                temp = str(timedelta(seconds=int(float(temp) / 1000)))
            else:
                temp = '%d' % int(temp)
            dict_ga['projs'][j][i] = temp

    return simplejson.dumps(dict_ga)


def dash_git(request):
    if request.GET.has_key('qs') and request.GET.has_key('repo') and request.GET.has_key('tqx'):
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        gh = Github(login_or_token=GIT["ACCESS_TOKEN"])

        if qs == 'init':
            repos = []
            for repo in gh.get_user().get_repos():
                i = 0
                contribs = repo.get_stats_contributors()
                while (contribs is None and i <= 5):
                    sleep(1)
                    contribs = repo.get_stats_contributors()
                if contribs is None: return HttpResponseServerError("PyGithub failed")
                data = []
                for contrib in contribs:
                    a, d = (0, 0)
                    for w in contrib.weeks:
                        a += w.a
                        d += w.d
                    data.append({u'Contributors': contrib.author.login, u'Commits': contrib.total, u'Additions': a, u'Deletions': d})
                data = sorted(data, key=operator.itemgetter(u'Commits'), reverse=True)[0:4]
                repos.append({'url':repo.html_url, 'private':repo.private, 'data':data, 'name':repo.name, 'id':repo.full_name})
            return simplejson.dumps({'git':repos})

        elif qs in ['c', 'ad']:
            repo = gh.get_repo('DasLab/' + request.GET.get('repo'))

            data = []
            desp = {'Timestamp':('datetime', 'Timestamp'), 'Samples':('number', 'Samples'), 'Unit':('string', 'Count')}
            stats = ['Timestamp']

            if qs == 'c':
                contribs = repo.get_stats_commit_activity()
                if contribs is None: return HttpResponseServerError("PyGithub failed")
                fields = ['Commits']
                for contrib in contribs: 
                    data.append({u'Timestamp': contrib.week, u'Commits': sum(contrib.days)})
            elif qs == 'ad':
                contribs = repo.get_stats_code_frequency()
                if contribs is None: return HttpResponseServerError("PyGithub failed")
                fields = ['Additions', 'Deletions']
                for contrib in contribs:
                    data.append({u'Timestamp': contrib.week, u'Additions': contrib.additions, u'Deletions': contrib.deletions})

            for field in fields:
                stats.append(field)
                desp[field] = ('number', field)
            
            data = sorted(data, key=operator.itemgetter(stats[0]))
            data_table = gviz_api.DataTable(desp)
            data_table.LoadData(data)
            results = data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)
            return results
        else:
            return HttpResponseBadRequest("Invalid query.")
    else:
        return HttpResponseBadRequest("Invalid query.")


def dash_slack(request):
    if request.GET.has_key('qs') and request.GET.has_key('tqx'):
        qs = request.GET.get('qs')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        sh = Slacker(SLACK["ACCESS_TOKEN"])

        if qs == 'users':
            response = sh.users.list().body['members']
            owners, admins, users, gones = [], [], [], []
            for resp in response:
                if resp.has_key('is_bot') and resp['is_bot']: continue
                if resp['deleted']:
                    gones.append({'name':resp['profile']['real_name'], 'id':resp['name'], 'image':resp['profile']['image_24']})
                elif resp['is_owner']:
                    owners.append({'name':resp['profile']['real_name'], 'id':resp['name'], 'image':resp['profile']['image_24']})
                elif resp['is_admin']:
                    admins.append({'name':resp['profile']['real_name'], 'id':resp['name'], 'image':resp['profile']['image_24']})
                else:
                    users.append({'name':resp['profile']['real_name'], 'id':resp['name'], 'image':resp['profile']['image_24']})
            json = {'users':users, 'admins':admins, 'owners':owners, 'gones':gones}
        elif qs == 'channels':
            response = sh.channels.list().body['channels']
            channels, archives = [], []
            for resp in response:
                temp = {'name':resp['name'], 'num_members':resp['num_members']}
                history = sh.channels.history(channel=resp['id'], count=1000).body
                temp.update({'num_msgs':len(history['messages']), 'has_more':history['has_more']})
                num_files = 0
                latest = 0
                for msg in history['messages']:
                    if msg.has_key('file'): num_files += 1
                    latest = max(latest, float(msg['ts']))
                temp.update({'latest':latest, 'num_files':num_files})
                if resp['is_archived']:
                    archives.append(temp)
                else:
                    channels.append(temp)
            json = {'channels':channels, 'archives':archives}
        elif qs == 'files':
            types = ['all', 'pdfs', 'images', 'gdocs', 'zips', 'posts', 'snippets']
            nums, sizes = [], []
            for t in types:
                response = sh.files.list(count=100, types=t).body
                size = 0
                for i in range(response['paging']['pages']):
                    page = sh.files.list(count=100, types=t, page=i).body['files']
                    for p in page:
                        size += p['size']
                nums.append(response['paging']['total'])
                sizes.append(size)
            json = {'files':{'types':types, 'nums':nums, 'sizes':sizes}}

        elif qs in ["plot_files", "plot_msgs"]:
            desp = {'Timestamp':('datetime', 'Timestamp'), 'Samples':('number', 'Samples'), 'Unit':('string', 'Count')}
            stats = ['Timestamp']
            data = []

            if qs == 'plot_files':
                fields = ['Files']
                for i in range(7):
                    start_time = datetime.today() - timedelta(days=i+1)
                    end_time = start_time + timedelta(days=1)
                    num = sh.files.list(types="all", ts_from=mktime(start_time.timetuple()), ts_to=mktime(end_time.timetuple())).body['paging']['total']
                    data.append({u'Timestamp': end_time.replace(hour=0, minute=0, second=0, microsecond=0), u'Files': num})
            elif qs == 'plot_msgs':
                fields = ['Messages']
                response = sh.channels.list().body['channels']
                for resp in response:
                    if resp['is_archived']: continue
                    for i in range(7):
                        start_time = datetime.today() - timedelta(days=i+1)
                        end_time = start_time + timedelta(days=1)
                        num = len(sh.channels.history(channel=resp['id'], latest=mktime(end_time.timetuple()), oldest=mktime(start_time.timetuple()), count=1000).body['messages'])
                        if len(data) > i:
                            data[i]['Messages'] += num
                        else:
                            data.append({u'Timestamp': end_time.replace(hour=0, minute=0, second=0, microsecond=0), u'Messages': num})

            for field in fields:
                stats.append(field)
                desp[field] = ('number', field)
            
            data = sorted(data, key=operator.itemgetter(stats[0]))
            data_table = gviz_api.DataTable(desp)
            data_table.LoadData(data)
            results = data_table.ToJSonResponse(columns_order=stats, order_by='Timestamp', req_id=req_id)
            return results

        else:
            return HttpResponseBadRequest("Invalid query.")
        return simplejson.dumps(json)
    else:
        return HttpResponseBadRequest("Invalid query.")

