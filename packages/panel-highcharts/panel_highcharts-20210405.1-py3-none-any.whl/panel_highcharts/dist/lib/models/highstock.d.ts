import * as p from "@bokehjs/core/properties";
import { HighBaseView, HighBase } from "./highbase";
export declare class HighStockView extends HighBaseView {
    create_chart(wn: any, el: HTMLElement, config: object): void;
}
export declare namespace HighStock {
    type Attrs = p.AttrsOf<Props>;
    type Props = HighBase.Props;
}
export interface HighStock extends HighBase.Attrs {
}
export declare class HighStock extends HighBase {
    static __module__: string;
    static init_HighStock(): void;
}
