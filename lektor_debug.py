# -*- coding: utf-8 -*-
import os
import pprint
from pathlib import Path

from jinja2.ext import DebugExtension
from markupsafe import Markup

from lektor.pluginsystem import Plugin
from lektor.markdown import Markdown
from lektor.types.flow import FlowDescriptor


class LektorDebugExtension(DebugExtension):
    """Jinja extension for Lektor to replace Jinja's native Debug extension"""
    def _device_info_html(self):
        device_info = Path(__file__).parent / "device_info.html"
        with open(device_info) as fp:
            return fp.read()

    def _render(self, context) -> str:
        if not os.environ.get("LEKTOR_DEV") == "1":
            return ""

        raw = {}

        this = context.get('this')  # not always present
        if this:
            data = getattr(this, '_data', None)
            if data:
                raw['this.fields'] = data
                for k, v in data.items():
                    if isinstance(v, FlowDescriptor):
                        raw[f"flow: this.{k}.blocks"] = v._blocks
            raw['dir(this)'] = dir(this)

        raw.update({
            "context": context.get_all(),
            "filters": sorted(self.environment.filters.keys()),
            "tests": sorted(self.environment.tests.keys()),
        })
        md_str = f"""\
```python
{pprint.pformat(raw, depth=3, compact=True)}
```
"""
        options = {'type': 'markdown'}
        record = context['this']
        md = Markdown(md_str, record, options)
        device = self._device_info_html()
        return Markup(
            f"<details><summary>DEBUG INFO -></summary>{md}</details>"
            "<br><br>"
            f"<details><summary>DEVICE INFO -></summary>{device}</details>"
        )


class DebugPlugin(Plugin):
    name = 'Lektor Debug'
    description = 'A Lektor Plugin for Debugging Help'

    # XXX Occaisionally using on_before_build_all seems to sometimes error
    # with `TemplateSyntaxError: Encountered unknown tag 'debug'` and sometimes not.
    # Why? fixme
    def on_before_build_all(self, builder, **extra):
        if "jinja2.ext.DebugExtension" in self.env.jinja_env.extensions:
            del self.env.jinja_env.extensions["jinja2.ext.DebugExtension"]

        # Always add the extension so the tag always works. It is just a noop
        # unless LEKTOR_DEV==1. This let's us keep the tag in all the time.
        self.env.jinja_env.add_extension(LektorDebugExtension)

    def on_setup_env(self, **extra):
        self.env.jinja_env.globals['str'] = str
        self.env.jinja_env.globals['dir'] = dir
        self.env.jinja_env.globals['type'] = type
