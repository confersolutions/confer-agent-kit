#!/usr/bin/env python3
"""
Confer Agent Kit Secrets Parser
Classifies, normalizes, and organizes raw secrets/notes dump.
"""

import re
import json
import csv
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Mask function: show first 4 and last 2 chars
def mask_secret(value: str, min_length: int = 6) -> str:
    """Mask a secret value, showing only first 4 and last 2 chars."""
    if not value or len(value) < min_length:
        return "****"
    if len(value) <= 6:
        return value[:2] + "****"
    return value[:4] + "…" * max(1, (len(value) - 6) // 4) + value[-2:]

def hash_value(value: str) -> str:
    """Generate SHA256 hash for deduplication."""
    return hashlib.sha256(value.encode()).hexdigest()[:16]

class SecretsParser:
    def __init__(self, output_base: str = "secrets"):
        self.output_base = Path(output_base)
        self.output_base.mkdir(exist_ok=True)
        self.intake_dir = self.output_base / "_intake"
        self.intake_dir.mkdir(exist_ok=True)
        self.global_dir = self.output_base / "global"
        self.global_dir.mkdir(exist_ok=True)
        self.ssh_dir = self.global_dir / "ssh"
        self.ssh_dir.mkdir(exist_ok=True)
        self.services_dir = self.output_base / "services"
        self.services_dir.mkdir(exist_ok=True)
        
        self.parsed_data = {
            "api_keys": [],
            "credentials": [],
            "tokens": [],
            "db_uris": [],
            "ssh": [],
            "env_vars": [],
            "endpoints": [],
            "unknown": []
        }
        self.value_hashes = {}  # For deduplication: hash -> best entry
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    def _parse_tab_separated_tables(self, lines: List[str]):
        """Parse tab-separated credential tables (Role/Username/Password or Email/Password format)."""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for table headers
            if re.search(r'(Role|Username|Password|Email\s+Address)', line, re.IGNORECASE):
                # Check if this looks like a table header
                parts = re.split(r'\t+|\s{2,}', line)  # Tab or multiple spaces
                has_role_or_username = any('role' in p.lower() or 'username' in p.lower() for p in parts)
                has_password = any('password' in p.lower() for p in parts)
                has_email = any('email' in p.lower() for p in parts)
                
                if (has_role_or_username or has_email) and has_password:
                    # Skip header line
                    i += 1
                    # Parse data rows
                    while i < len(lines):
                        data_line = lines[i].strip()
                        if not data_line or data_line.startswith('#') or re.search(r'^[☐✅]', data_line):
                            i += 1
                            continue
                        
                        # Split by tab or multiple spaces
                        parts = re.split(r'\t+|\s{2,}', data_line)
                        if len(parts) >= 3:
                            if has_email:
                                # Email format: email | service flags | password
                                email = parts[0].strip()
                                password_idx = len(parts) - 1  # Password usually last
                                password = parts[password_idx].strip()
                                
                                if '@' in email and password and password not in ['☐', '✅']:
                                    service = self._guess_service_from_email(email)
                                    self._add_credential(email, password, service, data_line, i+1)
                            else:
                                # Role/Username/Password format
                                if len(parts) >= 3:
                                    role = parts[0].strip() if len(parts) > 0 else ""
                                    username = parts[1].strip() if len(parts) > 1 else ""
                                    password = parts[2].strip() if len(parts) > 2 else ""
                                    
                                    if username and password and password not in ['☐', '✅']:
                                        service = self._guess_service_from_context([data_line])
                                        self._add_credential(username, password, service, data_line, i+1)
                        elif len(parts) == 2 and '@' in parts[0]:
                            # Email/password pair without extra columns
                            email = parts[0].strip()
                            password = parts[1].strip()
                            if password and password not in ['☐', '✅']:
                                service = self._guess_service_from_email(email)
                                self._add_credential(email, password, service, data_line, i+1)
                        else:
                            break
                        i += 1
                    continue
            
            # Also check for email:password pattern
            email_pass_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s+.*?([A-Za-z0-9@#$%^&*!]{8,})', line)
            if email_pass_match:
                email = email_pass_match.group(1)
                password = email_pass_match.group(2)
                if password and password not in ['☐', '✅']:
                    service = self._guess_service_from_email(email)
                    self._add_credential(email, password, service, line, i+1)
            
            # Service-specific password patterns
            service_pass_patterns = [
                (r'SSH\s*Password[:=]\s*([^\s]+)', 'ssh', ''),
                (r'Coolify\s+Password[:=]\s*([^\s]+)', 'coolify', ''),
                (r'Coolify\s+Account[:=]\s*([^\s]+)', 'coolify', ''),
                (r'Contabo\s+Account\s+Password[:=]\s*([^\s]+)', 'contabo', ''),
                (r'Contabo\s+Account[:=]\s*([^\s]+)', 'contabo', ''),
                (r'n8n.*Password[:=]\s*([^\s]+)', 'n8n', ''),
                (r'CLOUDFLARE\s+password[:=]\s*([^\s]+)', 'cloudflare', ''),
                (r'Snap\s+Shooter\s+Password[:=]\s*([^\s]+)', 'snapshot', ''),
                (r'SERVICE_PASSWORD_(\w+)[:=]\s*([^\s]+)', None, None),  # Generic service password env vars
            ]
            
            for pattern, service, username in service_pass_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if pattern.startswith('SERVICE_PASSWORD_'):
                        service_name = match.group(1).lower()
                        value = match.group(2)
                        # Check if it's an API key pattern
                        if 'APIKEY' in match.group(1):
                            self._add_api_key(value, service_name.replace('apikey', ''), f'{service_name.upper()}_API_KEY', line, i+1)
                        else:
                            self._add_credential('', value, service_name, line, i+1)
                    else:
                        password = match.group(1)
                        # Check if username is on the same or previous line
                        username_val = username
                        if not username_val and i > 0:
                            # Check previous line for email/username
                            prev_line = lines[i-1].strip()
                            email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', prev_line)
                            if email_match:
                                username_val = email_match.group(1)
                            else:
                                user_match = re.search(r'(?:Account|Username|User)[:=]\s*([^\s]+)', prev_line, re.IGNORECASE)
                                if user_match:
                                    username_val = user_match.group(1)
                        
                        self._add_credential(username_val, password, service or 'unknown', line, i+1)
                    break
            
            i += 1
    
    def _guess_service_from_email(self, email: str) -> str:
        """Guess service from email address."""
        email_lower = email.lower()
        if 'dev' in email_lower or 'dev01' in email_lower or 'dev02' in email_lower:
            return 'development'
        elif 'employee' in email_lower:
            return 'internal'
        elif 'admin' in email_lower:
            return 'admin'
        elif 'confersolutions' in email_lower or 'confer' in email_lower:
            return 'confer'
        return 'unknown'
        
    def parse_raw_text(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw text dump into structured data."""
        lines = raw_text.split('\n')
        
        # First, detect and parse tab-separated credential tables
        self._parse_tab_separated_tables(lines)
        
        # Patterns
        api_key_patterns = [
            (r'OPENAI[_-]?KEY[:=]\s*([^\s]+)', 'openai', 'OPENAI_API_KEY'),
            (r'sk-[A-Za-z0-9]{20,}', 'openai', 'OPENAI_API_KEY'),
            (r'ghp_[A-Za-z0-9]{36,}', 'github', 'GITHUB_TOKEN'),
            (r'AIza[0-9A-Za-z_-]{35,}', 'google', 'GOOGLE_API_KEY'),
            (r'xox[baprs]-[A-Za-z0-9-]+', 'slack', 'SLACK_TOKEN'),
            (r'Bearer\s+([\w\.-]+)', None, None),  # Generic bearer
            (r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', None, 'JWT_TOKEN'),  # JWT
        ]
        
        username_pattern = r'(?:user(?:name)?|login|account)[:=]\s*([^\s]+)'
        password_pattern = r'pass(?:word|wd)?[:=]\s*([^\s]+)'
        
        db_uri_pattern = r'(postgres|mysql|mongodb|redis|amqp|neo4j|qdrant)(\+s)?://([^\s]+)'
        
        ssh_key_pattern = r'-----BEGIN\s+(OPENSSH|RSA|EC|DSA)\s+(PUBLIC|PRIVATE)\s+KEY-----'
        ssh_key_block_pattern = r'-----BEGIN.*?KEY-----\s*(.*?)\s*-----END.*?KEY-----'
        
        env_var_pattern = r'([A-Z][A-Z0-9_]+)[:=]\s*([^\s]+)'
        
        endpoint_pattern = r'(https?://[^\s]+|[a-z0-9.-]+\.(com|net|org|io|dev|app|cloud)[^\s]*)'
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith('#'):
                i += 1
                continue
                
            # API Keys / Tokens
            for pattern, service, key_name in api_key_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1) if match.groups() else match.group(0)
                    self._add_api_key(value, service, key_name, line, i+1)
                    break
            
            # Username/Password pairs
            user_match = re.search(username_pattern, line, re.IGNORECASE)
            pass_match = re.search(password_pattern, line, re.IGNORECASE)
            if user_match or pass_match:
                username = user_match.group(1) if user_match else None
                password = pass_match.group(1) if pass_match else None
                
                # Check next line if password not found
                if username and not password and i + 1 < len(lines):
                    next_match = re.search(password_pattern, lines[i+1], re.IGNORECASE)
                    if next_match:
                        password = next_match.group(1)
                
                if username or password:
                    service = self._guess_service_from_context(lines[max(0, i-2):i+3])
                    self._add_credential(username, password, service, line, i+1)
                    if password:
                        i += 1  # Skip next line if we consumed it
                    break
            
            # DB URIs
            db_match = re.search(db_uri_pattern, line, re.IGNORECASE)
            if db_match:
                db_type = db_match.group(1).lower()
                uri = db_match.group(3)
                service = db_type  # postgres -> postgres
                self._add_db_uri(uri, service, line, i+1)
            
            # SSH Keys
            if re.search(ssh_key_pattern, line, re.IGNORECASE):
                key_type = re.search(r'(PUBLIC|PRIVATE)', line, re.IGNORECASE)
                key_block = self._extract_ssh_key_block(lines[i:i+50])  # Look ahead
                if key_block:
                    self._add_ssh_key(key_block, key_type.group(1) if key_type else 'UNKNOWN', line, i+1)
                    # Skip lines in the key block
                    i += len(key_block.split('\n')) - 1
            
            # Env vars
            env_match = re.search(env_var_pattern, line)
            if env_match and not any(p in line.lower() for p in ['password', 'secret', 'key', 'token']):
                key = env_match.group(1)
                value = env_match.group(2)
                # Skip if already classified as API key
                if not any(k['value_masked'] == mask_secret(value) for k in self.parsed_data['api_keys']):
                    service = self._guess_service_from_key(key)
                    scope = 'service' if service else 'global'
                    self._add_env_var(key, value, service, scope, line, i+1)
            
            # Traefik basic auth (bcrypt hashes)
            traefik_match = re.search(r'traefik[^=]*basicauth[^=]*=(.+)', line, re.IGNORECASE)
            if traefik_match:
                # Parse username:hash pairs - split on commas outside of bcrypt hashes
                users_str = traefik_match.group(1).strip()
                # Split on comma followed by word (username:) pattern
                users = re.split(r',(?=\w+:)', users_str)
                
                for user_pair in users:
                    user_pair = user_pair.strip()
                    if ':' in user_pair and '$2' in user_pair:
                        parts = user_pair.split(':', 1)
                        if len(parts) == 2:
                            username = parts[0].strip()
                            bcrypt_hash = parts[1].strip()
                            # Store bcrypt hash as a token (can't reverse it)
                            self._add_token(bcrypt_hash, 'traefik', 'bcrypt', username, line, i+1)
                i += 1
                continue
            
            # Endpoints
            endpoint_match = re.search(endpoint_pattern, line, re.IGNORECASE)
            if endpoint_match:
                url = endpoint_match.group(1)
                service = self._guess_service_from_url(url)
                self._add_endpoint(url, service, line, i+1)
            
            # Unknown
            if line and not any([
                user_match, pass_match, db_match, env_match, endpoint_match,
                re.search(ssh_key_pattern, line, re.IGNORECASE)
            ]):
                self._add_unknown(line, i+1)
            
            i += 1
        
        return self.parsed_data
    
    def _extract_ssh_key_block(self, lines: List[str]) -> Optional[str]:
        """Extract complete SSH key block."""
        text = '\n'.join(lines)
        match = re.search(r'-----BEGIN.*?KEY-----\s*(.*?)\s*-----END.*?KEY-----', text, re.DOTALL)
        return match.group(0) if match else None
    
    def _guess_service_from_context(self, context: List[str]) -> str:
        """Guess service from surrounding context."""
        text = ' '.join(context).lower()
        services = ['openai', 'groq', 'qdrant', 'neo4j', 'vercel', 'coolify', 'github', 'replit', 'clerk', 'n8n', 'flowise', 'postgres', 'mysql', 'redis']
        for svc in services:
            if svc in text:
                return svc
        return 'unknown'
    
    def _guess_service_from_key(self, key: str) -> Optional[str]:
        """Guess service from env var key name."""
        key_lower = key.lower()
        mapping = {
            'openai': 'openai',
            'groq': 'groq',
            'qdrant': 'qdrant',
            'neo4j': 'neo4j',
            'vercel': 'vercel',
            'coolify': 'coolify',
            'github': 'github',
            'replit': 'replit',
            'clerk': 'clerk',
            'n8n': 'n8n',
            'flowise': 'flowise',
            'postgres': 'postgres',
            'mysql': 'mysql',
            'redis': 'redis',
        }
        for svc, name in mapping.items():
            if svc in key_lower:
                return name
        return None
    
    def _guess_service_from_url(self, url: str) -> str:
        """Guess service from URL."""
        url_lower = url.lower()
        mapping = {
            'openai.com': 'openai',
            'groq.com': 'groq',
            'qdrant.io': 'qdrant',
            'neo4j.com': 'neo4j',
            'vercel.com': 'vercel',
            'coolify.io': 'coolify',
            'github.com': 'github',
            'replit.com': 'replit',
            'clerk.com': 'clerk',
            'api.openai.com': 'openai',
            'api.groq.com': 'groq',
        }
        for domain, service in mapping.items():
            if domain in url_lower:
                return service
        return 'unknown'
    
    def _add_api_key(self, value: str, service: Optional[str], key_name: Optional[str], source_line: str, line_num: int):
        """Add API key with deduplication."""
        value_hash = hash_value(value)
        if value_hash in self.value_hashes:
            return  # Already seen
        
        self.value_hashes[value_hash] = value
        
        if not service:
            service = self._guess_service_from_context([source_line])
        if not key_name:
            key_name = f"{service.upper()}_API_KEY" if service != 'unknown' else "API_KEY"
        
        entry = {
            "service": service or "unknown",
            "key_name": key_name,
            "value_masked": mask_secret(value),
            "value_hash": value_hash,
            "source_line": source_line[:100],  # Truncate
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["api_keys"].append(entry)
    
    def _add_credential(self, username: Optional[str], password: Optional[str], service: str, source_line: str, line_num: int):
        """Add credential with deduplication."""
        if password:
            value_hash = hash_value(password)
            if value_hash in self.value_hashes:
                return
            self.value_hashes[value_hash] = password
        
        entry = {
            "service": service or "unknown",
            "username": username or "",
            "password_masked": mask_secret(password) if password else "",
            "url": "",
            "source_line": source_line[:100],
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["credentials"].append(entry)
    
    def _add_db_uri(self, uri: str, service: str, source_line: str, line_num: int):
        """Add DB URI with deduplication."""
        value_hash = hash_value(uri)
        if value_hash in self.value_hashes:
            return
        self.value_hashes[value_hash] = uri
        
        # Parse URI
        match = re.search(r'://([^:]+):([^@]+)@([^/]+)/(.+)', uri)
        username = match.group(1) if match else None
        host = match.group(3) if match else None
        dbname = match.group(4).split('?')[0] if match else None
        
        entry = {
            "service": service,
            "uri_masked": mask_secret(uri),
            "uri_hash": value_hash,
            "username": username or "",
            "host": host or "",
            "dbname": dbname or "",
            "source_line": source_line[:100],
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["db_uris"].append(entry)
    
    def _add_ssh_key(self, key_block: str, key_type: str, source_line: str, line_num: int):
        """Add SSH key."""
        value_hash = hash_value(key_block)
        if value_hash in self.value_hashes:
            return
        self.value_hashes[value_hash] = key_block
        
        key_type_lower = key_type.lower()
        filename = f"id_rsa_{'private' if 'PRIVATE' in key_type_lower else 'public'}.{'key' if 'PRIVATE' in key_type_lower else 'pub'}"
        
        entry = {
            "type": key_type,
            "path_written": f"global/ssh/{filename}",
            "comment": "",
            "source_line": source_line[:100],
            "line_num": line_num
        }
        self.parsed_data["ssh"].append(entry)
        
        # Write SSH key file
        ssh_path = self.ssh_dir / filename
        ssh_path.write_text(key_block)
        ssh_path.chmod(0o600)  # Secure permissions
    
    def _add_env_var(self, key: str, value: str, service: Optional[str], scope: str, source_line: str, line_num: int):
        """Add env var with deduplication."""
        value_hash = hash_value(value)
        if value_hash in self.value_hashes:
            return
        self.value_hashes[value_hash] = value
        
        entry = {
            "service": service or "",
            "name": key,
            "value_masked": mask_secret(value),
            "value_hash": value_hash,
            "scope": scope,
            "source_line": source_line[:100],
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["env_vars"].append(entry)
    
    def _add_endpoint(self, url: str, service: str, source_line: str, line_num: int):
        """Add endpoint with deduplication."""
        value_hash = hash_value(url)
        if value_hash in self.value_hashes:
            return
        self.value_hashes[value_hash] = url
        
        entry = {
            "service": service,
            "url": url,
            "source_line": source_line[:100],
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["endpoints"].append(entry)
    
    def _add_token(self, value: str, service: str, token_type: str, username: Optional[str], source_line: str, line_num: int):
        """Add token (bearer tokens, bcrypt hashes, etc.) with deduplication."""
        value_hash = hash_value(value)
        if value_hash in self.value_hashes:
            return
        self.value_hashes[value_hash] = value
        
        entry = {
            "service": service,
            "token_type": token_type,
            "value_masked": mask_secret(value),
            "value_hash": value_hash,
            "username": username or "",
            "expires_at": "",
            "source_line": source_line[:100],
            "line_num": line_num,
            "notes": ""
        }
        self.parsed_data["tokens"].append(entry)
    
    def _add_unknown(self, line: str, line_num: int):
        """Add unknown/unclassified line."""
        entry = {
            "raw_line": line[:200],  # Truncate
            "line_num": line_num,
            "guess": ""
        }
        self.parsed_data["unknown"].append(entry)
    
    def write_outputs(self, raw_text: str):
        """Write all output files."""
        # 1. Save raw intake
        raw_file = self.intake_dir / f"{self.timestamp}_raw.txt"
        raw_file.write_text(raw_text)
        
        # 2. Write parsed JSON
        json_file = self.intake_dir / f"{self.timestamp}_parsed.json"
        with open(json_file, 'w') as f:
            json.dump(self.parsed_data, f, indent=2)
        
        # 3. Write parse report (masked)
        report_file = self.intake_dir / f"{self.timestamp}_parse_report.md"
        self._write_report(report_file)
        
        # 4. Write global .env.global
        self._write_global_env()
        
        # 5. Write CSVs
        self._write_csvs()
        
        # 6. Write service-specific .env files
        self._write_service_envs()
        
        # 7. Write registry.yaml
        self._write_registry()
        
        # 8. Update README
        self._update_readme()
        
        return {
            "raw_file": str(raw_file),
            "json_file": str(json_file),
            "report_file": str(report_file)
        }
    
    def _write_report(self, file_path: Path):
        """Write human-readable parse report (masked)."""
        lines = [
            f"# Secrets Parse Report - {self.timestamp}\n",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Summary\n",
            f"- API Keys: {len(self.parsed_data['api_keys'])}",
            f"- Credentials: {len(self.parsed_data['credentials'])}",
            f"- Tokens: {len(self.parsed_data['tokens'])}",
            f"- DB URIs: {len(self.parsed_data['db_uris'])}",
            f"- SSH Keys: {len(self.parsed_data['ssh'])}",
            f"- Env Vars: {len(self.parsed_data['env_vars'])}",
            f"- Endpoints: {len(self.parsed_data['endpoints'])}",
            f"- Unknown: {len(self.parsed_data['unknown'])}\n",
        ]
        
        # Details by category
        for category, items in self.parsed_data.items():
            if items:
                lines.append(f"## {category.replace('_', ' ').title()}\n")
                for item in items[:20]:  # Limit to 20 per category
                    if category == 'api_keys':
                        lines.append(f"- {item['service']}: {item['key_name']} = {item['value_masked']}")
                    elif category == 'credentials':
                        lines.append(f"- {item['service']}: {item['username']} / {item['password_masked']}")
                    elif category == 'unknown':
                        lines.append(f"- Line {item['line_num']}: {item['raw_line'][:80]}")
                if len(items) > 20:
                    lines.append(f"\n... and {len(items) - 20} more\n")
                lines.append("")
        
        file_path.write_text('\n'.join(lines))
    
    def _write_global_env(self):
        """Append to global .env.global file."""
        env_file = self.global_dir / ".env.global"
        
        # Load existing entries to avoid duplicates
        existing_keys = set()
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key = line.split('=')[0]
                            existing_keys.add(key)
        
        # Append new entries
        with open(env_file, 'a') as f:
            # Add API keys
            for item in self.parsed_data['api_keys']:
                key_name = item['key_name']
                if key_name not in existing_keys:
                    value = self.value_hashes[item['value_hash']]
                    f.write(f"{key_name}={value}\n")
                    existing_keys.add(key_name)
            
            # Add global env vars
            for item in self.parsed_data['env_vars']:
                if item['scope'] == 'global' and item['name'] not in existing_keys:
                    value = self.value_hashes[item['value_hash']]
                    f.write(f"{item['name']}={value}\n")
                    existing_keys.add(item['name'])
    
    def _write_csvs(self):
        """Append to CSV files."""
        # Credentials - append if file exists, write header if new
        if self.parsed_data['credentials']:
            cred_file = self.global_dir / "credentials.csv"
            file_exists = cred_file.exists()
            with open(cred_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['service', 'username', 'password_masked', 'url', 'notes'])
                if not file_exists:
                    writer.writeheader()
                for item in self.parsed_data['credentials']:
                    writer.writerow({
                        'service': item['service'],
                        'username': item['username'],
                        'password_masked': item['password_masked'],
                        'url': item.get('url', ''),
                        'notes': item.get('notes', '')
                    })
        
        # Tokens - append if file exists, write header if new
        if self.parsed_data['tokens']:
            token_file = self.global_dir / "tokens.csv"
            file_exists = token_file.exists()
            with open(token_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['service', 'token_type', 'value_masked', 'expires_at', 'notes'])
                if not file_exists:
                    writer.writeheader()
                for item in self.parsed_data['tokens']:
                    writer.writerow({
                        'service': item.get('service', ''),
                        'token_type': item.get('token_type', ''),
                        'value_masked': item.get('value_masked', ''),
                        'expires_at': item.get('expires_at', ''),
                        'notes': item.get('notes', '')
                    })
        
        # Endpoints - append if file exists, write header if new
        if self.parsed_data['endpoints']:
            endpoint_file = self.global_dir / "endpoints.csv"
            file_exists = endpoint_file.exists()
            with open(endpoint_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['service', 'url', 'region', 'notes'])
                if not file_exists:
                    writer.writeheader()
                for item in self.parsed_data['endpoints']:
                    writer.writerow({
                        'service': item['service'],
                        'url': item['url'],
                        'region': '',
                        'notes': item.get('notes', '')
                    })
    
    def _write_service_envs(self):
        """Write service-specific .env.local files."""
        services = defaultdict(list)
        
        # Group env vars by service
        for item in self.parsed_data['env_vars']:
            if item['service']:
                services[item['service']].append(item)
        
        for service, items in services.items():
            service_dir = self.services_dir / service
            service_dir.mkdir(exist_ok=True)
            
            env_file = service_dir / ".env.local"
            lines = [f"# {service} service-specific environment variables\n", "# DO NOT COMMIT - This file is git-ignored\n"]
            
            for item in items:
                value = self.value_hashes[item['value_hash']]
                lines.append(f"{item['name']}={value}")
            
            env_file.write_text('\n'.join(lines))
            
            # Write service README
            readme_file = service_dir / "README.md"
            readme_content = f"""# {service} Service Secrets

This directory contains service-specific environment variables for {service}.

## Files

- `.env.local` - Service-specific environment variables (DO NOT COMMIT)

## Normalized Keys

"""
            for item in items:
                readme_content += f"- `{item['name']}`\n"
            
            readme_file.write_text(readme_content)
    
    def _write_registry(self):
        """Update registry.yaml, merging with existing data."""
        registry_file = self.output_base / "registry.yaml"
        
        # Load existing registry if it exists
        registry = {
            "global_env": [],
            "services": {},
            "unknown": 0
        }
        
        if registry_file.exists():
            try:
                import yaml
                with open(registry_file, 'r') as f:
                    existing = yaml.safe_load(f) or {}
                    registry['global_env'] = existing.get('global_env', [])
                    registry['services'] = existing.get('services', {})
                    registry['unknown'] = existing.get('unknown', 0)
            except Exception:
                # If YAML parsing fails, try JSON
                import json
                try:
                    with open(registry_file, 'r') as f:
                        existing = json.load(f) or {}
                        registry['global_env'] = existing.get('global_env', [])
                        registry['services'] = existing.get('services', {})
                        registry['unknown'] = existing.get('unknown', 0)
                except Exception:
                    pass  # Start fresh if both fail
        
        # Add new global env keys
        for item in self.parsed_data['api_keys']:
            if item['key_name'] not in registry['global_env']:
                registry['global_env'].append(item['key_name'])
        
        for item in self.parsed_data['env_vars']:
            if item['scope'] == 'global' and item['name'] not in registry['global_env']:
                registry['global_env'].append(item['name'])
        
        # Add new services and update counts
        services_seen = set()
        for category in ['api_keys', 'credentials', 'tokens', 'db_uris', 'env_vars', 'endpoints']:
            for item in self.parsed_data[category]:
                service = item.get('service', 'unknown')
                if service != 'unknown' and service not in services_seen:
                    services_seen.add(service)
                    if service not in registry['services']:
                        registry['services'][service] = {
                            'env': [],
                            'credentials': 0,
                            'tokens': 0,
                            'endpoints': 0,
                            'ssh': []
                        }
        
        # Update service data with new items
        for item in self.parsed_data['env_vars']:
            service = item.get('service')
            if service and service in registry['services']:
                if item['name'] not in registry['services'][service]['env']:
                    registry['services'][service]['env'].append(item['name'])
        
        for item in self.parsed_data['credentials']:
            service = item.get('service')
            if service and service in registry['services']:
                registry['services'][service]['credentials'] += 1
        
        for item in self.parsed_data['tokens']:
            service = item.get('service')
            if service and service in registry['services']:
                registry['services'][service]['tokens'] += 1
        
        for item in self.parsed_data['endpoints']:
            service = item.get('service')
            if service and service in registry['services']:
                registry['services'][service]['endpoints'] += 1
        
        for item in self.parsed_data['ssh']:
            service = item.get('service', 'global')
            if service == 'global':
                if 'ssh' not in registry:
                    registry['ssh'] = []
                if item['path_written'] not in registry['ssh']:
                    registry['ssh'].append(item['path_written'])
        
        # Update unknown count (cumulative)
        registry['unknown'] += len(self.parsed_data['unknown'])
        
        # Write YAML (fallback to JSON if PyYAML not available)
        try:
            import yaml
            with open(registry_file, 'w') as f:
                yaml.dump(registry, f, default_flow_style=False, sort_keys=False)
        except ImportError:
            # Fallback to JSON with .yaml extension (less ideal but works)
            import json
            with open(registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
    
    def _update_readme(self):
        """Update secrets/README.md with run count and timestamp summary."""
        readme_path = self.output_base / "README.md"
        
        # Count intake runs
        intake_files = list(self.intake_dir.glob("*_raw.txt"))
        run_count = len(intake_files)
        
        # Get latest timestamp
        latest_timestamp = self.timestamp
        
        # Get all services from current and previous runs
        services_detected = set()
        for category in ['api_keys', 'credentials', 'tokens', 'db_uris', 'env_vars', 'endpoints']:
            for item in self.parsed_data[category]:
                service = item.get('service')
                if service and service != 'unknown':
                    services_detected.add(service)
        
        # Load existing services from registry if available
        registry_file = self.output_base / "registry.yaml"
        if registry_file.exists():
            try:
                import yaml
                with open(registry_file, 'r') as f:
                    registry = yaml.safe_load(f) or {}
                    if 'services' in registry:
                        for service in registry['services'].keys():
                            services_detected.add(service)
            except Exception:
                pass
        
        readme_content = f"""# Confer Agent Kit Secrets Workspace

**DO NOT COMMIT SECRETS** - This directory is git-ignored.

## Structure

\`\`\`
secrets/
  _intake/              # Raw dumps and parse reports (timestamped)
  global/               # Reusable cross-project secrets
    .env.global         # Global environment variables
    credentials.csv     # Username/password pairs (masked)
    tokens.csv          # Bearer/JWT tokens (masked)
    endpoints.csv       # Service URLs
    ssh/                # SSH keys
  services/             # Service-specific secrets
    <service>/          # Per-service directory
      .env.local        # Service env vars
      README.md         # Documentation
  registry.yaml         # Master index
  README.md             # This file
\`\`\`

## Usage

### Global vs Service-Scoped Secrets

**Global secrets** (`.env.global`): Reusable across projects
- API keys for external services (OpenAI, Groq, etc.)
- Universal tokens
- Shared credentials

**Service-scoped secrets** (`services/<service>/.env.local`): Specific to one service
- Database connection strings for a specific service
- Service-specific API keys
- Local development overrides

### How to Reference

**Locally:**
\`\`\`bash
# Source global secrets
source secrets/global/.env.global

# Or source service-specific
source secrets/services/openai/.env.local
\`\`\`

**In platforms (Coolify/Vercel/Replit):**
- **DO NOT** upload raw `.env.global` or `.env.local` files
- Instead, add individual environment variables through platform UI
- Use the keys from `.env.global` or service `.env.local` files

### Recommended Secret Managers

For team sharing, use:
- **1Password** - Secure team vaults
- **Bitwarden** - Open-source password manager
- **Doppler** - Developer-first secret management
- **AWS Secrets Manager** / **GCP Secret Manager** - Cloud-native

### Rotation Checklist

- [ ] Review `secrets/_intake/` for new additions
- [ ] Update platform env vars when rotating keys
- [ ] Update `registry.yaml` when adding services
- [ ] Remove old keys from `.env.global` or service `.env.local`
- [ ] Verify no secrets in git history: `git log --all --full-history -- "**/*.env*"`

## Parse History

**Total Intake Runs:** {run_count}
**Latest Parse:** {latest_timestamp} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

## Detected Services

The following services have been detected across all parse runs:

{', '.join(sorted(services_detected)) if services_detected else 'None'}

## Safety

- **All files under `secrets/` are git-ignored**
- **Never commit secrets** - use platform env vars instead
- **Rotate keys regularly** - check `registry.yaml` for active keys
- **Mask in logs** - secrets are masked (first 4 + last 2 chars) in reports
"""
        
        readme_path.write_text(readme_content)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            raw_text = f.read()
    else:
        # Read from stdin
        raw_text = sys.stdin.read()
    
    parser = SecretsParser()
    parsed = parser.parse_raw_text(raw_text)
    outputs = parser.write_outputs(raw_text)
    
    # Print summary
    print("\n=== Secrets Parse Complete ===\n")
    print(f"✓ Raw text saved: {outputs['raw_file']}")
    print(f"✓ Parsed JSON saved: {outputs['json_file']}")
    print(f"✓ Report saved: {outputs['report_file']}\n")
    
    print("Summary by category:")
    for category, items in parsed.items():
        if items:
            print(f"  - {category.replace('_', ' ').title()}: {len(items)}")
    
    services_detected = set()
    for category in ['api_keys', 'credentials', 'tokens', 'db_uris', 'env_vars', 'endpoints']:
        for item in parsed[category]:
            service = item.get('service')
            if service and service != 'unknown':
                services_detected.add(service)
    
    if services_detected:
        print(f"\n✓ Services detected: {', '.join(sorted(services_detected))}")
    
    if parsed['unknown']:
        print(f"\n⚠ Unknown items requiring review: {len(parsed['unknown'])}")
        print("   Check the parse report for details.")

