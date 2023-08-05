import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export declare class HighBaseView extends HTMLBoxView {
    model: HighBase;
    chart: any;
    connect_signals(): void;
    render(): void;
    create_chart(wn: any, el: HTMLElement, config: object): void;
    after_layout(): void;
    _resize(): void;
    _handle_config_update_change(): void;
    _clean_config(config: object): object;
}
export declare namespace HighBase {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        config: p.Property<any>;
        config_update: p.Property<any>;
        event: p.Property<any>;
    };
}
export interface HighBase extends HighBase.Attrs {
}
export declare class HighBase extends HTMLBox {
    properties: HighBase.Props;
    constructor(attrs?: Partial<HighBase.Attrs>);
    static __module__: string;
    static init_HighBase(): void;
}
