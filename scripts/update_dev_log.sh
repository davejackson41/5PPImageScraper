#!/bin/bash

# Automated script to append log entries to logs/dev_log.txt

LOG_FILE="logs/dev_log.txt"

# Prompt user for log entry
echo "Enter log message:"
read log_msg

# Ensure a message is provided
if [ -z "$log_msg" ]; then
    echo "❌ Error: Log message cannot be empty!"
    exit 1
fi

# Append the log message with timestamp
# Store the new log entry in a variable
new_entry="## [$(date +"%Y-%m-%d %H:%M:%S")] $log_msg"

# Insert the new entry at the beginning of the file
echo -e "$new_entry\n$(cat $LOG_FILE)" > $LOG_FILE

echo "✅ Log entry added successfully!"
