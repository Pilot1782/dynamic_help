import logging
import traceback

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
    def __init__(self, bot, *_, skip_coms: list = None, skip_opts: list = None, combine: bool = True,
                 page_args: dict = None, logger=None):
        super().__init__()

        self.bot = bot
        self.skip_coms = {"help"}
        if skip_coms:
            self.skip_coms.update(skip_coms)
        self.skip_opts = {"ctx", "self", "kwargs", "args", "return"}
        if skip_opts:
            self.skip_opts.update(skip_opts)
        self.combine = combine

        self.page_args = {
            "ephemeral": True,
            "delete_after": 60,
        }
        self.page_args.update(page_args or {})

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("DynHelp")

    @slash_command(
        name="help",
        description="Shows this message.",
    )
    async def help(self, ctx: SlashContext):
        """
        Shows this message, which is a dynamically generated list of all the commands and their options.

        :param ctx:
        :return:
        """
        try:
            # get a list of all the commands
            commands = ctx.bot.interaction_tree

            embed = Embed(
                title="Help",
                description="Here's a list of all the commands.",
            )

            self.logger.debug(f"Tree: {commands}")

            for _, tree in commands.items():
                for name, com in tree.items():
                    tre = com.to_dict()
                    callback = com.callback
                    doc = callback.__doc__ if callback.__doc__ else ""

                    self.logger.debug(f"Command: {tre}")

                    if name in self.skip_coms:
                        continue

                    name = tre["name"]
                    description = tre["description"].strip() if "description" in tre else "No Description Set"

                    if len(doc) > len(
                            description) and doc != "partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n":
                        description = doc.strip()
                    dm = tre["dm_permission"]

                    self.logger.debug(f"Command: {name} - {description} - {dm}")

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
                            elif parsed_doc.short_description:
                                description = parsed_doc.short_description.strip()

                    embed.add_field(
                        name=f"`/{name}`",
                        value=f"{description.strip()}\n"
                              + (f"\nArgs:{'  '.join(options)}" if options else ""),
                        inline=True,
                    )
            await ctx.send(embed=embed, **self.page_args)
        except Exception as err:
            await ctx.send("An error occurred while running the command", ephemeral=True)
            self.logger.error(f"An error occurred while running the command:\n{traceback.format_exc()}")
            raise err
