import ipywidgets as widgets
from traitlets import Unicode, Bool, validate, TraitError
from datetime import datetime
import asyncio
import json


# See js/lib/example.js for the frontend counterpart to this file.

def wait_for_change(widget, value):
    future = asyncio.Future()

    def get_value(change):
        future.set_result(change.new)
        widget.unobserve(get_value, value)

    widget.observe(get_value, value)
    return future


@widgets.register
class Canvas(widgets.DOMWidget, widgets.ValueWidget):
    """An example widget."""

    # Name of the widget view class in front-end
    _view_name = Unicode('CanvasView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('CanvasModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('ttgtcanvas').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('ttgtcanvas').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode('^0.1.3').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode('^0.1.3').tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    current_call  = Unicode('{}').tag(sync=True)
    method_return = Unicode('{}').tag(sync=True)
    
    def update_div(self, msg, timeout):
         return asyncio.ensure_future(self.js_call('update_div', datetime.now().strftime('%f'), ['Hello ' + msg, timeout]))
    
    def draw_canvas(self):
        return asyncio.ensure_future(self.js_call('draw_canvas', datetime.now().strftime('%f'), []))
    
    async def js_call(self, method_name, cb, params):
        print("calling {} with {}".format(method_name, params))
        self.current_call = json.dumps({'method_name': method_name, 'params': params, 'cb': cb})
        return await wait_for_change(self, "method_return")