import os
import sys

from django.core.management.base import BaseCommand

from src.settings import *
from src.models import *


class Command(BaseCommand):
    help = 'Convert static files path in MySQL database table entries.'

    def handle(self, *args, **options):
        dev = '/MATLAB_Code/Daslab_server/data/'
        release = '/home/ubuntu/Server_DasLab/data/'

        if len(sys.argv) != 2:
            self.stdout.write('Usage:')
            self.stdout.write('    %s <flag>' % sys.argv[0])
            self.stdout.write('    <flag> is chosen from "dev" or "release", indicating the target.')
            exit()

        target = sys.argv[1]
        if target == 'dev':
            old = release
            new = dev
        elif target == 'release':
            old = dev
            new = release
        else:
            self.stdout.write('Usage:')
            self.stdout.write('    %s <flag>' % sys.argv[0])
            self.stdout.write('    <flag> is chosen from "dev" or "release", indicating the target.')
            exit()


        self.stdout.write("Converting database path to \033[94m%s\033[0m..." % target)

        entries = News.objects.all()
        for e in entries:
            if e.image:
                e.image = e.image.url.replace(old, new)
                e.save()
        self.stdout.write("\033[92mSUCCESS\033[0m: ", len(entries), "of News image converted.\033[0m")

        entries = Member.objects.all()
        for e in entries:
            if e.image:
                e.image = e.image.url.replace(old, new)
                e.save()
        self.stdout.write("\033[92mSUCCESS\033[0m: ", len(entries), "of Member image converted.\033[0m")

        entries = Publication.objects.all()
        for e in entries:
            if e.pdf:
                e.pdf = e.pdf.url.replace(old, new)
                e.save()
            if e.extra_file:
                e.extra_file = e.extra_file.url.replace(old, new)
                e.save()
            if e.image:
                e.image = e.image.url.replace(old, new)
                e.save()
        self.stdout.write("\033[92mSUCCESS\033[0m: ", len(entries), "of Publication pdf, extra_file, image converted.\033[0m")

        entries = RotationStudent.objects.all()
        for e in entries:
            if e.ppt:
                e.ppt = e.ppt.url.replace(old, new)
                e.save()
            if e.data:
                e.data = e.data.url.replace(old, new)
                e.save()
        self.stdout.write("\033[92mSUCCESS\033[0m: ", len(entries), "of RotationStudent ppt, data converted.\033[0m")

        entries = Presentation.objects.all()
        for e in entries:
            if e.ppt:
                e.ppt = e.ppt.url.replace(old, new)
                e.save()
        self.stdout.write("\033[92mSUCCESS\033[0m: ", len(entries), "of Presentation ppt converted.\033[0m")
        self.stdout.write("All done!"

