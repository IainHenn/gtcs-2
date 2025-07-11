$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

Start-Process $chromePath -ArgumentList '--remote-debugging-port=9222 --user-data-dir="C:\chrome-profile-1"'
Start-Process $chromePath -ArgumentList '--remote-debugging-port=9223 --user-data-dir="C:\chrome-profile-2"'
Start-Process $chromePath -ArgumentList '--remote-debugging-port=9224 --user-data-dir="C:\chrome-profile-3"'
Start-Process $chromePath -ArgumentList '--remote-debugging-port=9225 --user-data-dir="C:\chrome-profile-4"'
Start-Process $chromePath -ArgumentList '--remote-debugging-port=9226 --user-data-dir="C:\chrome-profile-5"'
