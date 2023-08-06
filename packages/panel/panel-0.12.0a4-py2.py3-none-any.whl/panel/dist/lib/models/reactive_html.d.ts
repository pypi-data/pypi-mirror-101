import * as p from "@bokehjs/core/properties";
import { HTMLBox } from "@bokehjs/models/layouts/html_box";
import { LayoutDOM } from "@bokehjs/models/layouts/layout_dom";
import { PanelHTMLBoxView } from "./layout";
export declare class ReactiveHTMLView extends PanelHTMLBoxView {
    model: ReactiveHTML;
    html: string;
    _parent: any;
    _changing: boolean;
    _event_listeners: any;
    _mutation_observers: MutationObserver[];
    _script_fns: any;
    _state: any;
    initialize(): void;
    connect_signals(): void;
    connect_scripts(): void;
    disconnect_signals(): void;
    get child_models(): LayoutDOM[];
    build_child_views(): Promise<void>;
    update_layout(): void;
    render(): void;
    private _send_event;
    private _render_child;
    private _render_children;
    after_layout(): void;
    private _align_view;
    private _render_html;
    private _render_script;
    private _remove_mutation_observers;
    private _setup_mutation_observers;
    private _remove_event_listeners;
    private _setup_event_listeners;
    private _update;
    private _update_model;
}
export declare namespace ReactiveHTML {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        attrs: p.Property<any>;
        callbacks: p.Property<any>;
        children: p.Property<any>;
        data: p.Property<any>;
        events: p.Property<any>;
        html: p.Property<string>;
        looped: p.Property<string[]>;
        nodes: p.Property<string[]>;
        scripts: p.Property<any>;
    };
}
export interface ReactiveHTML extends ReactiveHTML.Attrs {
}
export declare class ReactiveHTML extends HTMLBox {
    properties: ReactiveHTML.Props;
    constructor(attrs?: Partial<ReactiveHTML.Attrs>);
    static __module__: string;
    static init_ReactiveHTML(): void;
}
