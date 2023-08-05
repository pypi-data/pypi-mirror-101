var widgets = require("@jupyter-widgets/base");
var _ = require("lodash");

// See example.py for the kernel counterpart to this file.

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var BaseModel = widgets.DOMWidgetModel.extend({
	defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
		_model_name: "BaseModel",
		_view_name: "BaseView",
		_model_module: "ttgtcanvas",
		_view_module: "ttgtcanvas",
		_model_module_version: "0.2.2",
		_view_module_version: "0.2.2",
		current_call: "{}",
		method_return: "{}",
	}),
});

// Custom View. Renders the widget model.
var BaseView = widgets.DOMWidgetView.extend({
	// Defines how the widget gets rendered into the DOM
	init: function () {
		this.model.on("change:current_call", this.method_changed, this);
	},

	method_changed: function () {
		console.log("current_call");
		let current_call = JSON.parse(this.model.get("current_call"));
		console.log("current_call", this);
		let ret =
			typeof this[current_call.method_name] === "function"
				? this[current_call.method_name].apply(this, current_call.params)
				: null;

		console.log("current_call", current_call);
		let that = this;
		return Promise.resolve(ret).then(function (x) {
			console.log("reached in promise");
			let data = JSON.stringify({
				value: x,
				cb: +new Date(),
				params: current_call.params,
				method: current_call.method_name,
			});
			console.log("setting return", data);
			that.model.set("method_return", data);
			that.model.save_changes();
			return data;
		});
	},
});

module.exports = {
	BaseModel: BaseModel,
	BaseView: BaseView,
};
