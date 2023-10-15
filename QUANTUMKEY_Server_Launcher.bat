
if exist port.txt (
	start Broadcaster.bat
	start syncVault.bat
	python serverMenu.py
) else (
	python serverInit.py
)

timeout /t 10
exit