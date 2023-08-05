import { HighBaseView, HighBase } from "./highbase";
export class HighMapView extends HighBaseView {
    create_chart(wn, el, config) {
        return wn.Highcharts.mapChart(el, config);
    }
}
HighMapView.__name__ = "HighMapView";
export class HighMap extends HighBase {
    static init_HighMap() {
        this.prototype.default_view = HighMapView;
    }
}
HighMap.__name__ = "HighMap";
HighMap.__module__ = "panel_highcharts.models.highmap";
HighMap.init_HighMap();
//# sourceMappingURL=highmap.js.map