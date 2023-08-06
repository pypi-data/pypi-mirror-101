// See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
// The view of the Bokeh extension/ HTML element
// Here you can define how to render the model as well as react to model changes or View events.
export class SketchView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.value.change, () => {
            this.render();
        });
    }
    render() {
        console.log("render");
        console.log(this.model);
        super.render();
        this.el.innerHTML = this.model.value;
        this.valueElement = this.el.firstElementChild;
        this.valueElement.addEventListener("click", () => { this.model.clicks += 1; }, false);
    }
}
SketchView.__name__ = "SketchView";
// The Bokeh .ts model corresponding to the Bokeh .py model
export class Sketch extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_Sketch() {
        this.prototype.default_view = SketchView;
        this.define(({ String, Int }) => ({
            value: [String, "<button style='width:100%'>Click Me</button>"],
            clicks: [Int, 0],
        }));
    }
}
Sketch.__name__ = "Sketch";
Sketch.__module__ = "panel_sketch.models.sketch";
Sketch.init_Sketch();
//# sourceMappingURL=sketch.js.map