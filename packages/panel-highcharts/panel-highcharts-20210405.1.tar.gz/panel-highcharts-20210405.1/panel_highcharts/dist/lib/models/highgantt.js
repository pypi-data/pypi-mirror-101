import { HighBaseView, HighBase } from "./highbase";
export class HighGanttView extends HighBaseView {
    create_chart(wn, el, config) {
        return wn.Highcharts.ganttChart(el, config);
    }
}
HighGanttView.__name__ = "HighGanttView";
export class HighGantt extends HighBase {
    static init_HighGantt() {
        this.prototype.default_view = HighGanttView;
    }
}
HighGantt.__name__ = "HighGantt";
HighGantt.__module__ = "panel_highcharts.models.highgantt";
HighGantt.init_HighGantt();
//# sourceMappingURL=highgantt.js.map