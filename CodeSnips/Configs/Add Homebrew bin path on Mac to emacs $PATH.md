Homebrew likes to install things in `/usr/local/bin` so if you want to call commands from Emacs add the following to `$HOME/.emacs.d/init.el`:

```elisp
(setenv "PATH" (concat "/usr/local/bin:" (getenv "PATH")))
```
