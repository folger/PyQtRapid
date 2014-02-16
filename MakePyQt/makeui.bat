@echo off

for /R . %%x in (*.ui) do (
  pyuic4 %%x -o ui_%%~nx.py
)