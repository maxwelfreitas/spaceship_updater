# Spaceship DNS IPv6 Updater

Python script to automatically update IPv6 (AAAA) DNS records on the Spaceship platform.

## Features

- Gets the local server's hostname
- Gets the server's public IPv6 via https://api6.ipify.org
- Queries current DNS records via Spaceship API (GET)
- Compares the current IPv6 with the DNS record
- Updates or creates the AAAA record (hostname@domain) if needed via API (PUT)
- Modular code divided into specific functions

## Requirements

- Python 3.6 or higher (standard libraries only)
- Internet access (IPv6)
- Spaceship API credentials

## Installation

1. **From GitHub**:
   You can clone and install this project directly from GitHub:

   ```bash
   git clone https://github.com/maxwelfreitas/spaceship-dns-ipv6-updater.git
   cd spaceship-dns-ipv6-updater
   cp .env.example .env.spaceship
   # Edit the .env.spaceship file with your Spaceship credentials
   ```

2. **From source**:
   Set up the environment variables:
   ```bash
   cp .env.example .env.spaceship
   # Edit the .env.spaceship file with your credentials
   ```

## Configuration

Set the following environment variables:

- `SPACESHIP_DOMAIN`: Your domain (e.g., example.com)
- `SPACESHIP_API_KEY`: Your Spaceship API key
- `SPACESHIP_SECRET`: Your Spaceship API secret

### Configuration options:

**Option 1: .env.spaceship file** (recommended)
```bash
export $(cat .env.spaceship | xargs)
```

**Option 2: Direct environment variables**
```bash
export SPACESHIP_DOMAIN="yourdomain.com"
export SPACESHIP_API_KEY="your_api_key"
export SPACESHIP_SECRET="your_secret"
```

## Usage

Run the script:
```bash
python updater.py
```

Or make it executable:
```bash
chmod +x updater.py
./updater.py
```

## Code Structure

The program is divided into the following functions:

- `get_hostname()`: Gets the server's hostname
- `get_public_ipv6()`: Gets the server's public IPv6
- `get_env_variables()`: Validates and returns environment variables
- `get_dns_records()`: Queries DNS records via API (GET)
- `find_aaaa_record()`: Finds the existing IPv6 record for the hostname
- `needs_update()`: Checks if an update is needed
- `update_dns_record()`: Updates or creates the DNS record (PUT)
- `main()`: Orchestrates the whole process

## Scheduling (Optional)

To run automatically, add to crontab:

```bash
# Run every hour
0 * * * * cd /path/to/spaceship_updater && /usr/bin/python3 updater.py >> /var/log/dns-updater.log 2>&1
```

## Example Output

```
============================================================
Starting IPv6 DNS record update
============================================================

Domain: example.com

--- Getting server hostname ---
Server hostname: myserver

--- Getting public IPv6 ---
Public IPv6 obtained: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

--- Querying DNS records ---
DNS records successfully obtained

--- Checking AAAA record ---
Existing AAAA record found: 2001:0db8:85a3:0000:0000:8a2e:0370:1234

--- Checking if update is needed ---
IPv6 changed from 2001:0db8:85a3:0000:0000:8a2e:0370:1234 to 2001:0db8:85a3:0000:0000:8a2e:0370:7334, will update

--- Updating DNS record ---
DNS record updated successfully!

============================================================
Process finished successfully!
============================================================
```

## Error Handling

The script includes error handling for:
- Failure to connect to the IPv6 API
- Missing environment variables
- Spaceship API errors
- Invalid DNS records

## API Documentation

- [Spaceship DNS Records API](https://docs.spaceship.dev/#tag/DNS-records/operation/saveRecords)
- [IPv6 Detection Service](https://www.ipify.org/)

## License

This is a free-to-use script.
