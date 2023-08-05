import { HighBaseView, HighBase } from "./highbase";
export class HighChartView extends HighBaseView {
    create_chart(wn, el, config) {
        return wn.Highcharts.chart(el, config);
    }
}
HighChartView.__name__ = "HighChartView";
export class HighChart extends HighBase {
    static init_HighChart() {
        this.prototype.default_view = HighChartView;
    }
}
HighChart.__name__ = "HighChart";
HighChart.__module__ = "panel_highcharts.models.highchart";
HighChart.init_HighChart();
//# sourceMappingURL=highchart.js.map