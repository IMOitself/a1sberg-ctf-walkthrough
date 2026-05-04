freqs = [] # paste the frequencies here from the writeup

flag = ""

for i in freqs:
  frequency = round(i) 
  ascii_text = (frequency + 136) / 18  # ASCII = (frequency + 136) / 18 | (our formula from the writeup)
  flag += chr(int(ascii_text)) 

print(flag)