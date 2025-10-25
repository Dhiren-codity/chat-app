"""
Reusable syntax repair utilities for test files.

This module contains AST-aware syntax repair methods extracted from test_orchestrator.py
to be used by both the test generation pipeline and the auto-fixer.
"""

import ast
import re
import logging

logger = logging.getLogger(__name__)


class SyntaxRepairer:
    """AST-aware syntax repair for Python test files."""

    def repair_file(self, content: str, max_passes: int = 3) -> tuple[bool, str]:
        """
        Attempt to repair syntax errors in Python code with multiple passes.

        Args:
            content: Python code to repair
            max_passes: Maximum number of repair passes (default 3)

        Returns:
            (success, repaired_content)
        """
        try:
            ast.parse(content)
            return True, content  # Already valid
        except SyntaxError:
            pass  # Continue with repairs

        # Multi-pass repair - try up to max_passes times
        current_content = content
        for pass_num in range(1, max_passes + 1):
            logger.info(f"🔧 Syntax repair pass {pass_num}/{max_passes}")

            try:
                ast.parse(current_content)
                logger.info(f"✅ Code is valid after pass {pass_num}")
                return True, current_content
            except SyntaxError as e:
                logger.info(f"Pass {pass_num} - Attempting to repair syntax error: {e}")
                repaired = self._repair_syntax_error(current_content, e)

                # Check if we made progress
                if repaired == current_content:
                    logger.warning(f"Pass {pass_num} made no changes - stopping")
                    break

                current_content = repaired

        # Final validation
        try:
            ast.parse(current_content)
            logger.info("✅ Successfully repaired all syntax errors")
            return True, current_content
        except SyntaxError as e:
            logger.warning(f"⚠️ After {max_passes} passes, still has errors: {e}")
            # Return the best effort repair
            return False, current_content

    def _repair_syntax_error(self, content: str, error: SyntaxError) -> str:
        """Dispatch to appropriate repair strategy based on error type."""
        error_line = error.lineno - 1 if error.lineno else 0
        error_msg = str(error.msg).lower()

        logger.info(f"🔧 Repairing syntax error at line {error_line + 1}: {error_msg}")

        # PROACTIVE: Always try removing orphaned brackets first
        # This handles orphaned parametrize data, fixture closing brackets, etc.
        content_before = content
        content = self._remove_orphaned_bracket_lines(content)
        if content != content_before:
            # We removed some orphaned brackets - normalize indentation
            content = self._normalize_file_indentation(content)

            # Try parsing again
            try:
                ast.parse(content)
                logger.info("✅ Fixed by proactively removing orphaned brackets")
                return content
            except SyntaxError as e:
                # Still has errors after orphaned bracket removal
                # Update error info and continue with specific repairs
                error_line = e.lineno - 1 if e.lineno else 0
                error_msg = str(e.msg).lower()
                logger.info(f"🔧 After orphaned bracket removal, still has error at line {error_line + 1}: {error_msg}")

        # Check error type and apply appropriate fix
        if (
            "unmatched" in error_msg
            or "was never closed" in error_msg
            or "does not match" in error_msg  # e.g., "')' does not match '['"
            or ("expected" in error_msg
                and ("(" in error_msg or "[" in error_msg or "{" in error_msg))
        ):
            # Bracket-related errors - try fixing unclosed function calls first
            # (common in Flask tests with unclosed json={})
            content = self._fix_unclosed_function_calls(content)
            try:
                ast.parse(content)
                logger.info("✅ Fixed by closing unclosed function calls")
            except SyntaxError:
                # Try bracket-specific repairs
                content = self._repair_bracket_mismatches(content, error_line)
        elif "unexpected indent" in error_msg or "unindent" in error_msg or "expected an indented block" in error_msg:
            # First try fixing empty blocks (add 'pass' where needed)
            content = self._fix_empty_blocks(content)
            try:
                ast.parse(content)
                logger.info("✅ Fixed by adding 'pass' to empty blocks")
            except SyntaxError:
                # Try fixing orphaned decorators (fixtures with wrong indentation)
                content = self._fix_orphaned_decorators(content)
                try:
                    ast.parse(content)
                    logger.info("✅ Fixed by moving/removing orphaned decorators")
                except SyntaxError:
                    # Then try normalizing file-wide indentation
                    content = self._normalize_file_indentation(content)
                    # Then apply specific indentation fixes if needed
                    try:
                        ast.parse(content)
                        logger.info("✅ Fixed by file-wide indentation normalization")
                    except SyntaxError:
                        content = self._repair_indentation(content, error_line)
        elif "invalid syntax" in error_msg:
            # First try fixing unclosed function calls (common in Flask tests)
            content = self._fix_unclosed_function_calls(content)
            try:
                ast.parse(content)
                logger.info("✅ Fixed by closing unclosed function calls")
            except SyntaxError:
                content = self._repair_invalid_syntax(content, error_line)
        elif "return" in error_msg and "outside" in error_msg:
            content = self._remove_module_level_returns(content)
        else:
            # Try generic bracket repair as fallback
            logger.info("🔧 Trying generic bracket repair as fallback")
            content = self._repair_bracket_mismatches(content, error_line)

        # CRITICAL: After any repair, also check for and fix module-level returns
        content = self._remove_module_level_returns(content)
        content = self._remove_module_level_returns(
            content
        )  # Call twice to ensure it's applied

        return content

    def _repair_bracket_mismatches(self, content: str, error_line: int) -> str:
        """
        AST-aware bracket repair that understands Python structure.

        Uses AST to identify valid bracket contexts and only repairs
        actual mismatches without breaking indentation.
        """
        lines = content.split("\n")

        # Strategy 0: Fix bracket TYPE mismatches (e.g., '[' closed with ')')
        lines = self._fix_bracket_type_mismatch(lines, error_line)

        # Try parsing after type mismatch fix - might be enough!
        try:
            ast.parse("\n".join(lines))
            logger.info("✅ Fixed by bracket type mismatch repair")
            return "\n".join(lines)
        except SyntaxError:
            pass  # Continue with other repairs

        # Strategy 1: Try to parse each decorator separately
        # Decorators are the most common source of bracket issues
        decorator_pattern = re.compile(r"^(\s*)@(\w+\.)*\w+\s*\(")

        for line_num, line in enumerate(lines):
            if decorator_pattern.match(line):
                # Extract just this decorator
                indent = len(line) - len(line.lstrip())
                decorator_lines = [line]

                # Collect continuation lines
                for i in range(line_num + 1, len(lines)):
                    next_line = lines[i]
                    next_indent = len(next_line) - len(next_line.lstrip())

                    # Stop at next statement or less indented line
                    if next_line.strip() and (
                        next_indent <= indent
                        or next_line.strip().startswith(("def ", "class ", "@"))
                    ):
                        break
                    decorator_lines.append(next_line)

                # Try to parse this decorator
                decorator_text = "\n".join(decorator_lines)
                if not self._is_balanced_brackets(decorator_text):
                    logger.info(f"🔍 Unbalanced decorator at line {line_num + 1}")

                    # Fix by adding missing closing brackets
                    fixed_decorator = self._balance_decorator_brackets(decorator_text)

                    # Replace in original lines
                    fixed_lines = fixed_decorator.split("\n")
                    for i, fixed_line in enumerate(fixed_lines):
                        if line_num + i < len(lines):
                            lines[line_num + i] = fixed_line

        return "\n".join(lines)

    def _is_balanced_brackets(self, code: str) -> bool:
        """Check if brackets are balanced, ignoring strings."""
        stack = []
        bracket_map = {"(": ")", "[": "]", "{": "}"}
        in_string = False
        string_char = None
        escape_next = False

        for char in code:
            if escape_next:
                escape_next = False
                continue
            if char == "\\":
                escape_next = True
                continue
            if not in_string and char in ['"', "'"]:
                in_string = True
                string_char = char
            elif in_string and char == string_char:
                in_string = False
            elif not in_string:
                if char in bracket_map:
                    stack.append(char)
                elif char in bracket_map.values():
                    if not stack:
                        return False
                    expected = bracket_map[stack[-1]]
                    if expected != char:
                        return False
                    stack.pop()

        return len(stack) == 0

    def _balance_decorator_brackets(self, decorator: str) -> str:
        """Add missing closing brackets to a decorator."""
        stack = []
        bracket_map = {"(": ")", "[": "]", "{": "}"}
        in_string = False
        string_char = None
        escape_next = False

        for char in decorator:
            if escape_next:
                escape_next = False
                continue
            if char == "\\":
                escape_next = True
                continue
            if not in_string and char in ['"', "'"]:
                in_string = True
                string_char = char
            elif in_string and char == string_char:
                in_string = False
            elif not in_string:
                if char in bracket_map:
                    stack.append(char)
                elif char in bracket_map.values():
                    if stack and bracket_map[stack[-1]] == char:
                        stack.pop()

        # Add missing closing brackets
        closing = "".join(bracket_map[b] for b in reversed(stack))

        # Find the right place to add (end of last non-empty line)
        lines = decorator.split("\n")
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip():
                lines[i] = lines[i].rstrip() + closing
                logger.info(f"🔧 Added closing brackets: {closing}")
                break

        return "\n".join(lines)

    def _fix_bracket_type_mismatch(self, lines: list, error_line: int) -> list:
        """
        Fix bracket type mismatches like '[' being closed with ')'.

        Common pattern: Parametrize decorators with wrong closing bracket.
        Example:
            @pytest.mark.parametrize("arg", [
                (1, 2),
                (3, 4),
            )  # Wrong! Should be ])
        """
        # Look backwards from error line to find opening bracket
        bracket_map = {"(": ")", "[": "]", "{": "}"}
        reverse_map = {v: k for k, v in bracket_map.items()}

        # Track bracket stack for the region around error
        start_line = max(0, error_line - 10)
        end_line = min(len(lines), error_line + 5)

        stack = []
        in_string = False
        string_char = None

        for i in range(start_line, end_line):
            line = lines[i]
            for j, char in enumerate(line):
                # Track strings to ignore brackets inside them
                if char in ['"', "'"] and (j == 0 or line[j-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None
                    continue

                if in_string:
                    continue

                if char in bracket_map:
                    stack.append((char, i, j))
                elif char in reverse_map:
                    if stack:
                        opening_char, opening_line, opening_col = stack[-1]
                        expected_closing = bracket_map[opening_char]
                        if char == expected_closing:
                            stack.pop()
                        elif i == error_line:
                            # WRONG closing bracket on error line!
                            logger.info(
                                f"🔧 Bracket type mismatch at line {i+1}: "
                                f"'{opening_char}' on line {opening_line+1} closed with '{char}' instead of '{expected_closing}'"
                            )
                            # STRATEGY: Check if this is the ONLY character on the line (like "),")
                            # If so, REPLACE it. Otherwise, INSERT before it.
                            line_after_char = line[j+1:].strip()
                            line_before_char = line[:j].strip()

                            # If the line is just the wrong bracket (possibly with comma/whitespace)
                            # AND the stack only has one item, REPLACE it
                            if len(stack) == 1 and line_after_char in ['', ','] and not line_before_char:
                                # Replace the wrong bracket with the correct one
                                lines[i] = line[:j] + expected_closing + line[j+1:]
                                logger.info(f"   Fixed: replaced '{char}' with '{expected_closing}'")
                            else:
                                # INSERT the correct closing bracket BEFORE the wrong one
                                # This handles cases like: `)` should be `])`
                                lines[i] = line[:j] + expected_closing + line[j:]
                                logger.info(f"   Fixed: inserted '{expected_closing}' before '{char}'")
                            return lines

        return lines

    def _fix_unclosed_function_calls(self, content: str) -> str:
        """
        Fix unclosed function calls - common in Flask test code.

        Pattern:
        response = client.post('/route', json={
            'key': 'value'
        # MISSING: })
        assert response.status_code == 200  # ← Syntax error here!

        We detect unclosed brackets and add the missing closing brackets.
        """
        lines = content.split("\n")
        result = []

        # Track bracket state globally across ALL lines
        global_stack = []
        in_string = False
        string_char = None
        escape_next = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # BEFORE adding this line, check if it starts a new statement
            # while we still have unclosed brackets
            if global_stack and stripped and (
                stripped.startswith("assert ")
                or stripped.startswith("def ")
                or stripped.startswith("@")
                or stripped.startswith("class ")
                or stripped.startswith("return ")
                or stripped.startswith("raise ")
            ):
                # New statement detected with unclosed brackets!
                # Add closing brackets BEFORE this line
                closing = ""
                for bracket in reversed(global_stack):
                    if bracket == "(":
                        closing += ")"
                    elif bracket == "[":
                        closing += "]"
                    elif bracket == "{":
                        closing += "}"

                # Match indentation of dict/json opening
                indent = 4
                if result:
                    prev_line = result[-1]
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    indent = prev_indent

                closing_line = " " * indent + closing
                logger.info(
                    f"🔧 Added closing brackets '{closing}' before line {i+1} (new statement)"
                )
                result.append(closing_line)
                global_stack = []
                in_string = False

            # Now analyze THIS line and update bracket state
            for char in line:
                if escape_next:
                    escape_next = False
                    continue
                if char == "\\":
                    escape_next = True
                    continue

                if not in_string and char in ['"', "'"]:
                    in_string = True
                    string_char = char
                elif in_string and char == string_char:
                    in_string = False
                    string_char = None
                elif not in_string:
                    if char in "({[":
                        global_stack.append(char)
                    elif char in ")}]":
                        if global_stack:
                            global_stack.pop()

            # Add this line to result
            result.append(line)

        # If brackets still unclosed at EOF, close them
        if global_stack:
            closing = ""
            for bracket in reversed(global_stack):
                if bracket == "(":
                    closing += ")"
                elif bracket == "[":
                    closing += "]"
                elif bracket == "{":
                    closing += "}"

            indent = 4
            if result:
                prev_line = result[-1]
                prev_indent = len(prev_line) - len(prev_line.lstrip())
                indent = prev_indent

            closing_line = " " * indent + closing
            logger.info(f"🔧 Added closing brackets '{closing}' at end of file")
            result.append(closing_line)

        return "\n".join(result)

    def _remove_orphaned_bracket_lines(self, content: str) -> str:
        """
        Remove lines that contain ONLY closing brackets (orphaned after fixture removal).

        Patterns to detect:
        - Lines with only ]
        - Lines with only )
        - Lines with only ])
        - Lines with combinations like )])
        - Lines with whitespace + brackets only
        - Orphaned parametrize data like: (1, 200),
        - Lines ending with ]) (end of parametrize decorator)

        These are typically left behind when fixture definitions or decorators
        are removed but their closing brackets/data remain.

        CRITICAL: Preserves proper indentation after removal.
        """
        lines = content.split("\n")
        result = []
        removed_count = 0
        in_orphaned_parametrize = False

        # Track the next non-empty line after orphaned content
        # to ensure proper indentation is maintained
        last_preserved_line_indent = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Pattern 1: Lines with ONLY closing brackets
            if stripped and all(c in ")]}" for c in stripped):
                logger.info(
                    f"🔧 Removing orphaned bracket line {i + 1}: '{stripped}'"
                )
                removed_count += 1
                in_orphaned_parametrize = False
                # Check if next line needs indentation adjustment
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip().startswith(("@", "def ", "class ")):
                        # Next line is a decorator or definition, ensure it's at proper indent
                        last_preserved_line_indent = len(line) - len(line.lstrip())
                continue

            # Pattern 2: Orphaned parametrize data (tuple lines)
            # These look like: (1, 200), or (999, 200),  # comment
            # BUT be careful not to remove valid parametrize data!
            if (
                stripped
                and stripped.startswith("(")
                and (stripped.endswith(",") or stripped.rstrip().endswith(","))
            ):
                # Check if this might be part of a function call or valid structure
                # by looking at previous AND next non-empty lines
                prev_line_idx = i - 1
                while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                    prev_line_idx -= 1

                next_line_idx = i + 1
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1

                is_orphaned = False
                if prev_line_idx >= 0:
                    prev_stripped = lines[prev_line_idx].strip()

                    # Check next line if available
                    has_valid_continuation = False
                    if next_line_idx < len(lines):
                        next_stripped = lines[next_line_idx].strip()
                        # If next line continues the structure or closes it, this is valid
                        if (
                            next_stripped.startswith("(")  # Another tuple
                            or next_stripped.startswith("]")  # List closing
                            or next_stripped.endswith("])")  # Parametrize closing
                            or next_stripped.startswith("def ")  # Function definition after
                            or "pytest.mark.parametrize" in prev_stripped  # Part of parametrize decorator
                        ):
                            has_valid_continuation = True

                    # If previous line is a function call, list opening, tuple continuation,
                    # or a list/dict literal assignment, then this line is valid
                    # Also check for @pytest.mark.parametrize in recent lines
                    if (
                        prev_stripped.endswith("(")
                        or prev_stripped.endswith("[")
                        or prev_stripped.endswith(",")  # Continuation of tuple/list
                        or "def " in prev_stripped
                        or prev_stripped.endswith("= [")
                        or prev_stripped.endswith("= (")
                        or "pytest.mark.parametrize" in prev_stripped
                        or has_valid_continuation
                    ):
                        # This is valid structure - DON'T remove
                        is_orphaned = False
                    else:
                        # Look back up to 5 lines for @pytest.mark.parametrize
                        found_parametrize = False
                        for lookback_idx in range(max(0, i - 5), i):
                            if "pytest.mark.parametrize" in lines[lookback_idx]:
                                found_parametrize = True
                                break

                        if found_parametrize:
                            # This is part of parametrize - DON'T remove
                            is_orphaned = False
                        else:
                            # This looks like orphaned data
                            is_orphaned = True
                elif prev_line_idx < 0:
                    # No previous line - this is definitely orphaned
                    is_orphaned = True

                if is_orphaned:
                    logger.info(
                        f"🔧 Removing orphaned parametrize data line {i + 1}: '{stripped[:60]}...'"
                    )
                    removed_count += 1
                    in_orphaned_parametrize = True
                    continue

            # Pattern 3: If we detected orphaned parametrize, continue removing
            # until we hit the closing ])
            if in_orphaned_parametrize:
                logger.info(
                    f"🔧 Removing continuation of orphaned parametrize {i + 1}: '{stripped[:60]}...'"
                )
                removed_count += 1
                if stripped.endswith("])"):
                    in_orphaned_parametrize = False
                continue

            # Keep this line
            result.append(line)

        if removed_count > 0:
            logger.info(f"🔧 Removed {removed_count} orphaned bracket/parametrize line(s)")

        return "\n".join(result)

    def _repair_bracket_mismatches_v2(self, content: str, error_line: int) -> str:
        """
        Alternative bracket repair: scan and balance brackets line by line.

        This is a fallback if v1 doesn't work.
        """
        lines = content.split("\n")

        # Count total brackets in file (ignoring strings)
        total_counts = {"(": 0, ")": 0, "[": 0, "]": 0, "{": 0, "}": 0}

        for line in lines:
            in_string = False
            string_char = None
            escape_next = False

            for char in line:
                if escape_next:
                    escape_next = False
                    continue
                if char == "\\":
                    escape_next = True
                    continue
                if not in_string and char in ['"', "'"]:
                    in_string = True
                    string_char = char
                elif in_string and char == string_char:
                    in_string = False
                elif not in_string and char in total_counts:
                    total_counts[char] += 1

        # Check for imbalances
        for opening, closing in [("(", ")"), ("[", "]"), ("{", "}")]:
            diff = total_counts[opening] - total_counts[closing]

            if diff > 0:
                # More opening than closing - add closing brackets
                closing_to_add = closing * diff
                lines[error_line] = lines[error_line].rstrip() + closing_to_add
                logger.info(
                    f"🔧 Added {diff} '{closing}' bracket(s) to line {error_line + 1}"
                )

            elif diff < 0:
                # More closing than opening - remove extra closing brackets
                # Find and remove extra closing brackets at error line
                line = lines[error_line]
                brackets_to_remove = abs(diff)

                # Remove from right to left
                new_line = line
                for _ in range(brackets_to_remove):
                    last_idx = new_line.rfind(closing)
                    if last_idx != -1:
                        new_line = new_line[:last_idx] + new_line[last_idx + 1 :]

                lines[error_line] = new_line
                logger.info(
                    f"🔧 Removed {abs(diff)} extra '{closing}' bracket(s) from line {error_line + 1}"
                )

        return "\n".join(lines)

    def _repair_indentation(self, content: str, error_line: int) -> str:
        """
        AST-aware indentation repair.

        Fixes indentation based on Python structure, not just removing indent.
        """
        lines = content.split("\n")

        if error_line >= len(lines):
            return content

        error_line_text = lines[error_line]
        current_indent = len(error_line_text) - len(error_line_text.lstrip())

        # Find the expected indent by looking at context
        expected_indent = 0

        # Look backwards for the most recent def/class/if/for/etc
        for i in range(error_line - 1, -1, -1):
            prev_line = lines[i].strip()
            if not prev_line:
                continue

            prev_indent = len(lines[i]) - len(lines[i].lstrip())

            # If previous line starts a block, indent is prev + 4
            if prev_line.endswith(":"):
                expected_indent = prev_indent + 4
                break
            # If previous line is normal, use same indent
            elif not prev_line.startswith(("@", "#")):
                expected_indent = prev_indent
                break

        # Apply the expected indentation
        fixed_line = " " * expected_indent + error_line_text.lstrip()
        lines[error_line] = fixed_line

        logger.info(
            f"🔧 Fixed indentation: {current_indent} → {expected_indent} spaces"
        )

        return "\n".join(lines)

    def _repair_invalid_syntax(self, content: str, error_line: int) -> str:
        """
        Repair generic invalid syntax.

        NOTE: We already tried _fix_unclosed_function_calls before this.
        At this point, we can't fix it generically, so return unchanged.
        NEVER comment out code - that makes things worse!
        """
        logger.info(f"🔧 Cannot repair invalid syntax at line {error_line + 1} - returning unchanged")
        return content

    def _remove_module_level_returns(self, content: str) -> str:
        """
        Remove return statements at module level.

        Generic approach: Remove any return not inside a function.
        """
        lines = content.split("\n")
        fixed_lines = []
        in_function = False
        function_indent = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            current_indent = len(line) - len(line.lstrip())

            # Track function definitions
            if stripped.startswith("def "):
                in_function = True
                function_indent = current_indent
                fixed_lines.append(line)
                logger.info(
                    f"🔧 Entered function at line {i + 1}, indent={function_indent}"
                )
                continue

            # Track when we exit a function (indent goes back to function level or less)
            if (
                in_function
                and current_indent <= function_indent
                and stripped
                and not stripped.startswith("def ")
            ):
                in_function = False
                logger.info(
                    f"🔧 Exited function at line {i + 1}, indent={current_indent}"
                )

            # Remove module-level returns
            if stripped.startswith("return ") and not in_function:
                logger.info(
                    f"🔧 Removed module-level return: {stripped} (line {i + 1})"
                )
                continue

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def _fix_empty_blocks(self, content: str) -> str:
        """
        Fix empty code blocks by adding 'pass' statements.

        Handles:
        - if/elif/else with no body
        - for/while loops with no body
        - function definitions with no body
        - try/except/finally with no body
        """
        lines = content.split("\n")
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check if this is a block-starting statement
            is_block_start = (
                stripped.startswith(("if ", "elif ", "else:", "for ", "while "))
                or stripped.startswith(("def ", "async def ", "class "))
                or stripped.startswith(("try:", "except", "finally:", "with "))
            )

            if is_block_start and stripped.endswith(":"):
                # This starts a block - check if next line is indented
                result.append(line)
                current_indent = len(line) - len(line.lstrip())
                expected_indent = current_indent + 4

                # Look at next non-empty line
                j = i + 1
                next_line = None
                while j < len(lines):
                    if lines[j].strip():  # Found non-empty line
                        next_line = lines[j]
                        break
                    j += 1

                if next_line is None:
                    # End of file - add pass
                    result.append(" " * expected_indent + "pass")
                    logger.info(f"Added 'pass' at EOF after line {i + 1}: {stripped[:50]}")
                else:
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= current_indent:
                        # Next line is not indented properly - empty block!
                        result.append(" " * expected_indent + "pass")
                        logger.info(f"Added 'pass' after line {i + 1}: {stripped[:50]}")

                i += 1
                continue

            result.append(line)
            i += 1

        return "\n".join(result)

    def _fix_orphaned_decorators(self, content: str) -> str:
        """
        Fix decorators that are orphaned or have wrong indentation.

        Handles:
        - @pytest.fixture at wrong indentation (should be module-level)
        - Decorators without following function
        - Decorators inside classes when they should be module-level
        """
        lines = content.split("\n")
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check if this is a decorator
            if stripped.startswith("@"):
                current_indent = len(line) - len(line.lstrip())

                # Check what follows this decorator
                j = i + 1
                # Skip blank lines and additional decorators
                while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith("@")):
                    j += 1

                if j >= len(lines):
                    # Orphaned decorator at end of file - remove it
                    logger.info(f"Removing orphaned decorator at EOF line {i + 1}: {stripped}")
                    i += 1
                    continue

                next_line = lines[j]
                next_stripped = next_line.strip()

                # Check if the next non-decorator line is a function definition
                if next_stripped.startswith(("def ", "async def ", "class ")):
                    # This is a valid decorator - but check indentation
                    # Fixtures should be at module level (indent 0)
                    if "@pytest.fixture" in stripped and current_indent > 0:
                        logger.info(f"Moving @pytest.fixture from indent {current_indent} to module level (line {i + 1})")
                        # De-indent this decorator and all following decorators until the function
                        for k in range(i, j):
                            if lines[k].strip():
                                result.append(lines[k].lstrip())
                        # Also de-indent the function definition
                        result.append(next_line.lstrip())
                        i = j + 1
                        continue

                elif not next_stripped.startswith(("def ", "async def ")):
                    # Decorator not followed by a function - orphaned!
                    logger.info(f"Removing orphaned decorator line {i + 1}: {stripped} (not followed by function)")
                    i += 1
                    continue

            result.append(line)
            i += 1

        return "\n".join(result)

    def _normalize_file_indentation(self, content: str) -> str:
        """
        Normalize indentation across the entire file after orphaned content removal.

        This ensures that decorators, functions, and classes have proper indentation
        relative to their context (module-level, class-level, nested, etc.).
        """
        lines = content.split("\n")
        result = []
        expected_indent = 0  # Current expected indentation level
        in_class = False
        class_indent = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                result.append(line)
                continue

            current_indent = len(line) - len(line.lstrip())

            # Detect class definitions
            if stripped.startswith("class "):
                in_class = True
                class_indent = expected_indent
                # Classes should be at module level (indent 0) or nested
                result.append(" " * expected_indent + stripped)
                expected_indent = class_indent + 4  # Methods inside class are indented
                continue

            # Detect function/method definitions
            if stripped.startswith("def "):
                if in_class:
                    # Method inside class - should be at class_indent + 4
                    result.append(" " * expected_indent + stripped)
                else:
                    # Module-level function - should be at indent 0
                    expected_indent = 0
                    result.append(stripped)
                    in_class = False
                continue

            # Detect decorators
            if stripped.startswith("@"):
                # Decorators should match the indentation of what they decorate
                # Look ahead to see what comes next
                next_line_idx = i + 1
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1

                if next_line_idx < len(lines):
                    next_stripped = lines[next_line_idx].strip()
                    if next_stripped.startswith("def "):
                        # Decorator for a function
                        if in_class:
                            result.append(" " * expected_indent + stripped)
                        else:
                            result.append(stripped)
                        continue

                # Default: use current expected indent
                result.append(" " * expected_indent + stripped)
                continue

            # Detect end of class (outdent back to module level)
            if in_class and current_indent < class_indent + 4 and stripped.startswith(("class ", "def ", "@")):
                in_class = False
                expected_indent = 0

            # For all other lines, preserve their content but validate indentation
            result.append(line)

        return "\n".join(result)
