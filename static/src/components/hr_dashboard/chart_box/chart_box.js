/** @odoo-module **/
import { Component } from "@odoo/owl"
import { useState, useRef, onMounted, onWillStart, onWillUnmount } from '@odoo/owl';
import { loadJS } from "@web/core/assets";

export class ChartBox extends Component {
    static template = "chart_box_template";
    static props = { name: String, class: String, onClick: Function, config: Object };

    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
//            const plotlyUrl = '/sd_hr_dashboard/static/src/lib/plotly-2.35.2.min.js'
            const plotlyUrl = '/sd_hr_dashboard/static/src/lib/plotly-3.0.0.min.js'
            await loadJS(plotlyUrl)
        })
        this.chart = null;
        onMounted(() => this.renderChart())
        this.renderChart = this.renderChart.bind(this)
    }
    renderChart() {
        const config = this.props.config ? JSON.parse(JSON.stringify(this.props.config)) : {config: {responsive: true, displayModeBar: true}}
        Plotly.newPlot(this.chartRef.el, config)
    }
}

