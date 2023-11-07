import docstring_parser
from interactions import Extension, slash_command, SlashContext, Embed

option_types = {
    1: "SUB_COMMAND",
    2: "SUB_COMMAND_GROUP",
    3: "STRING",
    4: "INTEGER",
    5: "BOOLEAN",
    6: "USER",
    7: "CHANNEL",
    8: "ROLE",
    9: "MENTIONABLE",
    10: "NUMBER",
    11: "ATTACHMENT",
}


class DynHelp(Extension):
    def __init__(self, bot, skip_coms: list = None, skip_opts: list = None, combine: bool = True):
        super().__init__()

        self.bot = bot
        self.skip_coms = skip_coms or []
        self.skip_opts = ["ctx"] + (skip_opts or [])
        self.combine = combine

    @slash_command(
        name="help",
        description="Shows this message.",
    )
    async def help(self, ctx: SlashContext):
        try:
            # get a list of all the commands
            commands = ctx.bot.interaction_tree

            embed = Embed(
                title="Help",
                description="Here's a list of all the commands.",
            )

            print(f"Tree: {commands}")

            for _, tree in commands.items():
                for name, com in tree.items():
                    tre = com.to_dict()
                    callback = com.callback
                    doc = callback.__doc__ if callback.__doc__ else ""

                    print(f"Command: {tre}")

                    if name in self.skip_coms:
                        continue

                    name = tre["name"]
                    description = tre["description"].strip()

                    if len(doc) > len(
                            description) and doc != "partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n":
                        description = doc.strip()
                    dm = tre["dm_permission"]

                    print(f"Command: {name} - {description} - {dm}")

                    options = (
                        [
                            f"\n- `{name}`: {description} ({option_types[option['type']]})" + (
                                " DM allowed" if dm else "")
                            for option in tre["options"]
                        ]
                        if "options" in tre
                        else []
                    )

                    # parse options via docstring
                    if doc.strip() == description:
                        parsed_doc = docstring_parser.parse(doc)

                        if parsed_doc.params:
                            options = [
                                f"\n- `{param.arg_name}`: {param.description} ({option_types[param.type_name]})" + (
                                    " DM allowed" if dm else "")
                                for param in parsed_doc.params
                                if param.arg_name not in self.skip_opts
                            ]

                        if self.combine:
                            description = f"{parsed_doc.short_description.strip() if parsed_doc.short_description else ''}\n\n"
                            f"{parsed_doc.long_description.strip() if parsed_doc.long_description else parsed_doc.short_description.strip()}"
                        else:
                            if parsed_doc.long_description:
                                description = parsed_doc.long_description.strip()

                            if parsed_doc.short_description and not parsed_doc.long_description:
                                description = parsed_doc.short_description.strip()

                    embed.add_field(
                        name=f"`/{name}`",
                        value=f"{description.strip()}\n"
                              + (f"\nArgs:{'  '.join(options)}" if options else ""),
                        inline=True,
                    )
            await ctx.send(embed=embed, ephemeral=True, delete_after=60)
        except Exception as err:
            await ctx.send("An error occurred while running the command", ephemeral=True)
            raise err
