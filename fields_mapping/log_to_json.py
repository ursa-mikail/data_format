#!pip install faker
import re
import json
import uuid
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def extract_fields(text):
    result = {}
    lines = text.strip().splitlines()

    # Extract timestamp from the header
    header = lines[0]
    match = re.search(r'\[(.*?)\]', header)
    if match:
        raw_ts = match.group(1)
        try:
            result["timestamp"] = datetime.strptime(raw_ts, "%Y-%m-%d").isoformat()
        except:
            result["timestamp"] = raw_ts  # fallback

    # Extract blocks (in order): log, reference, tags
    block_pattern = r'("""|\'\'\'|```)(.*?)\1'
    blocks = re.findall(block_pattern, text, re.DOTALL)
    block_texts = [b[1].strip() for b in blocks]

    if len(block_texts) >= 3:
        result["log"] = block_texts[0]
        result["reference"] = block_texts[1]
        try:
            result["tags"] = json.loads(block_texts[2])
        except:
            result["tags"] = [tag.strip().strip('"') for tag in block_texts[2].split(",")]

    # Extract score
    score_match = re.search(r'score:\s*([0-9.]+)', text)
    if score_match:
        result["score"] = float(score_match.group(1))

    return result

def generate_fake():
    return {
        "timestamp": fake.iso8601(),
        "log": fake.sentence(),
        "score": round(random.uniform(0, 100), 2),
        "reference": str(uuid.uuid4()),
        "tags": fake.words(nb=random.randint(2, 4))
    }

def remap(entry):
    return {
        "event": {
            "time": entry["timestamp"],
            "message": entry["log"],
            "metrics": {
                "score": entry["score"]
            },
            "meta": {
                "id": entry["reference"]
            },
            "labels": entry["tags"]
        }
    }

def main():
    with open("input.txt") as f:
        input_data = f.read()

    # Extract real and fake entries
    parsed = extract_fields(input_data)
    fake_entry = generate_fake()

    # Save raw extracted and fake
    with open("source.json", "w") as f:
        json.dump([parsed, fake_entry], f, indent=2)

    # Remap both
    remapped = [remap(parsed), remap(fake_entry)]

    with open("target.json", "w") as f:
        json.dump(remapped, f, indent=2)

if __name__ == "__main__":
    main()


