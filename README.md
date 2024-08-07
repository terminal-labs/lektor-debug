## Lektor Debug

Example ran on the [Lektor Example Project's](https://github.com/lektor/lektor/tree/master/example) `/type` page:

![example.gif](https://raw.githubusercontent.com/terminal-labs/lektor-debug/main/example.gif)

This Plugin provides a `{% debug %}` template tag that will render helpful debugging information in a template. To use, simply add this tag in a template, and run lektor server in development mode with `LEKTOR_DEV=1 lektor server`.

This plugin replaces Lektor's built-in, optional `{% debug %}` tag from Jinja2's Debug Extension. That tag is completely superceded by this plugins, so we just replace it.

This plugins tag can also be left in with no ill-effects. Unless the environment variable `LEKTOR_DEV=1` is set, `{% debug %}` will be a noop and return an empty string, unlike Lektor's current behavior which, since Jinja2's Debug Extension would not be added, would raise a `TemplateSyntaxError`. **Note well,** that if you're trying to toggle in the same env, you will need a `lektor clean` in the middle.

### `{% debug %}` contents

#### DEBUG INFO

This tag automatically renders as a two collapsed `<detail>` html elements, so it is minimally invasive unless you need it. When the first, "DEBUG INFO", expanded, it will show a Python-ish dict with keys for:

- All fields available on `this`
- The complete `dir(this)`, which shows it's native attributes and methods (different from the above)
- All flowblocks and their fields
- All current template context, exactly like Jinja2's Debug Extension
- All available template filters, exactly like Jinja2's Debug Extension
- All available template tests, exactly like Jinja2's Debug Extension

The top-level keys are meant to quickly tell you what that piece of data is, but do not necessarily correspond to an available key in a real Python dict. For example, `this.fields` is not a key in any Lektor Python dict, but it's hopefully clear what this represents.

Flowblocks are listed as `this.<flowblock name>.blocks`, which is how you would access them in a template. Each flow field will present a list of dicts of all blocks' fields and their values.

This debug info is presented as a code block, ran through Lektor's markdown processor. Since that is the case, if you have [Lektor Markdown Highlighter](https://www.getlektor.com/plugins/lektor-markdown-highlighter/) installed and configured, this will also use the syntax highlighting for Python.

#### DEVICE INFO

The second collapsed `<detail>` element tells you the current actual and device width, resolution, orientation, and device pixel ratio. This is very handy when designing for multiple viewing devices and dimensions. If there's other items you'd like to see here, please submit a PR :)

### Additional Template Context

This plugin also adds the following template variables globally:

- `{{ dir }}` Python's `dir` builtin
- `{{ str }}` Python's `str` builtin
- `{{ type }}` Python's `type` builtin
