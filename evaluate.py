import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_chat(messages):
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"messages": messages}
    )
    return response.json()

print("=" * 50)
print("SHL RECOMMENDER EVALUATION")
print("=" * 50)

# Test 1: Vague query should ask clarifying question
print("\nTEST 1: Vague query")
result = test_chat([{"role": "user", "content": "I need an assessment"}])
has_recs = len(result["recommendations"]) > 0
print(f"Reply: {result['reply'][:80]}...")
print(f"Recommendations empty: {not has_recs}")
print(f"PASS ✅" if not has_recs else "FAIL ❌")

# Test 2: Clear query should give recommendations
print("\nTEST 2: Clear query - Java developer")
result = test_chat([{"role": "user", "content": "I am hiring a mid level Java developer"}])
has_recs = len(result["recommendations"]) > 0
print(f"Reply: {result['reply'][:80]}...")
print(f"Recommendations count: {len(result['recommendations'])}")
print(f"PASS ✅" if has_recs else "FAIL ❌")

# Test 3: Off-topic should be refused
print("\nTEST 3: Off-topic question")
result = test_chat([{"role": "user", "content": "What salary should I offer a Java developer?"}])
has_recs = len(result["recommendations"]) > 0
print(f"Reply: {result['reply'][:80]}...")
print(f"No recommendations given: {not has_recs}")
print(f"PASS ✅" if not has_recs else "FAIL ❌")

# Test 4: Recommendations should have correct fields
print("\nTEST 4: Schema check")
result = test_chat([
    {"role": "user", "content": "I am hiring a Python data scientist senior level"}
])
if result["recommendations"]:
    rec = result["recommendations"][0]
    has_name = "name" in rec
    has_url = "url" in rec
    has_type = "test_type" in rec
    url_valid = rec["url"].startswith("https://www.shl.com")
    print(f"Has name: {has_name}")
    print(f"Has url: {has_url}")
    print(f"Has test_type: {has_type}")
    print(f"URL is from SHL: {url_valid}")
    print(f"PASS ✅" if all([has_name, has_url, has_type, url_valid]) else "FAIL ❌")
else:
    print("No recommendations returned - bot still clarifying")

# Test 5: Refine recommendations
print("\nTEST 5: Refine recommendations")
result = test_chat([
    {"role": "user", "content": "I am hiring a Java developer"},
    {"role": "assistant", "content": "What seniority level?"},
    {"role": "user", "content": "Mid level. Also add personality tests"}
])
has_recs = len(result["recommendations"]) > 0
print(f"Reply: {result['reply'][:80]}...")
print(f"Recommendations count: {len(result['recommendations'])}")
print(f"PASS ✅" if has_recs else "FAIL ❌")

# Test 6: Health check
print("\nTEST 6: Health check")
response = requests.get(f"{BASE_URL}/health")
is_ok = response.json() == {"status": "ok"}
print(f"Response: {response.json()}")
print(f"PASS ✅" if is_ok else "FAIL ❌")

print("\n" + "=" * 50)
print("EVALUATION COMPLETE")
print("=" * 50)