var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'jupyterlab-yq-kfidentity:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'jupyterlab-yq-kfidentity',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

