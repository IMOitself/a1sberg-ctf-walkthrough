import subprocess
import re
import base64

def get_queries():
    # tshark -r ecchi_packet.pcap -Y 'dns.flags.response == 0 and dns.qry.name contains "cdn-updates.com"' -T fields -e dns.qry.name
    cmd = ['tshark', '-r', 'ecchi_packet.pcap', '-Y', 'dns.flags.response == 0 and dns.qry.name contains "cdn-updates.com"', '-T', 'fields', '-e', 'dns.qry.name']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.splitlines()

def solve():
    queries = get_queries()
    data_map = {}
    
    # Pattern: s{index}.{base64_data}.cdn-updates.com
    pattern = re.compile(r's(\d+)\.([^.]+)\.cdn-updates\.com')
    
    for q in queries:
        match = pattern.search(q)
        if match:
            idx = int(match.group(1))
            b64_part = match.group(2)
            data_map[idx] = b64_part
            
    sorted_indices = sorted(data_map.keys())
    full_b64 = "".join(data_map[i] for i in sorted_indices)
    
    # Try to decode
    try:
        # DNS might use slightly different b64 or have padding issues
        # Add padding if needed
        missing_padding = len(full_b64) % 4
        if missing_padding:
            full_b64 += '=' * (4 - missing_padding)
            
        decoded_data = base64.b64decode(full_b64)
        with open('output.bin', 'wb') as f:
            f.write(decoded_data)
        print(f"Decoded {len(decoded_data)} bytes to output.bin")
        
        # Check for ZIP header
        if decoded_data.startswith(b'PK\x03\x04'):
            print("Detected ZIP file! Saving as output.zip")
            with open('output.zip', 'wb') as f:
                f.write(decoded_data)
    except Exception as e:
        print(f"Error decoding: {e}")

if __name__ == "__main__":
    solve()
