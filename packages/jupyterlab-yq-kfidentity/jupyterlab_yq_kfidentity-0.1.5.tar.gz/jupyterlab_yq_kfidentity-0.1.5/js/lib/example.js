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
var HelloModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HelloModel',
        _view_name : 'HelloView',
        _model_module : 'jupyterlab-yq-kfidentity',
        _view_module : 'jupyterlab-yq-kfidentity',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : 'Hello World!'
    })
});
function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

function httpPost(url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function syncAndMinio()
{
    var baseUrl = location.origin
    var path = location.pathname
    var pathArray = path.split('/')
    var notebookPrefix = '/' + pathArray[1] + '/' + pathArray[2] + '/' + pathArray[3] + '/'
    var fullPath = baseUrl + notebookPrefix

    var xsrfToken = getCookie('_xsrf');

    httpPost(fullPath + 'yqid/sync?_xsrf=' + xsrfToken)
    httpPost(fullPath + 'yqid/minio?_xsrf=' + xsrfToken)
}

syncAndMinio(); //run function once on startup
setInterval(syncAndMinio, 60000) //each minute


// Custom View. Renders the widget model.
var HelloView = widgets.DOMWidgetView.extend({
    // Defines how the widget gets rendered into the DOM
    render: function() {
        this.value_changed();

        // Observe changes in the value traitlet in Python, and define
        // a custom callback.
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});


module.exports = {
    HelloModel: HelloModel,
    HelloView: HelloView
};
