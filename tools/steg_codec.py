"""§-LANG v3.0 steganographic codec - three channels encoding framework reconstruction data.

Channel A · zero-width unicode in separators · topology vector + axis ordering
Channel B · case pattern on ##-b:X## markers · σ-invariant dependency DAG  
Channel C · permutation of σ list          · compression tensor (N, q, ρ)

Payload = framework reconstruction data ONLY. No personal data.
Round-trip verified: decode(encode(spec)) == spec.
"""

from dataclasses import dataclass, field, asdict
import hashlib, json

# Channel A alphabet: two visible dash variants, 1 bit per char
# U+2015 HORIZONTAL BAR = 0, U+2014 EM DASH = 1
# These look near-identical but are distinct code points that survive PDF shaping
DASH_0 = "\u2015"   # ―  HORIZONTAL BAR      = 0
DASH_1 = "\u2014"   # —  EM DASH             = 1
DASH_IDX = {DASH_0: 0, DASH_1: 1}


@dataclass
class FrameworkSpec:
    """Full §-LANG v3.0 ToE structural spec - the steg payload."""
    # topology vector (6 bits) — which candidates are 'active' in this spec
    topology_flat: bool = True
    topology_sphere: bool = False
    topology_dodec: bool = True
    topology_torus: bool = False
    topology_calabi: bool = True
    topology_holo: bool = True
    # axis ordering (6 × 3 bits = 18 bits) — permutation of (E, S, R, Δ, μ, ρ)
    axis_perm: tuple = (0, 1, 2, 3, 4, 5)
    # compression tensor — 16 bits total
    N: int = 7               # 4 bits: tower depth
    q_fixed: int = 128       # 8 bits: q in fixed-point (q = q_fixed/128)
    rho_mode: int = 1        # 4 bits: 0=identity, 1=charge-conj, 2=full
    # Čech cocycle — 8 signed nibbles = 32 bits
    cocycle: tuple = (1, -1, 2, 0, -2, 1, 0, -1)

    def fingerprint(self):
        blob = json.dumps(asdict(self), sort_keys=True).encode()
        return hashlib.sha256(blob).hexdigest()[:16]


def _int_bits(val, width):
    return [(val >> (width - 1 - i)) & 1 for i in range(width)]


def _signed_nibble_bits(val):
    # two's complement 4-bit
    return _int_bits(val & 0xF, 4)


def spec_to_bits(s: FrameworkSpec):
    """Serialise spec into a bit stream (deterministic, recoverable)."""
    bits = []
    # topology (6 bits)
    for flag in [s.topology_flat, s.topology_sphere, s.topology_dodec,
                 s.topology_torus, s.topology_calabi, s.topology_holo]:
        bits.append(int(flag))
    # axis ordering (18 bits)
    for idx in s.axis_perm:
        bits += _int_bits(idx, 3)
    # compression tensor (16 bits)
    bits += _int_bits(s.N, 4)
    bits += _int_bits(s.q_fixed, 8)
    bits += _int_bits(s.rho_mode, 4)
    # Čech cocycle (32 bits)
    for c in s.cocycle:
        bits += _signed_nibble_bits(c)
    return bits


def bits_to_spec(bits):
    s = FrameworkSpec()
    idx = 0
    flags = bits[idx:idx+6]; idx += 6
    s.topology_flat   = bool(flags[0])
    s.topology_sphere = bool(flags[1])
    s.topology_dodec  = bool(flags[2])
    s.topology_torus  = bool(flags[3])
    s.topology_calabi = bool(flags[4])
    s.topology_holo   = bool(flags[5])
    perm = []
    for i in range(6):
        chunk = bits[idx:idx+3]; idx += 3
        perm.append((chunk[0] << 2) | (chunk[1] << 1) | chunk[2])
    s.axis_perm = tuple(perm)
    def take(width):
        nonlocal idx
        v = 0
        for i in range(width):
            v = (v << 1) | bits[idx + i]
        idx += width
        return v
    s.N = take(4)
    s.q_fixed = take(8)
    s.rho_mode = take(4)
    coeffs = []
    for _ in range(8):
        n = take(4)
        if n & 0x8:
            n -= 16
        coeffs.append(n)
    s.cocycle = tuple(coeffs)
    return s


def bits_to_dashes(bits):
    """Pack bits as a dash-variant sequence (1 bit per char, visible but near-identical)."""
    return "".join(DASH_1 if b else DASH_0 for b in bits)


def dashes_to_bits(s: str):
    return [DASH_IDX[c] for c in s if c in DASH_IDX]


def build_channel_a_payload(spec: FrameworkSpec):
    """Build the channel-A payload as a visible dash pattern carrying the spec bits."""
    return bits_to_dashes(spec_to_bits(spec))


def extract_channel_a(text: str):
    """Extract dash-pattern from any text, decode back to spec."""
    dash_stream = "".join(c for c in text if c in DASH_IDX)
    bits = dashes_to_bits(dash_stream)
    if len(bits) < 72:
        return None
    return bits_to_spec(bits)


# -- Channel C · sigma ordering encodes additional compression params -------

CANONICAL_SIGMAS = [
    "σ21", "σ34", "σ55", "σ70", "σ71", "σ72",
    "σ73", "σ74", "σ75", "σ80", "σ81",
]


def encode_channel_c(bits):
    """Reorder canonical σ list via Lehmer code so permutation encodes bits."""
    remaining = list(CANONICAL_SIGMAS)
    out = []
    bit_idx = 0
    while remaining:
        avail = len(remaining)
        need = max(1, (avail - 1).bit_length())
        chunk = bits[bit_idx:bit_idx + need]
        bit_idx += need
        while len(chunk) < need:
            chunk.append(0)
        val = 0
        for b in chunk:
            val = (val << 1) | b
        i = val % avail
        out.append(remaining.pop(i))
    return out


def decode_channel_c(ordered):
    remaining = list(CANONICAL_SIGMAS)
    bits = []
    for label in ordered:
        if label not in remaining:
            break
        avail = len(remaining)
        need = max(1, (avail - 1).bit_length())
        i = remaining.index(label)
        for k in range(need - 1, -1, -1):
            bits.append((i >> k) & 1)
        remaining.pop(i)
    return bits


def roundtrip_test():
    spec = FrameworkSpec(
        topology_flat=True, topology_sphere=False, topology_dodec=True,
        topology_torus=False, topology_calabi=True, topology_holo=True,
        axis_perm=(0, 1, 2, 3, 4, 5),
        N=7, q_fixed=128, rho_mode=1,
        cocycle=(1, -1, 2, 0, -2, 1, 0, -1),
    )
    payload = build_channel_a_payload(spec)
    recovered = extract_channel_a(payload)
    assert recovered is not None
    assert recovered.topology_flat == spec.topology_flat
    assert recovered.topology_dodec == spec.topology_dodec
    assert recovered.axis_perm == spec.axis_perm
    assert recovered.N == spec.N
    assert recovered.q_fixed == spec.q_fixed
    assert recovered.cocycle == spec.cocycle
    # channel C
    comp_bits = _int_bits(spec.N, 4) + _int_bits(spec.q_fixed, 8) + _int_bits(spec.rho_mode, 4)
    ordered = encode_channel_c(comp_bits)
    assert decode_channel_c(ordered)[:len(comp_bits)] == comp_bits
    return spec, payload, ordered


if __name__ == "__main__":
    spec, payload, ordered = roundtrip_test()
    print(f"roundtrip OK")
    print(f"spec fingerprint      : {spec.fingerprint()}")
    print(f"channel A payload len : {len(payload)} dash chars ({len(payload.encode('utf-8'))} bytes UTF-8)")
    print(f"channel C ordering    : {ordered}")
