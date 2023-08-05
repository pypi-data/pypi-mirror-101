import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export class HighChartView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.config.change, this.render);
        this.connect(this.model.properties.config_update.change, this._handle_config_update_change);
    }
    render() {
        super.render();
        if (this.chart) {
            this.chart.destroy();
        }
        const wn = window;
        if (wn.Highcharts) {
            const config = this._clean_config(this.model.config);
            this.chart = wn.Highcharts.chart(this.el, config);
        }
        else {
            console.error("HighCharts .js is not loaded. Could not create chart");
        }
    }
    after_layout() {
        super.after_layout();
        this._resize();
    }
    _resize() {
        if (this.chart) {
            this.chart.reflow();
        }
    }
    _handle_config_update_change() {
        const config_update = this._clean_config(this.model.config_update);
        this.chart.update(config_update);
    }
    _clean_config(config) {
        updateJS(config, this.model);
        return config;
    }
}
HighChartView.__name__ = "HighChartView";
export class HighChart extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_HighChart() {
        this.prototype.default_view = HighChartView;
        this.define(({ Any }) => ({
            config: [Any],
            config_update: [Any],
            event: [Any],
        }));
        this.override({
            height: 400,
            width: 600
        });
    }
}
HighChart.__name__ = "HighChart";
HighChart.__module__ = "panel_highcharts.models.highchart";
HighChart.init_HighChart();
// https://api.highcharts.com/highcharts/plotOptions.series.point.events.mouseOver
function updateJS(config, model) {
    if (config === null) {
        return config;
    }
    for (var i = 0; i < Object.keys(config).length; i++) {
        const key = Object.keys(config)[i];
        const value = config[key];
        if (typeof value == "object") {
            updateJS(value, model);
        }
        else if (typeof value === "string") {
            if (value[0].charAt(0) === "@") {
                const eventKey = value.slice(1, value.length);
                config[key] = (event) => sendEvent(event, model, eventKey);
            }
            else if (value.startsWith('function') && value.indexOf("{") > -1 && value.lastIndexOf("}") > -1) {
                const start = value.indexOf("{");
                const end = value.lastIndexOf("}");
                const command = value.slice(start + 1, end);
                try {
                    config[key] = new Function(command);
                }
                catch (e) {
                    config[key] = null;
                    console.log("Could not set key '" + key + "' to function '" + command + "'. ", e);
                }
            }
        }
    }
}
function sendEvent(event, model, key = null) {
    const eventData = filterEventData(event, key);
    // To make sure event gets sent we add a uuid
    // https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid
    eventData.uuid = uuidv4();
    model.event = eventData;
}
function filterEventData(event, channel = null) {
    const eventData = {};
    if (channel !== null && channel !== "") {
        eventData.channel = channel;
    }
    eventData.type = event.type;
    updateEventdata(event, eventData);
    return eventData;
}
function updateEventdata(event, eventData) {
    if (event.hasOwnProperty("index") && event["index"] !== undefined) {
        eventData.index = event["index"];
    }
    if (event.hasOwnProperty("name") && event["name"] !== undefined) {
        eventData.name = event["name"];
    }
    if (event.hasOwnProperty("x") && event.x !== undefined) {
        eventData.x = event.x;
    }
    if (event.hasOwnProperty("y") && event.y !== undefined) {
        eventData.y = event.y;
    }
    if (event.hasOwnProperty("target")) {
        eventData.target = {};
        updateEventdata(event.target, eventData.target);
    }
    if (event.hasOwnProperty("series")) {
        eventData.series = {};
        updateEventdata(event.series, eventData.series);
    }
    if (event.hasOwnProperty("point")) {
        eventData.point = {};
        updateEventdata(event.point, eventData.point);
    }
}
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
//# sourceMappingURL=highchart.js.map