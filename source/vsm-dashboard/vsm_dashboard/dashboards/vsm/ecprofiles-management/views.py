# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Corporation, All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django import forms as django_froms
from horizon import exceptions
from horizon import tables
from horizon import forms
from vsm_dashboard.api import vsm as vsmapi
from .tables import RBDGroupsTable
from django.http import HttpResponse,HttpResponseRedirect
from vsm_dashboard.utils import get_time_delta
import json
LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = RBDGroupsTable
    template_name = 'vsm/ecprofiles-management/index.html'

    def get_data(self):
        _ec_profiles = []
        try:
            _ec_profiles = vsmapi.ec_profile_get_all(self.request)
            #print '_rbdgroup_status===%s'%_rbdgroup_status
            if _ec_profiles:
                logging.debug("resp body in view: %s" % _ec_profiles)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve sever list. '))

        ec_profiles = []
        for _ec_profile in _ec_profiles:
            ec_profile = {
                      "id": _ec_profile.id,
                      "name":_ec_profile.name,
                      "plugin": _ec_profile.plugin,
                    }

            ec_profiles.append(ec_profile)
        return ec_profiles



def add_ec_profile_view(request):
    #print '222222222'
    template = "vsm/ecprofiles-management/add_ec_profile.html"
    context = {}
    return render(request,template,context)

def add_ec_profile(request):
    status = ""
    msg = ""
    body = json.loads(request.body)
    print body
    try:
        rsp, ret = vsmapi.ec_profile_create(request,body=body)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

def remove_ec_profiles(request):
    data = json.loads(request.body)
    ec_profile_id_list = data["ec_profile_id_list"]

    ec_profiles = {'ec_profiles':ec_profile_id_list}
    #print '---rbd_groups remove-%s'%rbd_groups
    #ret,message = vsmapi.rbd_remove(request, rbds)
    try:
        rsp, ret = vsmapi.ec_profile_remove(request, ec_profiles)
        ret = ret['message']
    except:
        ret = {'error_code':'-2','error_msg':'Unkown Error!'}
    resp = json.dumps(ret)
    return HttpResponse(resp)

