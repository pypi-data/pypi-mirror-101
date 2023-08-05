#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option

from generalobj.models import GOStatus

import sys


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--file', action='store', dest='filename', \
                required=True, help='filename for file is required')
        parser.add_argument('--dictionary', action='store', dest='dt', \
                required=True, help='The name of the dictionary from the file')
        #If reset is not specified, it'll do anything only if there're no
        #GOStatuses with the given pod.
        parser.add_argument('--reset', action='store_true', dest='reset', \
                help='If there is any GOStatus, it will delete them first')
        #Mostly it's a ForeignKey, so it wouldn't be a good idea to delete the
        #pks and recreate.
        parser.add_argument('--parent_obj_description', action='store', \
                dest='parent_obj_description', required=True, \
                help="It helps identify which GOS. It won't delete any GOS,\
                but tries to identify by code and update. If no match, it'll \
                create a new one.")

    def handle(self, *args, **options):
        #Get command line parameters
        filename = options['filename']
        dt_name = options['dt']
        reset = options['reset']
        pod = options['parent_obj_description']
        
        #I'll work only with GOStatuses with the given pod
        current_goses = GOStatus.objects.filter(parent_obj_description=pod)
        if not reset and current_goses:
            print("There are GOStatuses, but i can't reset them. Exiting.") 
            sys.exit(1)

        #Reading the config file and the given dictionary. Might be dangerous,
        #maybe i should change and use configparser.
        exec(open(filename).read())
        dt = eval(dt_name)

        #Checking for errors in the dictionary. Code and name are mandatory.
        errors = []
        if not 'pod' in dt:
            errors.append('pod is not in dictionary')
        for item in dt['items']:
            if not 'code' in item.keys():
                errors.append('code is not in item: %s' % item)
            else:
                if not item['code']:
                    errors.append('code is empty in item: %s' % item)
            if not 'name' in item.keys():
                errors.append('name is not in item: %s' % item)
            else:
                if not item['name']:
                    errors.append('name is empty in item: %s' % item)
        #Printing the errors and exiting.
        if errors:
            for count, error in enumerate(errors):
                print('%s.\t%s' % (count, error))
            sys.exit(2)

        #Creating / Updating the GOStatuses based on the dictionary.
        #If updating, the binding argument is the code.
        #If it's a new item, id can be updated.
        for item in dt['items']:
            if reset:
                try:
                    gos = current_goses.get(code=item['code'])
                except:
                    gos = GOStatus(parent_obj_description=pod, \
                            code=item['code'])
                    #If it's a new item, ID might be set
                    if 'id' in item.keys():
                        gos.id = item['id']
            else:
                gos = GOStatus(parent_obj_description=pod, code=item['code'])
                #If it's a new item, ID might be set
                if 'id' in item.keys():
                    gos.id = item['id']
            gos.name = item['name']
            if 'next_statuses' in item.keys():
                gos.next_statuses = item['next_statuses']
            if 'is_entrant' in item.keys():
                gos.is_entrant = item['is_entrant']
            if 'is_leaving' in item.keys():
                gos.is_leaving = item['is_leaving']
            if 'is_forward' in item.keys():
                gos.is_forward = item['is_forward']
            if 'is_backward' in item.keys():
                gos.is_backward = item['is_backward']
            if 'style' in item.keys():
                gos.style = item['style']
            gos.save()
