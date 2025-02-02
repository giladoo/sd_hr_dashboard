
from odoo import models, fields, api
import json
from jdatetimext import j_start, j_date_period
from datetime import date
from collections import Counter
from icecream import ic
import logging
class SdHrDashboardEmployee(models.Model):
    _inherit = 'hr.employee'


    def get_employees(self, domain_list=[{'total': ['', 0, 0]}]):
        if not self.env.user.has_group('hr.group_hr_user'):
            return {}
        ic(domain_list, )
        ic(list([r for r in domain_list if dict(r).get('total', False)]))
        lang = self.env.context.get('lang', 'en_US')
        emp_domain = []
        project_domain = []
        emp_project_domain = []
        project_name_selected = ''
        department_domain = []
        cont_domain = [('state', '=', 'open')]
        if len(list([r for r in domain_list if dict(r).get('total', False)])) > 0:
            emp_domain = []
            cont_domain = [('state', '=', 'open')]
        elif len(list([r for r in domain_list if dict(r).get('male', False)])) > 0:
            emp_domain = [('gender', '=', 'male')]
            cont_domain = [('state', '=', 'open')]
        elif len(list([r for r in domain_list if dict(r).get('female', False)])) > 0:
            emp_domain = [('gender', '=', 'female')]
            cont_domain = [('state', '=', 'open')]

        projects_clicked = list([r for r in domain_list if dict(r).get('projects', False)])
        if len(projects_clicked) > 0:
            project_name_selected = dict(projects_clicked[0]).get('projects')[0]
            project_domain = [('name', '=', dict(projects_clicked[0]).get('projects')[0])]
            emp_project_domain = [('project_name', '=', dict(projects_clicked[0]).get('projects')[0])]
            emp_domain += emp_project_domain
            cont_domain += emp_project_domain

        department_clicked = list([r for r in domain_list if dict(r).get('departments', False)])
        ic(department_clicked)
        if len(department_clicked) > 0:
            department_domain = [('name', '=', dict(department_clicked[0]).get('departments')[0])]
            department_id = self.env['hr.department'].sudo().search(department_domain,)

            emp_domain += [('department_id', 'in', department_id.ids)]

        employees_data = self.sudo().search_read(emp_domain, ['birthday', 'certificate', 'department_id', 'project_name'])
        employees_ids = self.sudo().search(emp_domain,)
        department_domain = []
        departments_data = self.env['hr.department'].sudo().search_read(department_domain, ['name'])

        project_domain = []
        projects_data = self.env['sd_projects.projects'].sudo().search_read(project_domain, ['name'])
        if self.env.user.has_group('hr_contract.group_hr_contract_employee_manager'):
            contracts_data = self.env['hr.contract'].sudo().search(cont_domain + [('employee_id', 'in', employees_ids.ids)])
        else:
            contracts_data = []

        # >>>>>>> AGES
        age_list = list([(self.age_calculation(rec['birthday']) // 10) * 10 for rec in employees_data if rec['birthday']])
        age_count = Counter(age_list)
        age_decade = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        age_count = list([age_count[rec] for rec in age_decade])
        age_count_max = max(age_count)
        trace1_y = {
            'x': age_decade,
            'y': age_count,
            'text': [rec if rec > age_count_max * .15  else '' for rec in age_count],
            'type': "bar",
            'textfont': {
                'size': 18,
            }
        }
        ages = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'margin': {'l': 40, 'r': 20, 'b': 80, 't': 10, 'pad': 4},
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 0,
                    'tickfont': {
                        'size': 15
                    },
                },
                'yaxis': {
                    'showticklabels': False,
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }

        # >>>>>>> Certificate
        certificate_list = list([rec['certificate'] for rec in employees_data])
        certificate_names_translate = list(dict(self._fields['certificate']._description_selection(self.env)).values())
        certificate_names = self._fields['certificate'].get_values(self.env)
        certificate_count = Counter(certificate_list)
        certificate_count = list([certificate_count[rec] for rec in certificate_names])
        trace1_y = {
            'labels': certificate_names_translate,
            'values': certificate_count,
            'text': certificate_names_translate,

            'type': "pie",
            'hole': .4,
            'textfont': {
                'size': 16,
            },
        }
        certificates = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'margin': {'l': 40, 'r': 20, 'b': 80, 't': 60, 'pad': 4},
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 0,
                    'tickfont': {
                        'size': 15
                    },
                },
                'yaxis': {
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }

        # >>>>>>> DEPARTMENTS
        department_names = list([rec['name'] for rec in departments_data if rec['name']])
        department_ids = list([rec['id'] for rec in departments_data])
        employees_department_list = list([rec['department_id'][0] for rec in employees_data if rec['department_id']])
        department_count = Counter(employees_department_list)
        department_count = list([department_count[rec] for rec in department_ids])
        max_y = max(department_count)
        trace1_y = {
            'x': department_names,
            'y': department_count,
            'text': [rec if rec > max_y * .15 else '' for rec in department_count],
            'type': "bar",
            'textfont': {
                'size': 18,
            }
        }
        departments = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'margin': {'l': 40, 'r': 20, 'b': 80, 't': 10, 'pad': 4},
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 30,
                    'tickfont': {
                        'size': 15
                    },
                },
                'yaxis': {
                    'showticklabels': False if max_y < 6 else True ,
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }

        # >>>>>>> projects_data
        project_names = list([rec['name'] for rec in projects_data if rec['name']])
        project_ids = list([rec['id'] for rec in projects_data])
        employees_project_list = list([rec['project_name'][0] for rec in employees_data if rec['project_name']])
        project_count = Counter(employees_project_list)
        project_count = list([project_count[rec] for rec in project_ids])
        project_count = list([rec for rec in project_count])
        trace1_y = {
            'x': project_names,
            'y': project_count,
            'type': "bar",
            'text': [rec if rec > max(project_count) * .15 else '' for rec in project_count],

            'textfont': {
                'size': 18,
            }
        }
        projects = {
            'data': [trace1_y],
            'layout': {
                'autosize': True,
                'margin': {'l': 40, 'r': 20, 'b': 80, 't': 10, 'pad': 4},
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 30,
                    'tickfont': {
                        'size': 15
                    },
                },
                'yaxis': {
                    'showticklabels': False if max(project_count) < 6 else True,
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }


        # >>>>>>> Projects HR Cost
        project_names = list([rec['name'] for rec in projects_data if rec['name']])
        project_ids = list([rec['id'] for rec in projects_data])
        employees_project_list = list([rec['project_name'][0] for rec in employees_data if rec['project_name']])
        months_list = j_date_period('month',12,fields.date.today(), lang)
        months_date_list = j_date_period('month',12,fields.date.today(), lang, 'date')
        contracts_date_list = []
        for rec_date in months_date_list:
            contracts_date_list.append(list([rec for rec in contracts_data if rec.date_end and rec.date_end >= rec_date.date()]))
        project_contract_dict = {}
        for index, rec_project in enumerate(project_ids):
            rec_project_list = []
            for rec_contracts in contracts_date_list:
                rec_project_list.append(list([rec for rec in rec_contracts if rec.project_name and rec.project_name.id == int(rec_project)]))
            project_contract_dict[project_names[index]] = rec_project_list

        project_cost_dict = {}
        for rec_project, rec_lists in project_contract_dict.items():
            project_cost_list = []
            for rec_list in rec_lists:
                project_date_cost = 0
                for rec in rec_list:
                    project_date_cost += rec.pr_sum // 10000000
                project_cost_list.append(project_date_cost)
            project_cost_dict[rec_project] = project_cost_list

        project_count = Counter(employees_project_list)
        project_count = list([project_count[rec] for rec in project_ids])
        data_of_cost = []
        for p_name, p_const in project_cost_dict.items():
            data_of_cost.append( {
                'x': months_list,
                'y': p_const,
                'text': p_const,
                'type': "bar",
                'name': p_name,
                'textfont': {
                    'size': 16,
                    },
                })

        projects_hr_cost = {
            'data': data_of_cost,
            'layout': {
                'autosize': True,
                'barmode': 'stack',
                'margin': {'l': 40, 'r': 20, 'b': 80, 't': 10, 'pad': 4},
                'xaxis': {
                    'type': 'category',
                    'dtick': 1,
                    'tickangle': 30,
                    'tickfont': {
                        'size': 15
                    },
                },
                'yaxis': {
                },
            },
            'config': {'responsive': True, 'displayModeBar': False}
        }


        data = {
            'ages': ages,
            'certificates': certificates,
            'departments': departments,
            'projects': projects,
            'projects_hr_cost': projects_hr_cost,

            }
        return json.dumps(data)


    def age_calculation(self, start_date, end_date=fields.date.today()):
        if isinstance(start_date, fields.date):
            age = end_date.year - start_date.year - (
                    (end_date.month, end_date.day) < (start_date.month, start_date.day))
        else:
            age = 0
        return age