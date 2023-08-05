var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ttgtcanvas:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ttgtcanvas',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

