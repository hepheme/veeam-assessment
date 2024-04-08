Basic usage
-----------

Running the script is as simple as:

    python3 veeam.py [-h] [--interval INTERVAL] source_folder replica_folder log_file

Example using custom folders with 60 seconds interval refresh:

    python3 veeam.py --interval 60 .\source .\replica .\logs\log
