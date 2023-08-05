import ipywidgets as widgets
from traitlets import Unicode, Bool, validate, TraitError
from datetime import datetime
import asyncio
import json

def wait_for_change(widget, value):
    future = asyncio.Future()

    def get_value(change):
        future.set_result(change.new)
        widget.unobserve(get_value, value)

    widget.observe(get_value, value)
    return future


class Base(widgets.DOMWidget):
    _view_name = Unicode('BaseView').tag(sync=True)
    _model_name = Unicode('BaseModel').tag(sync=True)
    _view_module = Unicode('ttgtcanvas').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('ttgtcanvas').tag(sync=True)

    _view_module_version = Unicode('^0.1.3').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode('^0.1.3').tag(sync=True)

    current_call  = Unicode('{}').tag(sync=True)
    method_return = Unicode('{}').tag(sync=True)

    def js_call(self, method_name, params):
        return asyncio.ensure_future(self._js_call(method_name, datetime.now().strftime('%f'), params))

    async def _js_call(self, method_name, cb, params):
        self.current_call = json.dumps({'method_name': method_name, 'params': params, 'cb': cb})
        return await wait_for_change(self, "method_return")