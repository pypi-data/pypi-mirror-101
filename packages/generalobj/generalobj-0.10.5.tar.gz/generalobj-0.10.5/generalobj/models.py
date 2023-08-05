from django.db import models

from django.apps import apps


class GOStatus(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    parent_obj_description = models.CharField(max_length=128) #'$appname___$modelname
    next_statuses = models.CharField(max_length=256, blank=True, null=True, \
            default='')
    is_entrant = models.BooleanField(default=False)
    is_leaving = models.BooleanField(default=False)
    is_forward = models.BooleanField(default=True)
    is_backward = models.BooleanField(default=False)

    def get_next_statuses(self):
        return GOStatus.objects.filter(\
                parent_obj_description=self.parent_obj_description).filter(\
                code__in=self.next_statuses.split('|'))

    def add_status(self, name):
        if not self.next_statuses:
            self.next_statuses = ''
        if '|%s|' % name in self.next_statuses:
            return True
        else:
            if not self.next_statuses.startswith('|'):
                self.next_statuses = '|%s' % self.next_statuses
            if not self.next_statuses.endswith('|'):
                self.next_statuses += '|'
            self.next_statuses += '%s|' % name
            self.save()

    def remove_status(self, name):
        if '|%s|' % name in self.next_statuses:
            self.next_statuses = self.next_statuses.replace('%s|' % name, '')
            self.save()

    def add_statuses(self, name_lst):
        self.next_statuses = '|%s|' % '|'.join(sorted(name_lst))
        self.save()


    def get_model(self):
        try:
            pob = self.parent_obj_description.split('___')
            model_base = apps.get_model(pob[0], pob[1])
            return model_base
        except:
            return False

    def get_attr_parts(self):
        mdl = self.get_model()
        if mdl:
            try:
                pob = self.parent_obj_description.split('___')
                return (mdl, pob[2])
            except:
                return (mdl, 'status')
        else:
            return False

    def set_status(self, status):
        self.status = status
        self.save()


    def change_parent_obj_status(self, parent_obj_id, ns_code, check_next_statuses=True):
        if check_next_statuses:
            if not '|%s|' % ns_code in self.next_statuses:
                print("Status can't be set. %s is not next." % ns_code)
        ns_obj = GOStatus.objects.get(code=ns_code, \
                parent_obj_description=self.parent_obj_description)
        parent_obj_base, attr_name = self.get_attr_parts()
        parent_obj = parent_obj_base.objects.get(id=parent_obj_id)
        if parent_obj:
            setattr(parent_obj, attr_name, ns_obj)
            parent_obj.save()
            

    def __str__(self):
        return '%s -> %s' % (self.code, self.next_statuses)
