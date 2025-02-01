/** @odoo-module **/

import { registry } from "@web/core/registry"
import { Component, useState, useRef, onMounted, onWillStart, onWillUnmount, useChildSubEnv } from '@odoo/owl';
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
        this.getData = this.getData.bind(this)
        this.onTextClick = this.onTextClick.bind(this)
        this.onClick = this.onTextClick.bind(this);
        this.updateChart = this.updateChart.bind(this);

        this.state = useState({
            domain: [{total: [0,0]}],
            texts: {
               total: {id: 0, name: _t('Total'), icon: 'fa fa-users', value: '164', class: 'text_class_100', classBg: 'bg-warning-light', onTextClick: this.onTextClick},
               male:  {id: 1, name: _t('Male'), icon: 'fa fa-male', value: '80', class: 'text_class_100', classBg: '', onTextClick: this.onTextClick},
               female: {id: 2, name: _t('Female'), icon: 'fa fa-female', value: '84', class: 'text_class_100', classBg: '', onTextClick: this.onTextClick},
//               presence: {id: 3, name: _t('Office'), icon: 'fa fa-building text-success', value: '33', class: 'text_class_100', classBg: '', onTextClick: this.onTextClick},
//               remote: {id: 4, name: _t('Remote'), icon: 'fa fa-home text-success', value: '33', class: 'text_class_100', classBg: '', onTextClick: this.onTextClick},
//               timeOff: {id: 5, name: _t('Time Off'), icon: 'fa fa-plane', value: '33', class: 'text_class_100', classBg: '', onTextClick: this.onTextClick},
            },
            charts: {
                projects: {name: _t('Projects'), description: _t('Categorization by Projects'), config: {data:[]}, class: 'col-3'},
                departments: {name: _t('Departments'), description: _t('Categorization by Departments'), config: {data:[]}, class: 'col-6'},
                age: {name: _t('Age'), description: _t('Categorization by Age'), config: {data:[]}, class: 'col-3', onClick: () => {}},
                certificates: {name: _t('Certificates'), description: _t('distribution of various educational degrees'), config: {data:[]}, class: 'col-3'},
                projects_hr_cost: {name: _t('Projects HR Cost'), description: _t('Projects HR cost forcast (Milion Toman)'), config: {data:[]}, class: 'col-6'},
//                productivity_rate: {name: _t('Employee productivity rate'), config: '', onTextClick: this.onTextClick},
//                absence_rate: {name: _t('Absence rate'), config: {data:[]}, class: 'col-4'},
//                absence_cost: {name: _t('Absence cost'), config: {data:[]}, class: 'col-4'},
//                quality_of_hire: {name: _t('Quality of hire'), config: {data:[]}, class: 'col-4'},
//                turnover_rate: {name: _t('Turnover rate'), config: {data:[]}, class: 'col-4'},
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
        onMounted(async ()=>{
            this.onTextClick([{total: ['', 0, 0]}])
            let oActionManager = document.querySelector('.o_action_manager')
            oActionManager && (oActionManager.style.overflowY = 'auto')
        })
        onWillUnmount(()=>{
            let oActionManager = document.querySelector('.o_action_manager')
            oActionManager && (oActionManager.style.overflowY = '')
        })
        console.log('this:', this)
    }
    async getData(state_domain=[{total: ['', 0, 0]}]){
        let hr_data = await this.orm.searchRead('hr.employee', [], ['name', 'gender', 'marital', 'hr_presence_state'])

        let getEmployee = await this.orm.call('hr.employee', 'get_employees', [false, state_domain])
        getEmployee = JSON.parse(getEmployee)
//        readGroup(model, domain, fields, groupby, kwargs = {})

//        console.log('getEmployee:', getEmployee)
        this.state.texts['total'].value = hr_data.length || 0
        this.state.texts['male'].value = hr_data.filter(v => v['gender'] == 'male').length || 0
        this.state.texts['female'].value = hr_data.filter(v => v['gender'] == 'female').length || 0
//        this.state.texts['presence'].value = hr_data.filter(v => v['hr_presence_state'] == 'present').length || 0
//        this.state.texts['timeOff'].value = hr_data.filter(v => v['hr_presence_state'] == 'absent').length || 0
//        this.state.texts['remote'].value = hr_data.filter(v => v['hr_presence_state'] == 'onmission').length || 0

        this.state.charts['age'].config = getEmployee.ages
        this.state.charts['certificates'].config = getEmployee.certificates
        this.state.charts['departments'].config = getEmployee.departments
        this.state.charts['projects'].config = getEmployee.projects
        this.state.charts['projects_hr_cost'].config = getEmployee.projects_hr_cost
    }
    async onTextClick(boxId, isChartClick=false, pn=0, tn=0, x=''){
        const self = this;
        console.log('onTextClick:', boxId, isChartClick, pn, tn)

        let updateList = ['total', 'male', 'female',]

        if(boxId == 'total'){
            this.state.texts.total.classBg = 'bg-warning-light'
            this.state.texts.male.classBg = ''
            this.state.texts.female.classBg = ''
            this.state.domain = [{total: ['', 0, 0]}]
        } else if(boxId == 'male'){
            this.state.texts.total.classBg = ''
            this.state.texts.male.classBg = 'bg-warning-light'
            this.state.texts.female.classBg = ''
            this.state.domain = [{male: ['', 0, 0]}]
        } else if(boxId == 'female'){
            this.state.texts.total.classBg = ''
            this.state.texts.male.classBg = ''
            this.state.texts.female.classBg = 'bg-warning-light'
            this.state.domain = [{female: ['', 0, 0]}]
        }else{
            if (this.state.domain.filter(r => r[boxId]).length){
            // remove the existing boxID from domain
            // [{male: ['', 0, 0]}, {projects: ['', 0, 0]}]
            this.state.domain = this.state.domain.filter(r => r[boxId] == undefined)

            }else{
                let domain_object = {}
                domain_object[boxId] = [x, pn, tn]
                this.state.domain.push(domain_object)
            }
        }
        console.log('domain filtered:', this.state.domain.filter(r => r[boxId]).length)
        await this.getData(this.state.domain)

        const chartBoxDivs = document.querySelectorAll('.chart_box_div')
        for ( const div of chartBoxDivs){
              self.updateChart(div, self.state.charts[div.attributes.chartName.value].config)
        }
    }
    async updateChart(div, config){
        let self = this;
        return new Promise((resolve) => {
            Plotly.newPlot(div, config);
            div.on('plotly_click', function(data){
              var pn='',
                  tn='',
                  x='',
                  colors=[];
              for(var i=0; i < data.points.length; i++){
                pn = data.points[i].pointNumber;
                tn = data.points[i].curveNumber;
                x = data.points[i].x;
              };
              self.onTextClick(div.attributes.chartName.value, true, pn, tn, x)
//              console.log('state:', self.state.domain)
//              console.log(div.attributes.chartName.value, '\npn:', pn, '\ntn:', tn, x )
//              colors[pn] = '#C54C82'; // #1f77b4 #094a77
//              var update = {'marker':{color: colors,}};
//              Plotly.restyle( self.chartRef.el, update, [tn]);
            });
            div.on('plotly_doubleclick', function(data){
//                console.log('plotly_doubleclick', data)
            })

            resolve();
        });
    }
}

registry.category("actions").add("hr_dashboard_view", SdHrDashboard);