# Lantern Courier: a fictional first slice

Player goal: deliver one lantern through a three-room ruin before its flame fades. Each room offers a short risky route or a long safe route. Moving consumes flame; stopping at a sheltered alcove restores a limited amount. The repeated choice is whether to spend light for speed. Visible flame, route markers and immediate room feedback communicate consequences.

Prototype question: can a new player predict the route tradeoff and complete or fail one run without developer help? One keyboard device, one character, three rooms, a flame meter, success/failure screens and restart are enough. Cut inventory, procedural levels, shops, multiplayer and save progression. Temporary geometric art is sufficient to test choice readability.

States: title -> room -> route chosen -> movement -> feedback -> next room or failure -> result -> restart. A fixed seed keeps the first test comparable. Log build ID, route choices, flame at each choice, completion/failure and one observed misunderstanding. Do not infer confusion from a timeout alone; unclear feedback is the strongest alternative to a weak mechanic.

First acceptance pass: every screen responds to keyboard, the meter remains legible at the target viewport, both routes can be selected, flame exhaustion fails clearly, delivery succeeds and restart resets all state. Then observe one fresh player and revise one confirmed issue. This is a method example; no runtime/build, player observation or shipped result is claimed.
