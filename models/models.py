
from odoo import models, fields, api
import json
from jdatetimext import j_start
from datetime import date
from collections import Counter
from icecream import ic
import logging
class SdHrDashboardEmployee(models.Model):
    _inherit = 'hr.employee'


    def get_employees(self):
        employees = self.search_read([], ['birthday', 'certificate', 'department_id', 'project_name'])
        departments = self.env['hr.department'].search_read([], ['name'])
        projects = self.env['sd_projects.projects'].search_read([], ['name'])
        ic(projects)

        # >>>>>>> AGES
        age_list = list([(self.age_calculation(rec['birthday']) // 10) * 10 for rec in employees if rec['birthday']])
        age_count = Counter(age_list)
        age_decade = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        age_count = list([age_count[rec] for rec in age_decade])
        trace1_y = {
            'x': age_decade,
            'y': age_count,
            'type': "bar",
            # 'name': "MEG",
            # 'xaxis': 'x1',
            # 'width': 0.2,
            # 'offset': 0.05,
            # 'marker': {'color': 'rgb(30,80,120)'},
        }
        ages = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 0,
                    'tickfont': {
                        'size': 12
                    },
                },
                'yaxis': {
                    'tickvals': age_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': True}
        }

        # >>>>>>> Certificate
        certificate_list = list([rec['certificate'] for rec in employees])
        certificate_names_translate = list(dict(self._fields['certificate']._description_selection(self.env)).values())
        certificate_names = self._fields['certificate'].get_values(self.env)
        certificate_count = Counter(certificate_list)
        certificate_count = list([certificate_count[rec] for rec in certificate_names])
        trace1_y = {
            'x': certificate_names_translate,
            'y': certificate_count,
            'type': "bar",
            # 'name': "MEG",
            # 'xaxis': 'x1',
            # 'width': 0.2,
            # 'offset': 0.05,
            # 'marker': {'color': 'rgb(30,80,120)'},
        }
        certificates = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 0,
                    'tickfont': {
                        'size': 12
                    },
                },
                'yaxis': {
                    'tickvals': certificate_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': True}
        }

        # >>>>>>> DEPARTMENTS
        department_names = list([rec['name'] for rec in departments if rec['name']])
        department_ids = list([rec['id'] for rec in departments])
        employees_department_list = list([rec['department_id'][0] for rec in employees if rec['department_id']])
        # ic(employees_department_list)
        '''
        ic| department_list: [(5, 'مدیریت / IT'),
                      (13, 'مدیریت / فنی و مهندسی'),
                      (2, 'مدیریت'),

        '''
        department_count = Counter(employees_department_list)
        department_count = list([department_count[rec] for rec in department_ids])
        trace1_y = {
            'x': department_names,
            'y': department_count,
            'type': "bar",
            # 'name': "MEG",
            # 'xaxis': 'x1',
            # 'width': 0.2,
            # 'offset': 0.05,
            # 'marker': {'color': 'rgb(30,80,120)'},
        }
        departments = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 45,
                    'tickfont': {
                        'size': 12
                    },
                },
                'yaxis': {
                    'tickvals': department_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': True}
        }


        # >>>>>>> Projects
        project_names = list([rec['name'] for rec in projects if rec['name']])
        project_ids = list([rec['id'] for rec in projects])
        employees_project_list = list([rec['project_name'][0] for rec in employees if rec['project_name']])
        ic(employees_project_list)
        # '''
        # ic| project_list: [(5, 'مدیریت / IT'),
        #               (13, 'مدیریت / فنی و مهندسی'),
        #               (2, 'مدیریت'),
        #
        # '''
        project_count = Counter(employees_project_list)
        project_count = list([project_count[rec] for rec in project_ids])
        trace1_y = {
            'x': project_names,
            'y': project_count,
            'type': "bar",
            # 'name': "MEG",
            # 'xaxis': 'x1',
            # 'width': 0.2,
            # 'offset': 0.05,
            # 'marker': {'color': 'rgb(30,80,120)'},
        }
        projects = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 45,
                    'tickfont': {
                        'size': 12
                    },
                },
                'yaxis': {
                    'tickvals': project_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': True}
        }






        data = {
            'ages': ages,
            'certificates': certificates,
            'departments': departments,
            'projects': projects,

            }
        return json.dumps(data)


    def age_calculation(self, start_date, end_date=fields.date.today()):
        if isinstance(start_date, fields.date):
            age = end_date.year - start_date.year - (
                    (end_date.month, end_date.day) < (start_date.month, start_date.day))
        else:
            age = 0
        return age