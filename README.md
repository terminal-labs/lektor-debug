## Lektor Debug

This Plugin provides a `{% debug %}` template tag that will render helpful debugging information in a template. To use, simply add this tag in a template, and run lektor server in development mode with `LEKTOR_DEV=1 lektor server`.

This plugin replaces Lektor's built-in, optional `{% debug %}` tag from Jinja2's Debug Extension. That tag is completely superceded by this plugins, so we just replace it.

This plugins tag can also be left in with no ill-effects. Unless the environment variable `LEKTOR_DEV=1` is set, `{% debug %}` will be a noop and return an empty string, unlike Lektor's current behavior which, since Jinja2's Debug Extension would not be added, would raise a `TemplateSyntaxError`.

### `{% debug %}` contents

This tag automatically renders as a collapsed `<detail>` html element, so it is minimally invasive unless you need it. When expanded, it will show a Python-ish dict with keys for:

- All fields available on `this`
- The complete `dir(this)`, which shows it's native attributes and methods (different from the above)
- All flowblocks and their fields
- All current template context, exactly like Jinja2's Debug Extension
- All available template filters, exactly like Jinja2's Debug Extension
- All available template tests, exactly like Jinja2's Debug Extension

The top-level keys are meant to quickly tell you what that piece of data is, but do not necessarily correspond to an available key in a real Python dict. For example, `this.fields` is not a key in any Lektor Python dict, but it's hopefully clear what this represents.

Flowblocks are listed as `this.<flowblock name>.blocks`, which is how you would access them in a template. Each flow field will present a list of dicts of all blocks' fields and their values.

This debug info is presented as a code block, ran through Lektor's markdown processor. Since that is the case, if you have [Lektor Markdown Highlighter](https://www.getlektor.com/plugins/lektor-markdown-highlighter/) installed and configured, this will also use the syntax highlighting for Python.

### Additional Template Context

This plugin also adds the following template variables globally:

- `{{ dir }}` Python's `dir` builtin
- `{{ str }}` Python's `str` builtin
- `{{ type }}` Python's `type` builtin
