import * as p from "@bokehjs/core/properties";
import { HighBaseView, HighBase } from "./highbase";
export declare class HighChartView extends HighBaseView {
    create_chart(wn: any, el: HTMLElement, config: object): void;
}
export declare namespace HighChart {
    type Attrs = p.AttrsOf<Props>;
    type Props = HighBase.Props;
}
export interface HighChart extends HighBase.Attrs {
}
export declare class HighChart extends HighBase {
    static __module__: string;
    static init_HighChart(): void;
}
