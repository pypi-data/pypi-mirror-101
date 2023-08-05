var baseWigets = require("./base.js");
var Konva = require("konva");

var MazeModel = baseWigets.BaseModel.extend({
	defaults: _.extend(baseWigets.BaseModel.defaults, {
		_model_name: "MazeModel",
		_view_name: "MazeView",
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
		console.log(x);
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

class Beeper {
	constructor(obj) {
		Object.assign(this, obj);
	}
}

class Robot {
	constructor(obj) {
		Object.assign(this, obj);
		this.points = [];
		this.trace_enabled = false;
		this.traceColor = "black";
		this.trace = null;
		this.pending_moves = [];
		this.delay = 0.2;
		let that = this;
		new Konva.Image.fromURL(this.src, function (darthNode) {
			that.set_node(darthNode);
			darthNode.setAttrs({
				x: 100,
				y: 100,
			});
			that.layer.add(darthNode);
			that.layer.batchDraw();
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
		console.log(this.points);
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

		var anim = new Konva.Animation(function (frame) {
			that.node.x(x - 15);
			that.node.y(y - 15);
		}, this.layer);

		anim.start();

		let updated = this.node.position();
		if (updated.x === x && updated.y === y) {
			anim.stop();
		}
	}
}

var MazeView = baseWigets.BaseView.extend({
	// Defines how the widget gets rendered into the DOM
	render: function () {
		this.init();
		console.log("🚀 ~ file: maze.js ~ line 167 ~ this.el", this.el);
		this._elem = document.createElement("div");
		this._elem.setAttribute("id", "container");
		this.layer = new Konva.Layer();
		this.line_layer = new Konva.Layer();
		this.el.appendChild(this._elem);
		this.robots = [];
	},

	add_robot: function (robot_index, src, avenue, street, orientation, beepers) {
		this.robots[robot_index] =
			this.robots[robot_index] ||
			new Robot({
				layer: this.layer,
				line_layer: this.line_layer,
				avenue,
				street,
				orientation,
				beepers,
				src,
			});
	},

	move_to: function (robot_index, x, y) {
		let robot = this.robots[robot_index];
		robot.move_to(x, y);
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
		let robot = this.robots[robot_index];
		robot.delay = delay;
	},

	set_trace: function (robot_index, x, y, color = "blue") {
		let robot = this.robots[robot_index];
		robot.enable_trace();
		robot.traceColor = color;
		robot.add_point(x, y);
	},

	init_robot: function (robot_index) {
		let robot = this.robots[robot_index];
		robot.clear_trace();
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
		console.log(this.stage);

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
	},
});

module.exports = {
	MazeModel: MazeModel,
	MazeView: MazeView,
};
