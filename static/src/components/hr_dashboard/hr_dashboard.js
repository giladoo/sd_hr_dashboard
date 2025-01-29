/** @odoo-module **/

import { registry } from "@web/core/registry"
import { Component } from "@odoo/owl"
import { _t } from "@web/core/l10n/translation";
import { useState, useRef, onMounted, onWillUnmount } from '@odoo/owl';
import { download } from "@web/core/network/download";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
const { DateTime } = luxon;
import { formatDate } from "@web/core/l10n/dates";



    console.log('asdfasdfasdfasdf 1')

export class SdHrDashboard extends Component {
    setup() {
        console.log('asdfasdfasdfasdf 2')
    }
}

SdHrDashboard.template = "hr_dashboard";
registry.category("actions").add("hr_dashboard_view", SdHrDashboard);