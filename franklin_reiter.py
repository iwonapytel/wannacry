def franklin_reiter_related_message_attack(e, n, c1, c2, a, b):
    assert e == 3 and b != 0
    frac = b * (c2 + 2*pow(a,3)*c1 - pow(b,3))
    denom = a * (c2 - pow(a,3)*c1 + 2*pow(b,3))
    m = (frac * invert(denom, n)) % n
    return m  
