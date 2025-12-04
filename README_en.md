# Spaceship DNS IPv6 Updater

Python script to automatically update IPv6 DNS records (AAAA) on the Spaceship platform.

## Features

- Gets the local server's hostname
- Gets the server's public IPv6 via https://api6.ipify.org
- Queries current DNS records via Spaceship API (GET)
- Compares the current IPv6 with the DNS record IPv6
- Updates or creates the AAAA record (hostname@domain) if needed via API (PUT)
- Modular code divided into specific functions

## Requirements

- Python 3.6 or higher (standard libraries only)
- Internet access (IPv6)
- Spaceship API credentials

## Installation

Clone the repository from GitHub:

```bash
git clone https://github.com/maxwelfreitas/spaceship_updater.git
cd spaceship_updater
```

## Configuration

Configure the following environment variables:

- `SPACESHIP_DOMAIN`: Your domain (e.g., example.com)
- `SPACESHIP_API_KEY`: Your Spaceship API key
- `SPACESHIP_SECRET`: Your Spaceship API secret

### Configuration options:

**Option 1: .env.spaceship file** (recommended)

Create a `.env.spaceship` file in the project directory:

```bash
SPACESHIP_DOMAIN=yourdomain.com
SPACESHIP_API_KEY=your_api_key
SPACESHIP_SECRET=your_secret
```

The script will automatically load these variables when executed.

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

- `load_dotenv()`: Loads environment variables from .env.spaceship file
- `get_hostname()`: Gets the server's hostname
- `get_public_ipv6()`: Gets the server's public IPv6
- `get_env_variables()`: Validates and returns environment variables
- `get_dns_records()`: Queries DNS records via API (GET)
- `find_aaaa_record()`: Locates the existing IPv6 record for the hostname
- `needs_update()`: Checks if an update is needed
- `update_dns_record()`: Updates or creates the DNS record (PUT)
- `main()`: Orchestrates the entire process

## Scheduling (Optional)

To run automatically, add to crontab:

```bash
# Run every hour
0 * * * * cd /path/to/spaceship_updater && /usr/bin/python3 updater.py >> /var/log/dns-updater.log 2>&1
```

## Output Example

```
2025-12-04 10:00:00 Starting IPv6 DNS record update
2025-12-04 10:00:00 Domain: example.com
2025-12-04 10:00:00 Getting server hostname
2025-12-04 10:00:00 Server hostname: myserver
2025-12-04 10:00:00 Getting public IPv6 address
2025-12-04 10:00:00 Public IPv6 obtained: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
2025-12-04 10:00:00 Querying DNS records
2025-12-04 10:00:00 DNS records successfully obtained
2025-12-04 10:00:00 Checking AAAA record
2025-12-04 10:00:00 Existing AAAA record found: {'id': '123', 'type': 'AAAA', 'name': 'myserver', 'address': '2001:0db8:85a3:0000:0000:8a2e:0370:1234'}
2025-12-04 10:00:00 Checking if update is needed
2025-12-04 10:00:00 IPv6 changed from 2001:0db8:85a3:0000:0000:8a2e:0370:1234 to 2001:0db8:85a3:0000:0000:8a2e:0370:7334, will update
2025-12-04 10:00:00 Updating DNS record
2025-12-04 10:00:00 DNS record updated successfully!
2025-12-04 10:00:00 Process finished successfully!
```

## Error Handling

The script includes error handling for:
- Connection failure with the IPv6 API
- Missing environment variables
- Spaceship API errors
- Invalid DNS records

## API Documentation

- [Spaceship DNS Records API](https://docs.spaceship.dev/#tag/DNS-records/operation/saveRecords)
- [IPv6 Detection Service](https://www.ipify.org/)

## License

This is a free-to-use script.
