# Dynamic Help

## Description

A dynamically generated help command for interactions.py that allows for >100 character command descriptions

## Usage

Install via pypi

```sh
pip install interactions-dynamic-help
```

Then load the extension into your bot

```python
from interactions import Client

bot = Client()

...

bot.load_extension("interactions.ext.dynhelp")
bot.start("Token")
```

## Using longer descriptions

Longer description is done with a docstring.

**If you are using a docstring longer than 100 chars, you MUST provide a description in the slash_command,
otherwise the docstring will be used as the description**

```python
from interactions import Client, slash_command

bot = Client()


@slash_command(
    name="test",
    description="This is a test command",
)
async def test(ctx):
    """This is a test command (parsed as a short description and ignored if a long description is provided)

    This is a longer description that will be used in the help command and is longer than 100 chars
    - this is parsed as part of the long description
    """
    await ctx.respond("Test")


bot.load_extension("interactions.ext.dynhelp")
bot.start("Token")
```

You can specify to combine the short and long description by adding `combine=True` to the decorator

```python
bot.load_extension("interactions.ext.dynhelp", combine=True)
```

## Skipping commands and/or options

By defualt the `ctx` and `bot` parameters are skipped, but you can skip more by adding `skip_coms` adn `skip_opts` to
the decorator

```python
bot.load_extension("interactions.ext.dynhelp", skip_coms=["test"], skip_opts=["test"])
```

## Custom args to the paginator

These can be added by adding `paginator_args` to the decorator, your args will be added to the default args which are

```json
{
  "ephemeral": true,
  "delete_after": 60
}
```

```python
bot.load_extension("interactions.ext.dynhelp", paginator_args={"timeout": 60})
```
