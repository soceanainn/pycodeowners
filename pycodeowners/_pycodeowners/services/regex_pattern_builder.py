import re


class RegexPatternBuilder:
    @classmethod
    def build(cls, pattern: str) -> re.Pattern:
        """compiles a new regexp object from a gitignore-style pattern string"""

        # Handle specific edge cases first
        if "***" in pattern:
            raise ValueError("Pattern cannot contain three consecutive asterisks")

        if not pattern:
            raise ValueError("Pattern cannot be empty")

        if pattern == "/":
            # "/" doesn't match anything
            return re.compile("^$")

        segments = pattern.split("/")

        if segments[0] == "":
            # Leading slash: match is relative to root
            segments = segments[1:]
        elif len(segments) == 1 or (len(segments) == 2 and segments[1] == ""):
            # No leading slash - check for a single segment pattern, which matches
            # relative to any descendent path (equivalent to a leading **/)
            if segments[0] != "**":
                segments.insert(0, "**")

        if len(segments) > 1 and segments[-1] == "":
            # Trailing slash is equivalent to "/**"
            segments[-1] = "**"
        sep = "/"
        last_seg_index = len(segments) - 1
        need_slash = False
        s = ""
        for i, seg in enumerate(segments):
            match seg:
                case "**":
                    if i == 0 and i == last_seg_index:
                        # If the pattern is just "**" we match everything
                        s += ".+"
                    elif i == 0:
                        # If the pattern starts with "**" we match any leading path segment
                        s += "(?:.+" + sep + ")?"
                        need_slash = False
                    elif i == last_seg_index:
                        #  If the pattern ends with "**" we match any trailing path segment
                        s += sep + ".*"
                    else:
                        # If the pattern contains "**" we match zero or more path segments
                        s += "(?:" + sep + ".+)?"
                        need_slash = True
                case "*":
                    if need_slash:
                        s += sep
                    s += "[^" + sep + "]+"
                    need_slash = True
                case _:
                    if need_slash:
                        s += sep
                    escape = False
                    for ch in seg:
                        if escape:
                            escape = False
                            s += re.escape(ch)
                            continue
                        # Other pathspec implementations handle character classes here (e.g.
                        # [AaBb]), but CODEOWNERS doesn't support that so we don't need to
                        match ch:
                            case "\\":
                                escape = True
                            case "*":
                                # Multi-character wildcard
                                s += "[^" + sep + "]*"
                            case "?":
                                # Single-character wildcard
                                s += "[^" + sep + "]"
                            case _:
                                s += re.escape(ch)

                    if i == last_seg_index:
                        # As there's no trailing slash (that'd hit the '**' case), we
                        # need to match descendent paths
                        s += "(?:" + sep + ".*)?"
                    need_slash = True

        return re.compile("^" + s + "$")
