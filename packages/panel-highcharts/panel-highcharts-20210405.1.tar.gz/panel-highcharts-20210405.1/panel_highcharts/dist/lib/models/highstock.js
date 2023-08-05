import { HighBaseView, HighBase } from "./highbase";
export class HighStockView extends HighBaseView {
    create_chart(wn, el, config) {
        return wn.Highcharts.stockChart(el, config);
    }
}
HighStockView.__name__ = "HighStockView";
export class HighStock extends HighBase {
    static init_HighStock() {
        this.prototype.default_view = HighStockView;
    }
}
HighStock.__name__ = "HighStock";
HighStock.__module__ = "panel_highcharts.models.highstock";
HighStock.init_HighStock();
//# sourceMappingURL=highstock.js.map