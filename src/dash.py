from datetime import datetime, timedelta
import operator
import os
import simplejson
import subprocess
import sys

import boto.ec2.cloudwatch
import gviz_api
from github import Github

from src.console import *
from src.settings import *


def server_list():
    dict_aws = {'ec2':{}, 'elb':{}, 'ebs':{}}

    conn = boto.ec2.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
    resvs = conn.get_only_instances()
    for resv in resvs:
        sub_conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
        data = sub_conn.get_metric_statistics(600, datetime.now() - timedelta(hours=2), datetime.now(), 'CPUCreditBalance', 'AWS/EC2', 'Average', {'InstanceId': resv.id}, 'Count')
        avg = 0
        for d in data:
            avg += d[u'Average']
        avg = avg / len(data)
        name = ''
        if resv.tags.has_key('Name'): name = resv.tags['Name']
        dict_aws['ec2'][resv.id] = {'name':name, 'type':resv.instance_type, 'dns':resv.dns_name, 'status':resv.state_code, 'arch':resv.architecture, 'region':resv.placement, 'credit': '%.1f' % avg}
    
    resvs = conn.get_all_volumes()
    for resv in resvs:
        name = ''
        if resv.tags.has_key('Name'): name = resv.tags['Name']
        dict_aws['ebs'][resv.id] = {'name':name, 'size':resv.size, 'type':resv.type, 'region':resv.zone, 'encrypted':resv.encrypted, 'status':resv.status}
    
    conn = boto.ec2.elb.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
    resvs = conn.get_all_load_balancers()
    for resv in resvs:
        sub_conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)
        data = sub_conn.get_metric_statistics(300, datetime.now() - timedelta(minutes=30), datetime.now(), 'HealthyHostCount', 'AWS/ELB', 'Maximum', {'LoadBalancerName': resv.name}, 'Count')
        status = True
        for d in data:
            if d[u'Maximum'] < 1: 
                status = False
                break
        dict_aws['elb'][resv.name] = {'dns':resv.dns_name, 'region': ', '.join(resv.availability_zones), 'status':status}


    results = {'aws':dict_aws}
    return results


def dash_aws(request):
    if request.GET.has_key('qs') and request.GET.has_key('id') and request.GET.has_key('tp') and request.GET.has_key('tqx'):
        qs = request.GET.get('qs')
        id = request.GET.get('id')
        tp = request.GET.get('tp')
        req_id = request.GET.get('tqx').replace('reqId:', '')
        conn = boto.ec2.cloudwatch.connect_to_region(AWS['REGION'], aws_access_key_id=AWS['ACCESS_KEY_ID'], aws_secret_access_key=AWS['SECRET_ACCESS_KEY'], is_secure=True)

        if tp in ['ec2', 'elb', 'ebs']:
            args = {'period':3600, 'start_time':datetime.now() - timedelta(days=1), 'end_time':datetime.now()}
        else:
            return HttpResponseBadRequest

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
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest

    if args['namespace'] == 'AWS/ELB':
        args['dims'] = {'LoadBalancerName': id}
    elif args['namespace'] == 'AWS/EC2':
        args['dims'] = {'InstanceId': id}
    elif args['namespace'] == 'AWS/EBS':
        args['dims'] = {'VolumeId': id}

    return aws_call(conn, args, req_id, qs)




