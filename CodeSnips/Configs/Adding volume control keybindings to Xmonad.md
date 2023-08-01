Sets mod-F6 and mod-F7 to volume down/up respectively.

Example below sets "Windows" meta key as mod key, but configure as preferred.

```haskell
myModMask            = mod4Mask

main = xmonad $ def { modMask = myModMask }
                `additionalKeys`
                [ ((myModMask, xK_F6), spawn "amixer -q sset Master 5%-")
		        , ((myModMask, xK_F7), spawn "amixer -q sset Master 5%+")
         ]
```
