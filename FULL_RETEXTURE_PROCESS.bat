
@echo off
echo: 
echo 1. Enter the name of the variant mesh you want to edit.
echo: 

input.txt
C:\Python27\python.exe find_connections.py < input.txt > output.txt

echo 2. Copy this data to excel, edit the third column to show new names when a new version of a variantmesh, rigid_model, or DDS should be created.
echo: 
output.txt

echo 3. Paste your completed data into this file.
echo: 
echo Paste new data here > adjusted_copies_input.txt

adjusted_copies_input.txt

C:\Python27\python.exe create_adjusted_copies.py < adjusted_copies_input.txt > adjusted_copies_output.txt

echo 4. This output shows you the name structure of the new files you should edit and add to the pack. Close this file to end the process.
echo: 

adjusted_copies_output.txt
