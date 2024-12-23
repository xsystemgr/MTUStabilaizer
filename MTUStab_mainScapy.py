import requests
import os


def check_service_mtu(url, max_size=1500, step=10):
    print(f"Testing MTU to service: {url}")

    for size in range(max_size, 0, -step):
        headers = {"Custom-Header": "X" * size}  # Προσθέτουμε μεγάλο header
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"Success: Service responded with MTU of {size} bytes.")
                return size
        except requests.exceptions.RequestException as e:
            print(f"Request with size {size} failed: {e}")

    print("No valid MTU size found for the service.")
    return None


def test_services(service_list):
    """
    Test a list of WCF services for MTU.
    """
    for service in service_list:
        print(f"\nTesting service: {service}")
        mtu = check_service_mtu(service)
        if mtu:
            print(f"Service {service}: Recommended MTU: {mtu} bytes.")
        else:
            print(f"Service {service}: No valid MTU found.")


def main():
    print("MTU Testing Script for WCF Services")

    # Έλεγχος αν υπάρχει το αρχείο urls.txt
    if os.path.exists("urls.txt"):
        print("Reading URLs from urls.txt...")
        with open("urls.txt", "r") as file:
            service_list = [line.strip() for line in file if line.strip()]
    else:
        # Ζητά URLs αν δεν υπάρχει το αρχείο
        service_list = input("Enter a comma-separated list of service URLs: ").split(",")
        service_list = [url.strip() for url in service_list]

    if not service_list:
        print("No URLs provided. Exiting.")
        return

    test_services(service_list)


if __name__ == "__main__":
    main()
