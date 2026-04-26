from Crypto.Util.number import isPrime, long_to_bytes
from sympy import factorint

c = 51928041009610903907250167459141284736642390382647761645469323779693816825809
d = 48470908100112652272702147130867162993853216436313071201013056157778976494289
e = 65537

target = e * d - 1
factors_dict = factorint(target)
factors = [f for f, exp in factors_dict.items() for _ in range(exp)]

# Try combinations to find p-1 and q-1
for i in range(1 << len(factors)):
    p_m1 = 1
    for j in range(len(factors)):
        if (i >> j) & 1: p_m1 *= factors[j]
    
    if 127 <= p_m1.bit_length() <= 128 and isPrime(p_m1 + 1):
        rem = target // p_m1
        # Try to find q-1 in the remaining factors
        for k in range(1 << len(factors)):
            if (i & k) == 0: # Disjoint sets
                q_m1 = 1
                for l in range(len(factors)):
                    if (k >> l) & 1: q_m1 *= factors[l]
                
                if 127 <= q_m1.bit_length() <= 128 and isPrime(q_m1 + 1):
                    N = (p_m1 + 1) * (q_m1 + 1)
                    msg = long_to_bytes(pow(c, d, N))
                    if len(msg) == 16:
                        print(f"Decoded Message: {msg.decode()}")
                        exit()