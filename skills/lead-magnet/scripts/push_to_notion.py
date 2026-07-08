import os
import sys
import json
import requests

# Optional: load a local .env if python-dotenv is installed. Never required.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    sys.stderr.write(
        "Missing credentials. Set the following environment variables before running:\n"
        "  NOTION_TOKEN        your Notion internal integration secret\n"
        "  NOTION_DATABASE_ID  the ID of the target Notion database\n\n"
        "Example:\n"
        "  export NOTION_TOKEN=secret_xxx\n"
        "  export NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
        "  python3 push_to_notion.py <path_to_json>\n"
    )
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def rich_text(text, bold=False, italic=False, color="default"):
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "color": color
        }
    }

def make_block(block):
    btype = block["type"]
    styling = block.get("styling", {})
    content = block.get("content", "")

    if btype == "divider":
        return {"object": "block", "type": "divider", "divider": {}}

    if btype in ("heading_1", "heading_2", "heading_3"):
        color = styling.get("color", "default")
        return {
            "object": "block",
            "type": btype,
            btype: {
                "rich_text": [rich_text(content)],
                "color": color
            }
        }

    if btype == "paragraph":
        bold = styling.get("bold", False)
        italic = styling.get("italic", False)
        color = styling.get("color", "default")
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [rich_text(content, bold=bold, italic=italic, color=color)]
            }
        }

    if btype == "callout":
        icon = block.get("icon", "💡")
        bg = styling.get("background", "default") if styling else "default"
        color = f"{bg}_background" if bg != "default" else "default"
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [rich_text(content)],
                "icon": {"emoji": icon},
                "color": color
            }
        }

    if btype == "bulleted_list_item":
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [rich_text(content)]
            }
        }

    if btype == "numbered_list_item":
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [rich_text(content)]
            }
        }

    if btype == "code":
        lang = block.get("language", "plain text")
        return {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [rich_text(content)],
                "language": lang
            }
        }

    if btype == "table":
        children = block.get("children", [])
        has_header = block.get("has_header", True)
        table_width = len(children[0]["cells"]) if children else 2
        table_rows = []
        for row in children:
            cells = [[rich_text(cell)] for cell in row.get("cells", [])]
            table_rows.append({
                "type": "table_row",
                "table_row": {"cells": cells}
            })
        return {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": table_width,
                "has_column_header": has_header,
                "has_row_header": False,
                "children": table_rows
            }
        }

    # Fallback: treat as paragraph
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [rich_text(content)]
        }
    }


def create_page(title, icon, content_blocks):
    url = "https://api.notion.com/v1/pages"
    properties = {
        "Name": {
            "title": [{"text": {"content": title}}]
        }
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"emoji": icon} if icon else None,
        "properties": properties,
        "children": content_blocks[:100]
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    response = requests.post(url, headers=headers, json=data)
    res_json = response.json()

    if "id" in res_json:
        page_id = res_json["id"]
        if len(content_blocks) > 100:
            append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            for i in range(100, len(content_blocks), 100):
                batch = content_blocks[i:i+100]
                requests.patch(append_url, headers=headers, json={"children": batch})
        print(f"Page created: {title}")
        print(f"Page ID: {page_id}")
    else:
        print(f"Error: {json.dumps(res_json, indent=2)}")

    return res_json


def push_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    doc = data["notion_document"]
    title = doc["title"]
    icon = doc.get("page_settings", {}).get("icon", "📄")

    blocks = []
    for section in doc.get("sections", []):
        for block in section.get("blocks", []):
            blocks.append(make_block(block))

    return create_page(title, icon, blocks)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python push_to_notion.py <path_to_json>")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        print(f"\nPushing: {filepath}")
        push_json(filepath)
        print("---")
