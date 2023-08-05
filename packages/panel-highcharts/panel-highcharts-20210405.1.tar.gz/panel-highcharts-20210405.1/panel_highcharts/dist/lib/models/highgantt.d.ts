import * as p from "@bokehjs/core/properties";
import { HighBaseView, HighBase } from "./highbase";
export declare class HighGanttView extends HighBaseView {
    create_chart(wn: any, el: HTMLElement, config: object): void;
}
export declare namespace HighGantt {
    type Attrs = p.AttrsOf<Props>;
    type Props = HighBase.Props;
}
export interface HighGantt extends HighBase.Attrs {
}
export declare class HighGantt extends HighBase {
    static __module__: string;
    static init_HighGantt(): void;
}
