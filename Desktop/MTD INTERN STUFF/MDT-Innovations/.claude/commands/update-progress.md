Update progress.md by reviewing recent changes to the codebase.

1. Run `git diff HEAD~1 HEAD --name-only` to see which files changed in the last commit, or `git diff --name-only` for unstaged changes.
2. For each changed file, read it to understand what the code does.
3. Read the existing progress.md at the project root (if it exists).
4. Append a summary entry to progress.md for each changed file:

## [YYYY-MM-DD] <filename>
**Changed:** <brief description of what changed>
**Purpose:** <what the code does / why it matters>

If no specific files are mentioned by the user, summarize all recently modified files since the last progress.md update. Keep entries concise and focused on intent, not line-by-line details.
