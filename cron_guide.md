# Using Cron on macOS

This guide explains how to set up automated tasks using cron on macOS, specifically for running the YouTube Comment Bot on a schedule.

## What is Cron?

Cron is a time-based job scheduler in Unix-like operating systems (including macOS). It allows you to schedule commands or scripts to run automatically at specified times or intervals.

## Accessing Crontab

On macOS, you can manage your cron jobs using the `crontab` command:

1. Open Terminal (Applications > Utilities > Terminal)
2. To view your current cron jobs:
   ```bash
   crontab -l
   ```
3. To edit your cron jobs:
   ```bash
   crontab -e
   ```
   This will open the crontab file in your default text editor (usually vim or nano).

## Crontab Syntax

A crontab entry has the following format:
```
* * * * * command_to_run
```

The five asterisks represent:
1. Minute (0-59)
2. Hour (0-23)
3. Day of month (1-31)
4. Month (1-12)
5. Day of week (0-7, where both 0 and 7 represent Sunday)

### Examples:

- Run every day at 3:30 PM:
  ```
  30 15 * * * /path/to/script.sh
  ```

- Run every Monday at 9:00 AM:
  ```
  0 9 * * 1 /path/to/script.sh
  ```

- Run every weekday (Monday to Friday) at 8:00 PM:
  ```
  0 20 * * 1-5 /path/to/script.sh
  ```

## Setting Up Cron for YouTube Comment Bot

To run the YouTube Comment Bot on a schedule:

1. Determine the absolute path to your script:
   ```bash
   cd /path/to/youtube_comment_bot
   pwd
   ```
   This will show you the full path to use in your crontab.

2. Edit your crontab:
   ```bash
   crontab -e
   ```

3. Add an entry like this (adjust the time as needed):
   ```
   # Run YouTube Comment Bot weekdays at 3:30 PM
   30 15 * * 1-5 /absolute/path/to/youtube_comment_bot/run_comment_bot.sh >> /absolute/path/to/youtube_comment_bot/logs/cron_output.log 2>&1
   ```

4. Save and exit the editor:
   - For vim: Press `Esc`, then type `:wq` and press `Enter`
   - For nano: Press `Ctrl+X`, then `Y` to confirm, then `Enter`

## Troubleshooting

- **Cron not running**: Make sure your Mac doesn't go to sleep at the scheduled time.
- **Permission issues**: Ensure your script has execute permissions:
  ```bash
  chmod +x /path/to/run_comment_bot.sh
  ```
- **Path problems**: Use absolute paths in your crontab entries, not relative paths.
- **Check logs**: Always redirect output to a log file (as shown above) to help with debugging.

## Additional Resources

- Use [Cronitor](https://crontab.guru/) to help build and understand cron expressions.
- Check system logs if jobs aren't running: `log show --predicate 'eventMessage contains "cron"' --last 1h`
