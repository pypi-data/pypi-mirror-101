var widgets = require("@jupyter-widgets/base");
var _ = require("lodash");
var Konva = require("konva");
const { default: PQueue } = require("p-queue");
const queue = new PQueue({ concurrency: 1 });

var MazeModel = widgets.DOMWidgetModel.extend({
	defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
		_model_name: "MazeModel",
		_view_name: "MazeView",
		_model_module: "ttgtcanvas",
		_view_module: "ttgtcanvas",
		_model_module_version: "0.2.3",
		_view_module_version: "0.2.3",
		current_call: "{}",
		method_return: "{}",
	}),
});

const draw_beeper = function (layer, av, st, x, y, ts, val) {
	let radius = 0.6 * ts;
	let circle = new Konva.Circle({
		radius: radius,
		x: x,
		y: y,
		fill: "yellow",
		stroke: "orange",
		strokeWidth: 5,
		name: `beeper-${av}-${st}-circle`,
	});

	let num = new Konva.Text({
		text: val,
		x: x - 5,
		y: y - 7,
		fontSize: 18,
		name: `beeper-${av}-${st}-text`,
	});
	layer.add(circle, num);
};

const create_beepers = function (layer, beepers, left, bottom, ts) {
	const cr2xy = function (col, row) {
		return [left + ts * col, bottom - ts * row];
	};

	beepers.map(function (beeper) {
		let av = beeper.key[0];
		let st = beeper.key[1];
		const [x, y] = cr2xy(2 * av - 1, 2 * st - 1);
		let val = beeper.value;
		draw_beeper(layer, av, st, x, y, ts, val);
	});
};

const create_walls = function (layer, walls, left, bottom, ts) {
	const cr2xy = function (col, row) {
		return [left + ts * col, bottom - ts * row];
	};
	walls.map(function ([col, row]) {
		let points = [];
		if (col % 2 == 0) {
			points = [...cr2xy(col, row - 1), ...cr2xy(col, row + 1)];
		} else {
			points = [...cr2xy(col - 1, row), ...cr2xy(col + 1, row)];
		}
		let w = new Konva.Line({
			stroke: "darkred",
			strokeWidth: 10,
			closed: true,
			points: points,
		});
		layer.add(w);
	});
};

const create_av = function (layer, av, ts, l, b, t) {
	for (let i = 1; i < av; i++) {
		let x = l + ts * (2 * i);

		let line = new Konva.Line({
			stroke: "gray",
			points: [x, t, x, b],
		});

		let count = new Konva.Text({
			text: i,
			x: x - 2,
			y: b + ts - 10,
		});
		layer.add(line);
		layer.add(count);
	}
};

const create_st = function (layer, st, ts, l, b, r) {
	for (let i = 1; i < st; i++) {
		let y = b - ts * (2 * i);

		let line = new Konva.Line({
			stroke: "gray",
			points: [l, y, r, y],
		});

		let count = new Konva.Text({
			text: i,
			y: y - 2,
			x: l - ts + 5,
		});
		layer.add(line);
		layer.add(count);
	}
};

class Robot {
	constructor(obj) {
		Object.assign(this, obj);
		this.points = [];
		this.trace_enabled = false;
		this.traceColor = "black";
		this.trace = null;
		this.pending_moves = [];
		this.delay = 0.2;
	}

	set_image(src, index) {
		return new Promise((resolve, reject) => {
			let that = this;
			new Konva.Image.fromURL(this.src, function (darthNode) {
				that.set_node(darthNode);
				darthNode.setAttrs({
					x: 100,
					y: 100,
					name: `robot-${index}`,
				});
				that.layer.add(darthNode);
				that.layer.batchDraw();
				resolve(that);
			});
		});
	}

	set_node(node) {
		this.node = node;
		while (this.pending_moves.length > 0) {
			let [x, y] = this.pending_moves.shift();
			this.move_to(x, y);
		}
	}

	add_point(x, y) {
		this.points = this.points.concat([x, y]);
	}

	clear_trace() {
		this.points = [];
		this.line_layer.destroyChildren();
		this.line_layer.draw();
	}

	enable_trace() {
		this.trace_enabled = true;
	}

	draw_trace() {
		let trace = new Konva.Line({
			points: this.points.slice(Math.max(this.points.length - 4, 0)),
			stroke: this.traceColor,
		});
		this.line_layer.add(trace);
		this.line_layer.draw();
	}

	move_to(x, y) {
		if (!!!this.node) {
			this.pending_moves.push([x, y]);
			return;
		}
		let that = this;

		return new Promise(function (resolve, reject) {
			var anim = new Konva.Animation(function (frame) {
				that.node.x(x - 15);
				that.node.y(y - 15);
			}, that.layer);

			anim.start();
			setTimeout(resolve, that.delay * 1000);
			let updated = that.node.position();
			if (updated.x === x - 15 && updated.y === x - 15) {
				anim.stop();
			}
		}).then((res) => console.log("done", that.delay));
	}
}

var MazeView = widgets.DOMWidgetView.extend({
	// Defines how the widget gets rendered into the DOM

	method_changed: function () {
		let current_call = JSON.parse(this.model.get("current_call"));
		queue.add(() => {
			let ret =
				typeof this[current_call.method_name] === "function"
					? this[current_call.method_name].apply(this, current_call.params)
					: null;

			console.log("current_call in promise", current_call);
			let that = this;
			return Promise.resolve(ret).then(function (x) {
				// console.log("reached in promise");
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
		});
	},
	// Defines how the widget gets rendered into the DOM
	render: function () {
		this._elem = document.createElement("div");

		console.log("🚀 ~ file: maze.js ~ line 218 ~ this._elem", this);
		this._elem.setAttribute("id", "container");
		this.layer = new Konva.Layer();
		this.line_layer = new Konva.Layer();
		this.robots = [];
		this.el.appendChild(this._elem);
		this.method_changed();
		this.listenTo(this.model, "change:current_call", this.method_changed, this);
	},

	add_robot: function (robot_index, src, avenue, street, orientation, beepers) {
		if (this.robots[robot_index]) {
			return Promise.resolve("robot exists");
		}

		this.robots[robot_index] = new Robot({
			layer: this.layer,
			line_layer: this.line_layer,
			avenue,
			street,
			orientation,
			beepers,
			src,
		});

		return this.robots[robot_index].set_image(src, robot_index).then((res) => {
			console.log(res);
		});
	},

	move_to: function (robot_index, x, y) {
		let robot = this.robots[robot_index];
		return robot.move_to(x, y);
	},

	add_point: function (robot_index, x, y) {
		let robot = this.robots[robot_index];
		robot.add_point(x, y);
		robot.draw_trace();
	},

	remove_trace: function (robot_index) {
		let robot = this.robots[robot_index];
		robot.trace_enabled = false;
		robot.clear_trace();
	},

	set_pause: function (robot_index, delay) {
		console.log("pause");
		let robot = this.robots[robot_index];
		if (robot) {
			robot.delay = delay;
		}
		return Promise.resolve(delay);
	},

	set_trace: function (robot_index, x, y, color = "blue") {
		let robot = this.robots[robot_index];
		robot.enable_trace();
		robot.traceColor = color;
		robot.add_point(x, y);
	},

	init_robot: function (robot_index) {
		let robot = this.robots[robot_index];
		if (robot) {
			robot.clear_trace();
		}
	},

	add_beeper: function (av, st, x, y, val) {
		draw_beeper(this.layer, av, st, x, y, this.ts, val);
	},

	update_beeper: function (av, st, val) {
		let text = this.layer.find(`.beeper-${av}-${st}-text`);
		text.text(val);
		this.layer.draw();
	},

	remove_beeper: function (av, st) {
		let circle = this.layer.find(`.beeper-${av}-${st}-circle`);
		let text = this.layer.find(`.beeper-${av}-${st}-text`);
		if (circle) {
			circle.destroy();
		}
		if (text) {
			text.destroy();
		}
		this.layer.draw();
	},

	draw_grid: function (width, height, av, st, ts, walls, beepers) {
		this.stage = new Konva.Stage({
			container: "container",
			width: width,
			height: height,
		});

		// add canvas element
		this.stage.add(this.layer);
		this.stage.add(this.line_layer);
		//init
		this.ts = ts;
		let left = 2 * ts;
		let right = left + 2 * ts * av;
		let bottom = height - 2 * ts;
		let top = bottom - 2 * ts * st;

		// create avenues
		create_av(this.layer, av, ts, left, bottom, top);

		//create streets
		create_st(this.layer, st, ts, left, bottom, right);

		//border
		let line = new Konva.Line({
			stroke: "darkred",
			points: [left, bottom, right, bottom, right, top, left, top],
			strokeWidth: 10,
			closed: true,
		});
		this.layer.add(line);

		//create walls
		create_walls(this.layer, walls, left, bottom, ts);

		//create_beepers
		create_beepers(this.layer, beepers, left, bottom, ts);

		this.layer.draw();

		return Promise.resolve("done");
	},
});

module.exports = {
	MazeModel: MazeModel,
	MazeView: MazeView,
};
