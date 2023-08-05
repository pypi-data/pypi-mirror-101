import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export declare class HighChartView extends HTMLBoxView {
    model: HighChart;
    chart: any;
    connect_signals(): void;
    render(): void;
    after_layout(): void;
    _resize(): void;
    _handle_config_update_change(): void;
    _clean_config(config: object): object;
}
export declare namespace HighChart {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        config: p.Property<any>;
        config_update: p.Property<any>;
        event: p.Property<any>;
    };
}
export interface HighChart extends HighChart.Attrs {
}
export declare class HighChart extends HTMLBox {
    properties: HighChart.Props;
    constructor(attrs?: Partial<HighChart.Attrs>);
    static __module__: string;
    static init_HighChart(): void;
}
