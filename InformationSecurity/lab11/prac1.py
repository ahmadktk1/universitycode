import hashlib


# ----------------------------
# 1. HASH FUNCTION
# ----------------------------
def get_hash(message):
    h = hashlib.sha256()
    h.update(message.encode())
    return h.hexdigest()


# ----------------------------
# 2. SIMPLE "KEYS"
# (for learning purpose only)
# ----------------------------
private_key = 123  # sender key
public_key = 123   # receiver key (same for simplicity)


# ----------------------------
# 3. "ENCRYPT" SIGNATURE
# (simulate private key signing)
# ----------------------------
def sign_hash(hash_value, key):
    signature = ""
    for ch in hash_value:
        signature += chr((ord(ch) + key) % 256)
    return signature


# ----------------------------
# 4. "DECRYPT" SIGNATURE
# (simulate public key verification)
# ----------------------------
def verify_signature(signature, key):
    original_hash = ""
    for ch in signature:
        original_hash += chr((ord(ch) - key) % 256)
    return original_hash


# ----------------------------
# 5. DIGITAL SIGNATURE PROCESS
# ----------------------------
def digital_signature_process(message):

    print("\n--- SENDER SIDE ---")

    # Step 1: Hash message
    msg_hash = get_hash(message)
    print("Message:", message)
    print("Hash:", msg_hash)

    # Step 2: Sign hash
    signature = sign_hash(msg_hash, private_key)
    print("Signature generated:", signature)

    print("\n--- RECEIVER SIDE ---")

    # Step 3: verify signature
    received_hash = verify_signature(signature, public_key)
    print("Recovered Hash:", received_hash)

    # Step 4: recompute hash
    new_hash = get_hash(message)
    print("Recomputed Hash:", new_hash)

    # Step 5: compare
    print("\n--- VERIFICATION RESULT ---")
    if received_hash == new_hash:
        print("✅ Digital Signature Verified (Data Authentic)")
    else:
        print("❌ Verification Failed (Data Tampered)")


# ----------------------------
# MAIN
# ----------------------------
msg = input("Enter message: ")
digital_signature_process(msg)
