from interactions.ext import Base, Version, VersionAuthor
from interactions import Extension, slash_command, SlashContext, Embed

version: Version = Version(
    version="1.0.0",
    author=VersionAuthor(
        name="Pilot1782",
        email="",
    ),
)

base = Base(
    name="interactions_dynamic_help",
    version=version,
    description="Unofficial Dynamic Help Command for interactions.py",
    link="https://github.com/Pilot1782/interactions-dynamic-help",
    packages=["interactions.ext.dynhelp"],
    requirements=["discord-py-interactions>=4.2.0"],
)


class DynHelp(Extension):
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

            for _, tree in commands.items():
                for name, com in tree.items():
                    if name == "Refresh":
                        continue
                    com = com.to_dict()

                    options = (
                        [
                            f"\n- `{option['name']}`: {option['description']} ({option['type']})"
                            for option in com["options"]
                        ]
                        if "options" in com
                        else []
                    )

                    embed.add_field(
                        name=f"`/{name}`",
                        value=f"{com['description']}\n"
                              + (f"Args:{'  '.join(options)}" if options else ""),
                        inline=True,
                    )
            await ctx.send(embed=embed, ephemeral=True, delete_after=60)
        except Exception as err:
            await ctx.send("An error occurred while running the command", ephemeral=True)
            raise err
