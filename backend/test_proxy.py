import requests

def test_proxy_connection():
    proxies = {
        "http": "http://gate.decodo.com:10001",
        "https": "https://gate.decodo.com:10001"
    }
    try:
        response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
        assert response.status_code == 200
        assert "origin" in response.json()
    except Exception as e:
        print("Proxy test failed:", e)
        assert False, f"Proxy test failed: {e}"

if __name__ == "__main__":
    test_proxy_connection()