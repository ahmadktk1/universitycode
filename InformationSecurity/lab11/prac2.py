import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import sys

# ─────────────────────────────────────────
#  SENDER SIDE
# ─────────────────────────────────────────

def get_capacity(image_path, channel=0):
    """Max bits we can hide in one color channel."""
    img = np.array(Image.open(image_path).convert("RGB"))
    h, w, _ = img.shape
    return h * w  # 1 bit per pixel in chosen channel


def embed_message(image_path, message, key, channel=0):
    """
    Embeds message into cover image using LSB on a single channel.
    Positions are randomized using the numeric key.
    Returns the stego image array.
    """
    img = np.array(Image.open(image_path).convert("RGB"))
    h, w, _ = img.shape
    total_pixels = h * w

    # Encode message to bits (prepend 32-bit length header)
    msg_bytes = message.encode("utf-8")
    msg_len   = len(msg_bytes) * 8          # length in bits
    header    = format(msg_len, "032b")     # 32-bit binary header
    all_bits  = header + "".join(format(b, "08b") for b in msg_bytes)

    capacity = total_pixels
    print(f"[INFO] Message bits (with header): {len(all_bits)}")
    print(f"[INFO] Image capacity (bits):      {capacity}")

    if len(all_bits) > capacity:
        print("Error: Message is too large for this image.")
        sys.exit(1)

    # Randomize pixel positions with the key
    positions = list(range(total_pixels))
    random.seed(key)
    random.shuffle(positions)

    flat = img[:, :, channel].flatten().copy()

    for i, bit in enumerate(all_bits):
        px = positions[i]
        flat[px] = (int(flat[px]) & 0xFE) | int(bit)   # set LSB

    stego = img.copy()
    stego[:, :, channel] = flat.reshape(h, w)
    return stego


# ─────────────────────────────────────────
#  RECEIVER SIDE
# ─────────────────────────────────────────

def extract_message(stego_path, key, channel=0):
    """
    Extracts hidden message from stego image using the same key.
    """
    img = np.array(Image.open(stego_path).convert("RGB"))
    h, w, _ = img.shape
    total_pixels = h * w
    capacity = total_pixels

    # Rebuild same shuffled positions
    positions = list(range(total_pixels))
    random.seed(key)
    random.shuffle(positions)

    flat = img[:, :, channel].flatten()

    # Read 32-bit length header first
    header_bits = ""
    for i in range(32):
        header_bits += str(flat[positions[i]] & 1)

    msg_len = int(header_bits, 2)   # bits
    print(f"[INFO] Extracted message length: {msg_len} bits")

    # Validate
    if msg_len > capacity:
        print("Error: Message length is invalid. Image may be corrupted.")
        sys.exit(1)

    # Read message bits
    msg_bits = ""
    for i in range(32, 32 + msg_len):
        msg_bits += str(flat[positions[i]] & 1)

    # Convert bits → bytes → string
    chars = [chr(int(msg_bits[i:i+8], 2)) for i in range(0, len(msg_bits), 8)]
    return "".join(chars)


# ─────────────────────────────────────────
#  VISUALISATION
# ─────────────────────────────────────────

def show_images(cover_path, stego_array):
    cover = np.array(Image.open(cover_path).convert("RGB"))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.patch.set_facecolor("#0d0d0d")

    for ax in axes:
        ax.set_facecolor("#0d0d0d")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333")

    axes[0].imshow(cover)
    axes[0].set_title("Cover Image\n(original)", color="#aaffaa",
                       fontsize=12, fontfamily="monospace")
    axes[0].axis("off")

    axes[1].imshow(stego_array)
    axes[1].set_title("Stego Image\n(message hidden inside)", color="#ffaa44",
                       fontsize=12, fontfamily="monospace")
    axes[1].axis("off")

    plt.suptitle("LSB Steganography — Single Channel Embedding",
                 color="white", fontsize=14, fontfamily="monospace", y=1.02)
    plt.tight_layout()
    plt.savefig("comparison.png", dpi=150, bbox_inches="tight",
                facecolor="#0d0d0d")
    plt.show()
    print("[INFO] Comparison saved → comparison.png")


# ─────────────────────────────────────────
#  MAIN DEMO
# ─────────────────────────────────────────

if __name__ == "__main__":

    # ── Parameters (change these) ──────────
    COVER_IMAGE  = "cover.png"      # path to your cover image
    SECRET_MSG   = "Hello! This is a secret message hidden with LSB steganography."
    KEY          = 42               # numeric key for randomized embedding
    STEGO_IMAGE  = "stego.png"      # output stego image path
    CHANNEL      = 0                # 0=Red, 1=Green, 2=Blue
    # ──────────────────────────────────────

    print("=" * 50)
    print("          STEGANOGRAPHY SYSTEM")
    print("=" * 50)

    # ── SENDER ────────────────────────────
    print("\n[SENDER] Computing capacity...")
    cap = get_capacity(COVER_IMAGE, CHANNEL)
    print(f"[SENDER] Max capacity: {cap} bits ({cap // 8} bytes)")

    print("[SENDER] Embedding message...")
    stego = embed_message(COVER_IMAGE, SECRET_MSG, KEY, CHANNEL)

    Image.fromarray(stego).save(STEGO_IMAGE)
    print(f"[SENDER] Stego image saved → {STEGO_IMAGE}")

    # ── RECEIVER ──────────────────────────
    print("\n[RECEIVER] Extracting message...")
    recovered = extract_message(STEGO_IMAGE, KEY, CHANNEL)
    print(f"[RECEIVER] Recovered message: \"{recovered}\"")

    # Verify
    print("\n[CHECK] Match:", "✓ PASS" if recovered == SECRET_MSG else "✗ FAIL")

    # ── VISUALISE ─────────────────────────
    show_images(COVER_IMAGE, stego)
