Simple scripts that is meant to help when making Wi-Fi related stuff.

Motivation: Help during attack like evil-twins and the such when needing to generate configuration for multiple AP either for relay or not. The work can be tedious and mostly a copy-paste of some basic configuration with only a few changes. In general, I want to be able to skip those config generation and potentially plug this project into other workflow.

I want, detection, connection, and generation of some files.
When doing auditing, some tools will auto generate config and do the full attack by themselves. I do not think such things are always appropriate as they might miss a few things during an attack. For exampe, if you want to do a PEAP Relay attack, this project will help you with the configs needed, but YOU will need to pull the trigger yourself

I will also try and implement tools to detect if an attack against a target is viable like a WPA3 downgrade.

This project will both hold template for copy-paste and simple generators to fill all required fields.



This is a really early script and I plan to add more customization and simple "hand-holding" for each case.
Will slowly be adding as I make my own tools for some certs.
