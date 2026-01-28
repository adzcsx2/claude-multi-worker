
$Host.UI.RawUI.WindowTitle = "Sending to c1"
# Focus the target tab and send text
wt.exe -w 0 focus-tab --target 0
Start-Sleep -Milliseconds 500

# Send the text character by character (workaround for WT limitation)
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("你好")
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
