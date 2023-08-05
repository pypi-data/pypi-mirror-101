var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');

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
var CanvasModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'CanvasModel',
        _view_name : 'CanvasView',
        _model_module : 'ttgtcanvas',
        _view_module : 'ttgtcanvas',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        current_call: '{}',
        method_return: '{}',

    })
});


// Custom View. Renders the widget model.
var CanvasView = widgets.DOMWidgetView.extend({
    
    // Defines how the widget gets rendered into the DOM
    render: function() {
        this.canvas = document.createElement('canvas');
        console.log(this.canvas);
        this.el.append(this.canvas);

        // Observe changes in the value traitlet in Python, and define
        // a custom callback.
        console.log("render", this)
        this.model.on('change:current_call', this.method_changed, this);
    },
    
    method_changed: function() {
        console.log("current_call");
        let current_call = JSON.parse(this.model.get('current_call'));
        console.log("current_call", this);
        let ret = this[current_call.method_name].apply(this, current_call.params);
        console.log("current_call", current_call)
        let that = this
        return Promise.resolve(ret).then(function(x) {
            console.log("reached in promise");
            let data = JSON.stringify({
              value: x,
              cb: +new Date,
              params: current_call.params, 
              method: current_call.method_name
            })
            console.log("setting return", data);
            that.model.set('method_return', data);
            that.model.save_changes();
            return data;
        })

    },
    
    update_div: function(msg, timeout) {
        console.log("update_div", msg);
        this.el.textContent = msg;
        return new Promise(function(resolve, reject) {
            setTimeout(resolve, timeout);
        })
    },
    
    
    
    
    draw_canvas: function() {
          var sun = new Image();
          var moon = new Image();
          var earth = new Image();
    
          sun.src = 'https://mdn.mozillademos.org/files/1456/Canvas_sun.png';
          moon.src = 'https://mdn.mozillademos.org/files/1443/Canvas_moon.png';
          earth.src = 'https://mdn.mozillademos.org/files/1429/Canvas_earth.png';
    
          let ctx = this.canvas.getContext('2d');
          ctx.globalCompositeOperation = 'destination-over';
          ctx.clearRect(0, 0, 300, 300); // clear canvas

          ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
          ctx.strokeStyle = 'rgba(0, 153, 255, 0.4)';
          ctx.save();
          ctx.translate(150, 150);

          // Earth
          var time = new Date();
          ctx.rotate(((2 * Math.PI) / 60) * time.getSeconds() + ((2 * Math.PI) / 60000) * time.getMilliseconds());
          ctx.translate(105, 0);
          ctx.fillRect(0, -12, 40, 24); // Shadow
          ctx.drawImage(earth, -12, -12);

          // Moon
          ctx.save();
          ctx.rotate(((2 * Math.PI) / 6) * time.getSeconds() + ((2 * Math.PI) / 6000) * time.getMilliseconds());
          ctx.translate(0, 28.5);
          ctx.drawImage(moon, -3.5, -3.5);
          ctx.restore();

          ctx.restore();

          ctx.beginPath();
          ctx.arc(150, 150, 105, 0, Math.PI * 2, false); // Earth orbit
          ctx.stroke();

          ctx.drawImage(sun, 0, 0, 300, 300);
          
          window.requestAnimationFrame(this.draw_canvas.bind(this));
    }
});


module.exports = {
    CanvasModel: CanvasModel,
    CanvasView: CanvasView
};
