# B210-Assignment_6
## a. What is the purpose of this program(s)?
The purpose of this program is to create a song class, complete with an initialization function, using the data in the taylor_discography.csv file to create song objects for each sample.
## b. What does the program do, including what it takes for input, and what it gives as output?
The program defines a Song class whose attributes come from the CSV header, implements a minimal, no-module CSV parser that handles quoted fields and doubled quotes and strips a UTF‑8 BOM, converts numeric-looking fields to int/float where reasonable, loads every CSV row into a Song instance and stores them in a list songs and prints the detected header fields, then launches an interactive paginated viewer (you can set page size, press Enter to continue, or type q to quit). 
The input is the CSV file at taylor_discography.csv (one row per track; header row required). The output (console) is a line reporting how many songs were loaded and the detected fields, and an interactive, paginated list of songs showing index, title (if present), track_id, and duration_ms.
## c. How do you use the program?
1. Create the .py file (copy & paste)
  Open VS Code, or any text editor.
  Please copy the entire Python script (the contents you pasted earlier) and paste it into the editor.
  Save the file as: C:\Users\jinas\Downloads\Assignment_6_User-Defined_Functions.py
  (Make sure the file extension is .py — not .txt.)
2. Verify the CSV is present
  Confirm the CSV is at: taylor_discography.csv
  Quick PowerShell check (copy/paste into PowerShell): Get-Item "C:\Users\jinas\Downloads\taylor_discography.csv" | Select-Object FullName,Length,LastWriteTime
  If that prints nothing, move the CSV to that path or update the script's csv_path variable to the actual path.
3. Run the script (exact command to paste into PowerShell)
  python 'C:\Users\jinas\Downloads\Assignment_6_User-Defined_Functions.py'
4. At the start, the program prints:
    Loading songs from: taylor_discography.csv
    Loaded N songs.
    Detected fields: [...]
  It then starts the interactive pager showing PAGE_SIZE songs per page.
    Pager controls (type at the pager prompt):
    Press Enter → show next page
  Type q then Enter → quit program
  To change how many songs are shown per page, edit the script and set: PAGE_SIZE = 24   # (change 24 to the number you want)
5. Then save and run again.
