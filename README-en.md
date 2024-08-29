# How to Use NezuNotify

日本語: [README.md](README.md)

## Overview

NezuNotify is a Python library for easy utilization of LINE Notify. Its main features include:

- Sending messages to LINE groups
- Sending images (via URL or local file)
- Sending stickers
- Token generation and management
- Token revocation
- Retrieving group information

## Installation

`git clone https://github.com/nezumi0627/NezuNotify.git`

## Usage

1. Create a `.env` file in the project's root directory.
2. Add the following content to the `.env` file, replacing with actual values:

```plaintext
LINE_CSRF_TOKEN=""
LINE_COOKIE=""
```

3. Token Management

```python
# Create a token
nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_id)
new_token = nezu_create.process("create", "NezuNotify")

# Check token status
nezu_check = NezuNotify(token=token, csrf=csrf, cookie=cookie)
status = nezu_check.process("check", token)

# Revoke a token
nezu = NezuNotify(token=token, csrf=csrf, cookie=cookie)
revoke_result = nezu.process("revoke")

# Get group list
group_manager = GroupManager(csrf=csrf, cookie=cookie)
groups = group_manager.get_groups()

for i, group in enumerate(groups, 1):
    logging.info(f"{i}. Name: {group['name']}, ID: {group['mid']}, Image URL: {group['pictureUrl']}")

```

4. Sending Messages

```python
nezu_text = NezuNotify(
    token=token,
    message_type="text",
    message_content="This is a test message."
)
send_result = nezu_text.process("send")
```

5. Sending Images

```python
# Send image using URL
image_url = "https://example.com/image.jpg"
nezu_url_image = NezuNotify(
    token=token,
    message_type="image",
    message_content=image_url
)
send_result = nezu_url_image.process("send")

# Send image from local file
local_image_path = "/path/to/local/image.jpg"
nezu_local_image = NezuNotify(
    token=token,
    message_type="image",
    message_content=local_image_path
)
send_result = nezu_local_image.process("send")
```

6. Sending Stickers

```python
nezu_sticker = NezuNotify(
    token=token,
    message_type="sticker",
    message_content="Sticker message!!",
    sticker_id="171",
    sticker_package_id="2"
)
send_result = nezu_sticker.process("send")
```

## Precautions

- Manage LINE Notify tokens securely.
- Be mindful of API usage limits.
- When sending images, use sizes and formats compatible with LINE specifications.
- For detailed usage and advanced features, refer to the official documentation.
