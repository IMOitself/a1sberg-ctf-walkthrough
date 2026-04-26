import base64

def xor(data, key):
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

debug_info_b64 = "UfMmILf40ANQcXfGSljmgFriMh+K+YsObBUEsFFYiYVW4VkEsfqCRHljDOdTWuLFTZZYRpz49QRRbwDtY3PmgE7NBE0="
debug_info = base64.b64decode(debug_info_b64)
combined = base64.b64decode("AKdgdNLLu3Q0J06BBx6w9Q==")

result = xor(debug_info, combined)
print(f"Key: {combined}")
print(f"Result: {result}")
print(f"decode from base64: {base64.b64decode(result)}")
