# Audience
- Myself
- Any computer user who doesn't need an edit->copy menu item because they just press ctl-c.
- Any hacker who is fed up with how clunky and old-fashioned vim, emacs, and acme are, or who like the simplicity of notepad++ and gedit, but want them to be more focused on power users instead of first-timers.

# Supported OS
Initially for testing, just Unix. Specifically, a Unix system with Gtk. Eventually, I would like this to work on Windows so I can use this at work.

# Appearance
- Minimalistic. No visible menus, toolbars, buttons, etc. I find all of these distracting. CUA and relevant mouse context menus should remove all need for menus at the top
- Little or no text formatting: highlight code comments and strings, but not other text.
- Highlight current line. It's easier to find the caret this way.
- Prefer tiles to tabs. What good is a text window if you can't see it? When I use editors like Notepad++ I often get on overload because of all the open tabs. Sometimes tabs are useful, but for now, I'll skip them.

# Interaction
- Primarily mouse-based. Gesture-based menus provide access to copy/cut/paste and any custom user commands. Interface should support assigning commands to all mouse buttons, not just buttons 1,2,3.
- CUA shortcuts for common tasks, but no hjkl or ctl-t swap characters nonsense.
- A smart Command bar, hidden by default. Gives access to more complex text actions (sed/sam commands), and functions such as open, save, find/replace, etc. The bar's execute button will have a feedback label that displays the name of the action currently typed in the bar.
- Classic ctl-s to save. None of this "files are saved automatically" business like in zed or google docs. Maybe I'm just stuck in the past, and my attitude about this will change, but I feel like I will make less mistakes if I explicitly save my work.
