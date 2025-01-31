/** @odoo-module **/
import { Component } from "@odoo/owl"
import { useState, useRef, onMounted, onWillStart, onWillUnmount } from '@odoo/owl';
import { loadJS } from "@web/core/assets";

export class ChartBox extends Component {
    static template = "chart_box_template";
    static props = { name: String, description: String, class: String, onClick: Function, config: Object, };

    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            const plotlyUrl = '/sd_hr_dashboard/static/src/lib/plotly-3.0.0.min.js'
            await loadJS(plotlyUrl)
        })
        this.chart = null;
        onMounted(() => this.renderChart())
        this.renderChart = this.renderChart.bind(this)
    }
    renderChart() {
        let self = this;
        const config = this.props.config ? JSON.parse(JSON.stringify(this.props.config)) : {config: {responsive: true, displayModeBar: true}}
        let data = config.data
        Plotly.newPlot(this.chartRef.el, config)
//        this.chartRef.el.on('plotly_click', this.chartClicked())
//        this.chartRef.el.on('plotly_doubleclick', function(){
//            alert('You clicked this Plotly chart!');
//        });

         this.chartRef.el.on('plotly_click', function(data){
              console.log('data:', data, self)
              var pn='',
                  tn='',
                  colors=[];
              for(var i=0; i < data.points.length; i++){
                pn = data.points[i].pointNumber;
                tn = data.points[i].curveNumber;
//                colors = data.points[i].data.marker.color;
              };
              colors[pn] = '#C54C82';
              console.log('pn:', pn, '\ntn:', tn)

              var update = {'marker':{color: colors,}};
//              Plotly.restyle( self.chartRef.el, update, [tn]);
            });
    }
    chartClicked(){
        console.log('chartClicked:', )
    }
}

