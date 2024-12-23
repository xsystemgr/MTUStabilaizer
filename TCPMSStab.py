from scapy.all import IP, TCP, sr1, conf


def find_best_mss(target_ip, target_port, min_mss=500, max_mss=1460, step=10):
    """
    Find the best TCP MSS value for a given target.

    :param target_ip: Target IP address to test.
    :param target_port: Target port to test.
    :param min_mss: Minimum MSS value to test.
    :param max_mss: Maximum MSS value to test.
    :param step: Step size for MSS increment.
    :return: The highest MSS value that works.
    """
    conf.verb = 0  # Disable verbose output from Scapy
    best_mss = None

    print(f"Testing MSS values for {target_ip}:{target_port}...")

    for mss in range(min_mss, max_mss + 1, step):
        options = [('MSS', mss), ('NOP', None), ('NOP', None), ('WScale', 0)]
        packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S", options=options)

        response = sr1(packet, timeout=1)
        if response and response.haslayer(TCP) and response[TCP].flags == "SA":
            print(f"Success: MSS {mss} is supported.")
            best_mss = mss
        else:
            print(f"Failed: MSS {mss} is not supported.")

    if best_mss:
        print(f"\nBest MSS value: {best_mss} bytes.")
    else:
        print("\nNo valid MSS values found. Check your network configuration.")

    return best_mss


def main():
    print("TCP MSS Optimization Script")
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port (e.g., 80 for HTTP): "))

    best_mss = find_best_mss(target_ip, target_port)
    if best_mss:
        print(f"\nRecommended TCP MSS: {best_mss} bytes.")
    else:
        print("Could not determine a valid MSS. Please verify your network settings.")


if __name__ == "__main__":
    main()
