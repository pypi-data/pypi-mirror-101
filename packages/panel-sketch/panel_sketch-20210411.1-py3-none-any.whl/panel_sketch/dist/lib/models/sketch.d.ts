import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class SketchView extends HTMLBoxView {
    model: Sketch;
    valueElement: any;
    connect_signals(): void;
    render(): void;
}
export declare namespace Sketch {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        value: p.Property<string>;
        clicks: p.Property<number>;
    };
}
export interface Sketch extends Sketch.Attrs {
}
export declare class Sketch extends HTMLBox {
    properties: Sketch.Props;
    constructor(attrs?: Partial<Sketch.Attrs>);
    static __module__: string;
    static init_Sketch(): void;
}
