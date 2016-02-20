# Audience
- Myself
- Any computer user who doesn't need an edit->copy menu item because they just press ctl-c.
- Any hacker who is fed up with how clunky and old-fashioned vim, emacs, and acme are, or who like the simplicity of notepad++ and gedit, but want them to be more focused on power users instead of first-timers.

# Supported OS
Initially for testing, just Unix. Eventually, I would like this to work on Windows so I can use this at work.

# Appearance
- Minimalistic. No visible menus, toolbars, buttons, etc (or maybe just very basic ones, like gnome3 gedit's menus). I find all of these distracting. CUA and relevant mouse context menus should remove all need for menus at the top
- Little or no text formatting: highlight code comments and strings, but not other text.
- Highlight current line. It's easier to find the caret this way.
- Prefer tiles to tabs. What good is a text window if you can't see it? When I use editors like Notepad++ I often get on overload because of all the open tabs. Sometimes tabs are useful, but for now, I'll skip them.
- A smart Command bar, hidden by default. Gives access to more complex text actions (sed/sam commands), and functions such as open, save, find/replace, etc. The bar's execute button will have a feedback label that displays the name of the action currently typed in the bar.

# Interaction
## Mouse
Interface should support assigning commands to all mouse buttons, not just 1,2,3.
### Default Bindings
(I dispense with calling them 1,2,3 etc. because that means different things to different mouse users)
| Button | Action | Description |
| ------ | ------ | ----------- |
| Primary | Shotgun Select | most of the time, we work with _whole_ words, not _partial_ words. So by default, selecting text with the mouse selects whole words (also, this is the standard on touch interfaces nowadays. might as well be consistent between mouse and touch). Click once to place the caret to the right of the nearest word (configurable regex). Click twice to select the nearest word. Click and drag to begin selecting text, incrementing by whole words. |
| Secondary | Action Menu | Gesture-based menu appears directly under mouse with options such as paste, find, move, and other custom actions. |
| Middle | Scrolling | Scroll wheel scrolls one line at a time. Click and drag to smoothly scroll |
| Thumb | Sniper Select | precision selecting is still useful, but less used than whole word selecting. This works like traditional mouse selecting: click once to place caret to the right of nearest character. Click and drag to begin selecting text, incrementing by whole words. |

Other notes on selections:
- No dragging a selection to move it. This is always so confusing and inaccurate. Better to **move** the text by clicking where you want the text to go and selecting "move" from the action menu.
- In addition to the selection modes described above, it is useful to change a selection after you have released the mouse button (this is also standard on touch interfaces nowadays). So the selection will have a "handle" at each end that will allow the user to increase/decrease the selection by clicking and dragging it. Depending on the selection mode (sniper|shotgun), the selection will change by either characters or whole words.
- It may also be useful to use ctl-click or shift-click to change the selection, since these keyboard keys are readily available when you have one hand on the mouse already. But current environments have this feature, and I never use it.
- No cutting. Cutting requires you to remember what is in the copy buffer, increasing cognitive load. Better to have the selection visible and chose to **move** it to the new mouse cursor position via the action menu.
- Copying is implicit. This is the primary reason we select text, so might as well make it happen automatically. That way you don't have to interact with the keyboard (or use mouse chording like acme) when you want to move text around.

## Keyboard
Keyboards are primarily for typing. As a recovering emacs user, I understand the convenience of keyboard shortcuts, but also understand the high cognitive load required to remember them all. That being said, some keyboard shortcuts are forever burned into my brain...
- CUA shortcuts for common tasks, but no hjkl or ctl-t swap characters nonsense.
- Classic ctl-s to save. None of this "files are saved automatically" business like in zed or google docs. Maybe I'm just stuck in the past, and my attitude about this will change, but I feel like I will make less mistakes if I explicitly save my work.
