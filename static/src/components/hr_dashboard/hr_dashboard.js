/** @odoo-module **/

import { registry } from "@web/core/registry"
import { Component, useState, useRef, onMounted, onWillStart, onWillUnmount } from '@odoo/owl';
import { _t } from "@web/core/l10n/translation";
import { download } from "@web/core/network/download";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
const { DateTime } = luxon;
import { formatDate } from "@web/core/l10n/dates";
import { ChartBox} from "./chart_box/chart_box"
import { TextBox} from "./text_box/text_box"


export class SdHrDashboard extends Component {
    static template = "hr_dashboard";
    static components = { ChartBox, TextBox };
    static props = ["*"];
    setup() {
        this.state = useState({
            texts: {
               total: {id: 0, name: _t('Total'), icon: 'fa fa-users', value: '164', class: 'text_class_100', onTextClick: this.onTextClick},
               male:  {id: 1, name: _t('Male'), icon: 'fa fa-male', value: '80', class: 'text_class_100', onTextClick: this.onTextClick},
               female: {id: 2, name: _t('Female'), icon: 'fa fa-female', value: '84', class: 'text_class_100', onTextClick: this.onTextClick},
               presence: {id: 3, name: _t('Office'), icon: 'fa fa-building text-success', value: '33', class: 'text_class_100', onTextClick: this.onTextClick},
               remote: {id: 4, name: _t('Remote'), icon: 'fa fa-home text-success', value: '33', class: 'text_class_100', onTextClick: this.onTextClick},
               timeOff: {id: 5, name: _t('Time Off'), icon: 'fa fa-plane', value: '33', class: 'text_class_100', onTextClick: this.onTextClick},
            },
            charts: {
                age: {name: _t('Age'), config: {data:[]}, class: 'col-3'},
                certificates: {name: _t('Certificates'), config: {data:[]}, class: 'col-3'},
                departments: {name: _t('Departments'), config: {data:[]}, class: 'col-6'},
                projects: {name: _t('projects'), config: {data:[]}, class: 'col-4'},
                projects_hr_cost: {name: _t('projects_hr_cost'), config: {data:[]}, class: 'col-4'},
//                productivity_rate: {name: _t('Employee productivity rate'), config: '', onTextClick: this.onTextClick},
//                absence_rate: {name: _t('Absence rate'), config: ''},
//                absence_cost: {name: _t('Absence cost'), config: ''},
//                quality_of_hire: {name: _t('Quality of hire'), config: ''},
//                turnover_rate: {name: _t('Turnover rate'), config: ''},
//                unwanted_turnover_rate: {name: _t('Unwanted turnover rate'), config: ''},
//                voluntary_turnover_rate: {name: _t('Voluntary  turnover rate'), config: ''},
//                training: {name: _t('Training effectiveness'), config: ''},
//                satisfaction_index: {name: _t('Employee satisfaction index'), config: ''},
//                engagement_index: {name: _t('Employee engagement index'), config: ''},
            }
        })
        this.orm = useService("orm")
        this.actionService = useService("action")
        onWillStart(async ()=>{
            await this.getData()
        })
        onMounted(()=>{
            let oActionManager = document.querySelector('.o_action_manager')
            oActionManager && (oActionManager.style.overflowY = 'auto')
        })
        onWillUnmount(()=>{
            let oActionManager = document.querySelector('.o_action_manager')
            oActionManager && (oActionManager.style.overflowY = '')
        })
        console.log('this.state:', this.state)
    }
    onTextClick(boxId){
        console.log('onTextClick:', boxId)
    }
    async getData(){
        let hr_data = await this.orm.searchRead('hr.employee', [], ['name', 'gender', 'marital', 'hr_presence_state'])
        let getEmployee = await this.orm.call('hr.employee', 'get_employees', [[]])
        getEmployee = JSON.parse(getEmployee)
//        readGroup(model, domain, fields, groupby, kwargs = {})
        console.log('getEmployee:', getEmployee)
        this.state.charts['age'].config = getEmployee.ages
        this.state.charts['certificates'].config = getEmployee.certificates
        this.state.charts['departments'].config = getEmployee.departments
        this.state.charts['projects'].config = getEmployee.projects
        this.state.charts['projects_hr_cost'].config = getEmployee.projects_hr_cost

        this.state.texts['total'].value = hr_data.length || 0
        this.state.texts['male'].value = hr_data.filter(v => v['gender'] == 'male').length || 0
        this.state.texts['female'].value = hr_data.filter(v => v['gender'] == 'female').length || 0
        this.state.texts['presence'].value = hr_data.filter(v => v['hr_presence_state'] == 'present').length || 0
        this.state.texts['timeOff'].value = hr_data.filter(v => v['hr_presence_state'] == 'absent').length || 0
        this.state.texts['remote'].value = hr_data.filter(v => v['hr_presence_state'] == 'onmission').length || 0

//        this.state.gender = hr_data.gender
    }
}

//SdHrDashboard.template = "hr_dashboard";
//SdHrDashboard.components = { ChartBox, TextBox };
registry.category("actions").add("hr_dashboard_view", SdHrDashboard);