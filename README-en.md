# How to Use NezuNotify

Japanese: [README.md](README.md)

## Overview

NezuNotify is a Python library that simplifies the use of LINE Notify. Its main features include:

- Sending messages to LINE groups
- Sending images (via URL or local file)
- Token generation and management
- Token revocation
- Retrieving group information

## Installation

`bash

# Clone the repository

git clone https://github.com/nezumi0627/NezuNotify
`

## Usage

1. Setting Environment Variables

```python
# Set environment variables
import os

# Set CSRF token
os.environ["LINE_CSRF_TOKEN"] = "YOUR_CSRF_TOKEN"

# Set Cookie
os.environ["LINE_COOKIE"] = "YOUR_COOKIE"

# Set target MID
os.environ["LINE_TARGET_MID"] = "YOUR_TARGET_MID"

# Set existing token
os.environ["LINE_EXISTING_TOKEN"] = "YOUR_EXISTING_TOKEN"
```

2. Initial Setup

```python
from NezuPuls.nezu_notify import NezuNotify

# Retrieve authentication information from environment variables
csrf = os.environ.get("LINE_CSRF_TOKEN")
cookie = os.environ.get("LINE_COOKIE")
target_mid = os.environ.get("LINE_TARGET_MID")
existing_token = os.environ.get("LINE_EXISTING_TOKEN")
```

3. Token Management

```python
# Create a token
nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_mid)
new_token = nezu_create.process("create", "New Token")

# Check token status
nezu_check = NezuNotify(token=new_token)
status = nezu_check.process("check", new_token)

# Revoke token
nezu_revoke = NezuNotify(token=new_token)
revoke_result = nezu_revoke.process("revoke", new_token)

# Retrieve list of groups
groups = nezu_create.get_groups()
```

4. Sending Messages

`python

# Send a text message

nezu_text = NezuNotify(
token=existing_token,
message_type="text",
message_content="This is a test message."
)
send_result = nezu_text.process("send")
`

5. Sending Images

```python
# Send image using URL
image_url = "https://example.com/image.jpg"
nezu_url_image = NezuNotify(
 token=existing_token,
 message_type="image",
 message_content=image_url
)
send_result = nezu_url_image.process("send")

# Send image using local file
local_image_path = "/path/to/local/image.jpg"
nezu_local_image = NezuNotify(
 token=existing_token,
 message_type="image",
 message_content=local_image_path
)
send_result = nezu_local_image.process("send")
```

## Precautions

- Securely manage your LINE Notify tokens.
- Be aware of API usage limits.
- When sending images, use sizes and formats that comply with LINE specifications.
- For detailed usage instructions and advanced features, please refer to the official documentation.
