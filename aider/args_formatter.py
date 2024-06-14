import argparse

from .dump import dump  # noqa: F401


class YamlHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        res = "\n\n"
        res += "#" * (len(heading) + 3)
        res += f"\n# {heading}"
        super().start_section(res)

    def _format_usage(self, usage, actions, groups, prefix):
        return ""

    def _format_text(self, text):
        return """
##########################################################
# Sample .aider.conf.yaml
# This file lists *all* the valid configuration entries.
# Place in your home dir, or at the root of your git repo.
##########################################################

"""

    def _format_action(self, action):
        if not action.option_strings:
            return ""

        parts = [""]

        metavar = action.metavar
        if not metavar and isinstance(action, argparse._StoreAction):
            metavar = "VALUE"

        default = action.default
        if default == argparse.SUPPRESS:
            default = ""
        elif isinstance(default, str):
            pass
        elif isinstance(default, list) and not default:
            default = ""
        elif action.default is not None:
            default = "true" if default else "false"
        else:
            default = ""

        if action.help:
            parts.append(f"## {action.help}")

        for switch in action.option_strings:
            if switch.startswith("--"):
                break
        switch = switch.lstrip("-")

        if isinstance(action, argparse._StoreTrueAction):
            default = False
        elif isinstance(action, argparse._StoreConstAction):
            default = False

        if default is False:
            default = "false"
        if default is True:
            default = "true"

        if default:
            parts.append(f"#{switch}: {default}\n")
        else:
            parts.append(f"#{switch}:\n")

        ###
        # parts.append(str(action))

        return "\n".join(parts) + "\n"

    def _format_action_invocation(self, action):
        return ""

    def _format_args(self, action, default_metavar):
        return ""


class MarkdownHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        super().start_section(f"## {heading}")

    def _format_usage(self, usage, actions, groups, prefix):
        res = super()._format_usage(usage, actions, groups, prefix)
        quote = "```\n"
        return quote + res + quote

    def _format_text(self, text):
        return ""

    def _format_action(self, action):
        if not action.option_strings:
            return ""

        parts = [""]

        metavar = action.metavar
        if not metavar and isinstance(action, argparse._StoreAction):
            metavar = "VALUE"

        for switch in action.option_strings:
            if switch.startswith("--"):
                break

        if metavar:
            parts.append(f"### `{switch} {metavar}`")
        else:
            parts.append(f"### `{switch}`")
        if action.help:
            parts.append(action.help + "  ")

        if action.default not in (argparse.SUPPRESS, None):
            parts.append(f"Default: {action.default}  ")

        if action.env_var:
            parts.append(f"Environment variable: `{action.env_var}`  ")

        if len(action.option_strings) > 1:
            parts.append("Aliases:")
            for switch in action.option_strings:
                if metavar:
                    parts.append(f"  - `{switch} {metavar}`")
                else:
                    parts.append(f"  - `{switch}`")

        return "\n".join(parts) + "\n"

    def _format_action_invocation(self, action):
        return ""

    def _format_args(self, action, default_metavar):
        return ""
