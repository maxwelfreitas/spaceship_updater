#!/usr/bin/env python3
"""
Script para atualizar registros DNS IPv6 na Spaceship
Atualiza automaticamente o registro AAAA com o IPv6 público do servidor
"""

import os
import sys
import socket
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Any
import json


def load_dotenv(dotenv_path: str = '.env.spaceship') -> None:
    """
    Loads environment variables from a .env.spaceship file into os.environ if not already set.
    """
    if not os.path.exists(dotenv_path):
        return
    with open(dotenv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key not in os.environ:
                os.environ[key] = value


def get_hostname() -> str:
    """
    Gets the server's hostname
    
    Returns:
        str: Hostname of the server
    """
    hostname = socket.gethostname()
    print(f"Server hostname: {hostname}")
    return hostname


def get_public_ipv6() -> Optional[str]:
    """
    Gets the server's public IPv6 address
    
    Returns:
        str: Public IPv6 address or None on error
    """
    try:
        with urllib.request.urlopen('https://api6.ipify.org', timeout=10) as response:
            ipv6 = response.read().decode('utf-8').strip()
            print(f"Public IPv6 obtained: {ipv6}")
            return ipv6
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error getting public IPv6: {e}")
        return None


def get_env_variables() -> Dict[str, str]:
    """
    Gets and validates required environment variables
    
    Returns:
        dict: Dictionary with SPACESHIP_DOMAIN, SPACESHIP_API_KEY, and SPACESHIP_SECRET
    
    Raises:
        SystemExit: If any environment variable is missing
    """
    domain = os.getenv('SPACESHIP_DOMAIN')
    api_key = os.getenv('SPACESHIP_API_KEY')
    secret = os.getenv('SPACESHIP_SECRET')
    
    if not all([domain, api_key, secret]):
        print("Error: The following environment variables are required:")
        print("  - SPACESHIP_DOMAIN")
        print("  - SPACESHIP_API_KEY")
        print("  - SPACESHIP_SECRET")
        sys.exit(1)
    
    return {
        'domain': domain,
        'api_key': api_key,
        'secret': secret
    }


def get_dns_records(domain: str, api_key: str, secret: str) -> Optional[List[Dict[str, Any]]]:
    """
    Gets the current DNS records from Spaceship
    
    Args:
        domain: Domain name
        api_key: API key
        secret: API secret
    
    Returns:
        list: List of DNS records or None on error
    """
    url = f"https://spaceship.dev/api/v1/dns/records/{domain}?take=100&skip=0"
    
    headers = {
        'X-API-Key': api_key,
        'X-API-Secret': secret
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"DNS records successfully obtained")
            return data.get('items', []) if isinstance(data, dict) else data
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error getting DNS records: {e}")
        if hasattr(e, 'read'):
            try:
                print(f"Response: {e.read().decode('utf-8')}")
            except:
                pass
        return None


def find_aaaa_record(records: List[Dict[str, Any]], hostname: str) -> Optional[Dict[str, Any]]:
    """
    Finds the existing AAAA (IPv6) record for the hostname
    
    Args:
        records: List of DNS records
        hostname: Server hostname
    
    Returns:
        dict: Found AAAA record or None
    """
    for record in records:
        if record.get('type') == 'AAAA' and record.get('name') == hostname:
            print(f"Existing AAAA record found: {record}")
            return record
    
    print(f"No AAAA record found for {hostname}")
    return None


def needs_update(current_record: Optional[Dict[str, Any]], new_ipv6: str) -> bool:
    """
    Checks if the DNS record needs to be updated
    
    Args:
        current_record: Current DNS record or None if it doesn't exist
        new_ipv6: New IPv6 address
    
    Returns:
        bool: True if update is needed, False otherwise
    """
    if current_record is None:
        print("Record does not exist, will be created")
        return True
    
    current_ip = current_record.get('address', '')
    if current_ip != new_ipv6:
        print(f"IPv6 changed from {current_ip} to {new_ipv6}, will update")
        return True
    
    print("IPv6 is up to date, no action needed")
    return False


def update_dns_record(domain: str, api_key: str, secret: str, 
                      ipv6: str, hostname: str, existing_record: Optional[Dict[str, Any]]) -> bool:
    """
    Updates or creates a AAAA DNS record in Spaceship
    
    Args:
        domain: Domain name
        api_key: API key
        secret: API secret
        ipv6: IPv6 address to set
        hostname: Server hostname
        existing_record: Existing record or None to create new
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    url = f"https://spaceship.dev/api/v1/dns/records/{domain}"
    
    headers = {
        'X-API-Key': api_key,
        'X-API-Secret': secret,
        'Content-Type': 'application/json'
    }
    
    # Prepare the record payload
    record = {
        'address': ipv6,
        'type': 'AAAA',
        'name': hostname,
        'ttl': 1800
    }
    
    # If record exists, include its ID for update
    if existing_record:
        record['id'] = existing_record.get('id')
    
    payload = {
        'force': True,
        'items': [record]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='PUT')
        with urllib.request.urlopen(req, timeout=10) as response:
            action = "updated" if existing_record else "created"
            print(f"DNS record {action} successfully!")
            return True
        
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error updating DNS record: {e}")
        if hasattr(e, 'read'):
            try:
                print(f"Response: {e.read().decode('utf-8')}")
            except:
                pass
        return False


def main():
    """
    Main function that orchestrates the DNS update process
    """
    print("=" * 60)
    print("Starting IPv6 DNS record update")
    print("=" * 60)
    
    # 1. Get environment variables
    env_vars = get_env_variables()
    domain = env_vars['domain']
    api_key = env_vars['api_key']
    secret = env_vars['secret']
    
    print(f"\nDomain: {domain}")
    
    # 2. Get server hostname
    print("\n--- Getting server hostname ---")
    hostname = get_hostname()
    
    # 3. Get public IPv6
    print("\n--- Getting public IPv6 ---")
    public_ipv6 = get_public_ipv6()
    if not public_ipv6:
        print("Error: Could not get public IPv6")
        sys.exit(1)
    
    # 4. Get current DNS records
    print("\n--- Querying DNS records ---")
    records = get_dns_records(domain, api_key, secret)
    if records is None:
        print("Error: Could not get DNS records")
        sys.exit(1)
    
    # 5. Check existing AAAA record
    print("\n--- Checking AAAA record ---")
    aaaa_record = find_aaaa_record(records, hostname)
    
    # 6. Check if update is needed
    print("\n--- Checking if update is needed ---")
    if not needs_update(aaaa_record, public_ipv6):
        print("\n" + "=" * 60)
        print("No update needed. Process finished.")
        print("=" * 60)
        return
    
    # 7. Update or create record
    print("\n--- Updating DNS record ---")
    success = update_dns_record(domain, api_key, secret, public_ipv6, hostname, aaaa_record)
    
    if success:
        print("\n" + "=" * 60)
        print("Process finished successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Error updating DNS record")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    # Load .env.spaceship before anything else
    load_dotenv()
    main()
