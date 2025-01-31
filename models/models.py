
from odoo import models, fields, api
import json
from jdatetimext import j_start, j_date_period
from datetime import date
from collections import Counter
from icecream import ic
import logging
class SdHrDashboardEmployee(models.Model):
    _inherit = 'hr.employee'


    def get_employees(self, emp='all'):
        ic(emp)
        lang = self.env.context.get('lang', 'en_US')
        emp_domain = []
        cont_domain = [('state', '=', 'open')]
        if emp == 'all':
            emp_domain = []
            cont_domain = [('state', '=', 'open')]
        elif emp == 'male':
            emp_domain = [('gender', '=', 'male')]
            cont_domain = [('state', '=', 'open')]
        elif emp == 'female':
            emp_domain = [('gender', '=', 'female')]
            cont_domain = [('state', '=', 'open')]

        employees_data = self.search_read(emp_domain, ['birthday', 'certificate', 'department_id', 'project_name'])
        employees_ids = self.search(emp_domain,)
        departments_data = self.env['hr.department'].search_read([], ['name'])
        projects_data = self.env['sd_projects.projects'].search_read([], ['name'])
        contracts_data = self.env['hr.contract'].search(cont_domain + [('employee_id', 'in', employees_ids.ids)])
        # cont_domain = cont_domain + [('employee_id', 'in', employees_ids.ids)]

        # >>>>>>> AGES
        age_list = list([(self.age_calculation(rec['birthday']) // 10) * 10 for rec in employees_data if rec['birthday']])
        age_count = Counter(age_list)
        age_decade = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        age_count = list([age_count[rec] for rec in age_decade])
        trace1_y = {
            'x': age_decade,
            'y': age_count,
            'text': [rec if rec > 5  else '' for rec in age_count],
            'type': "bar",
            'textfont': {
                'size': 18,
            }
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
                    # 'tickvals': age_count,
                    # 'tickformat': 'd',
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
                    # 'tickvals': certificate_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }

        # >>>>>>> DEPARTMENTS
        department_names = list([rec['name'] for rec in departments_data if rec['name']])
        department_ids = list([rec['id'] for rec in departments_data])
        employees_department_list = list([rec['department_id'][0] for rec in employees_data if rec['department_id']])
        # ic(employees_department_list)
        '''
        ic| department_list: [(5, 'مدیریت / IT'),
                      (13, 'مدیریت / فنی و مهندسی'),
                      (2, 'مدیریت'),

        '''
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
                    # 'tickvals': department_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }


        # >>>>>>> projects_data
        project_names = list([rec['name'] for rec in projects_data if rec['name']])
        project_ids = list([rec['id'] for rec in projects_data])
        employees_project_list = list([rec['project_name'][0] for rec in employees_data if rec['project_name']])
        # ic(employees_project_list)
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
                    # 'tickvals': project_count,
                    # 'tickformat': 'd',
                }, },
            'config': {'responsive': True, 'displayModeBar': False}
        }


        # >>>>>>> Projects HR Cost
        project_names = list([rec['name'] for rec in projects_data if rec['name']])
        project_ids = list([rec['id'] for rec in projects_data])
        employees_project_list = list([rec['project_name'][0] for rec in employees_data if rec['project_name']])
        # contracts_data
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

        ic(project_contract_dict)
        project_cost_dict = {}
        for rec_project, rec_lists in project_contract_dict.items():
            # ic(rec_project)
            project_cost_list = []
            for rec_list in rec_lists:
                project_date_cost = 0
                for rec in rec_list:
                    project_date_cost += rec.pr_sum // 10000000
                project_cost_list.append(project_date_cost)
            project_cost_dict[rec_project] = project_cost_list

        # ic(project_cost_dict)

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
                # 'xaxis': 'x1',
                # 'width': 0.2,
                # 'offset': 0.05,
                # 'marker': {'color': 'rgb(30,80,120)'},
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
                    # 'tickvals': project_count,
                    # 'tickformat': 'd',
                }, },
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