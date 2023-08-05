import * as p from "@bokehjs/core/properties";
import { HighBaseView, HighBase } from "./highbase";
export declare class HighMapView extends HighBaseView {
    create_chart(wn: any, el: HTMLElement, config: object): void;
}
export declare namespace HighMap {
    type Attrs = p.AttrsOf<Props>;
    type Props = HighBase.Props;
}
export interface HighMap extends HighBase.Attrs {
}
export declare class HighMap extends HighBase {
    static __module__: string;
    static init_HighMap(): void;
}
