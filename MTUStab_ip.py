from scapy.all import IP, ICMP, sr1, conf
import ipaddress


def check_mtu(host, max_size=1500, step=10):
    conf.verb = 0  # Disable Scapy verbosity
    print(f"Testing MTU to host: {host}")

    for size in range(max_size, 0, -step):
        ip_packet = IP(dst=host, flags="DF") / ICMP() / ("X" * size)
        response = sr1(ip_packet, timeout=1, verbose=0)

        if response:
            print(f"Success: MTU of {size + 28} bytes supported (including headers).")
            return size + 28  # Include IP/ICMP header size
        else:
            print(f"Packet size {size} failed.")

    print("No valid MTU size found.")
    return None


def test_range(ip_range):
    """
    Test a range of IP addresses for MTU.
    """
    for ip in ipaddress.IPv4Network(ip_range, strict=False):
        print(f"\nTesting IP: {ip}")
        mtu = check_mtu(str(ip))
        if mtu:
            print(f"IP {ip}: Recommended MTU: {mtu} bytes.")
        else:
            print(f"IP {ip}: No valid MTU found.")


def main():
    print("MTU Testing Script")
    choice = input("Test single IP or range? (single/range): ").strip().lower()

    if choice == "single":
        host = input("Enter the destination host (IP or hostname): ")
        mtu = check_mtu(host)
        if mtu:
            print(f"\nRecommended MTU: {mtu} bytes.")
        else:
            print("\nCould not determine a valid MTU size.")

    elif choice == "range":
        ip_range = input("Enter the IP range (CIDR notation, e.g., 192.168.1.0/24): ")
        test_range(ip_range)
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
