# Cookiecutter patch

cookiedough provides a mneu option →File→Cookiecutter→Patch for XDG-compliance,
which permanently fixes cookiecutters´ config module to use a `~/.config` path.

 * The new config filename will be `~/.config/cookiecutter/config`.
 * It'll also move an existing cache and replay/ directories.
 * Incurs a dependency on the `appdirs` package.
 * Patch will create a `config.py.orig`, so it's easily reversible.

When used from within cookiedough, the old cookiecutter paths would be ignored
in any case. (Fixated options). This patch is meant to bring CLI usage in line
with GUI invocations.


### The prophecy of a clutter-free homedir

System tools having a config file ~/.bashrc, ~/.ssh or even ~/.firefox directly
in the homedir is perfectly fine. Special-purpose and rarely used development 
tools are not entitled to such. And it went a little out of hand lately. (I blame
git, as is custom.)

User land applications should honor the XDG spec, APPDATA or whatever MacOS uses.
And this includes CLI tools. Which is why cookiedough enforces it for cookiecutter.
