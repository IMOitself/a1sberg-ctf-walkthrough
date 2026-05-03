The description talks about *"overlapping harmonics"*, *"frequency shifts"*, and *"reversal"* — all of which sound complex, but the actual solution is much more straightforward once you know where to look.

We are given an audio file named `resonance.wav`. Opening it in a spectrogram viewer (like Boxentriq) immediately shows a series of clean vertical lines at different heights. Each line is a single tone playing for about 280ms before switching to the next one — 36 tones total.

![spectrogram screenshot](./resonance-spectrogram.png)

It is tempting to try Morse code, DTMF decoding, or LSB steganography — but none of those work here. The real encoding is simpler than the description implies: **each tone's frequency directly maps to an ASCII character using a linear formula.**

---

### The Solution

First, extract the dominant frequency from each chunk of audio:

```python
import wave, numpy as np
from scipy.fft import fft

with wave.open('resonance.wav', 'r') as w:
    fs = w.getframerate()
    audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

chunk = int(fs * 0.28)
win = np.hanning(chunk)
freqs = []

for i in range(0, len(audio) - chunk, chunk):
    s = np.abs(fft(audio[i:i+chunk] * win, n=chunk*8))
    f = np.fft.fftfreq(chunk*8, 1/fs)
    pos = (f > 200) & (f < 3000)
    freqs.append(f[pos][np.argmax(s[pos])])

print(freqs)
```

```
[1033.9, 746.0, 1357.6, 2077.7, 1915.6, 781.7, 817.9, 727.7, 1843.7, 800.0,
 1843.7, 1951.8, 1573.7, 1735.7, 800.0, 1915.6, 1825.9, 727.7, 1843.7, 746.0,
 781.7, 817.9, 1573.7, 1951.8, 727.7, 1573.7, 1951.8, 1735.7, 781.7, 1573.7,
 1700.0, 746.0, 1843.7, 781.7, 817.9, 1951.8, 2114.0]
```

Since we know the flag format is `A1S{}`, the first four tones must be `A`, `1`, `S`, `{`. Using those as reference points, we can figure out the formula.

We know `A = 65` maps to `1034 Hz` and `1 = 49` maps to `746 Hz`. Assuming the relationship is linear (`freq = a × ASCII + b`), we solve:

```
1034 - 746 = a × (65 - 49)
288 = a × 16
a = 18

b = 746 - (18 × 49) = -136
```

Flip it around to decode frequency back to ASCII:

```
ASCII = (frequency + 136) / 18
```

We verified it on `S` and `{` and it matched perfectly, so we applied it to all 36 frequencies:

```python
a = (freqs[0] - freqs[1]) / (65 - 49)
b = freqs[1] - 49 * a

flag = ''.join(chr(round((f - b) / a)) for f in freqs)
print(flag)
```

```
A1S{REDACTED}
```