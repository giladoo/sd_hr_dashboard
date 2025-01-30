/** @odoo-module **/
import { Component } from "@odoo/owl"

export class TextBox extends Component {
    static template = "text_box_template";
    static props = { key: String, id: Number, name: String, class: String, onClick: Function, value: Number, icon: String };
}

