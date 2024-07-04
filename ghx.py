import requests
import json
import time
import threading
import math

api_url = "https://api.gamerhash.com"
headers = {
  'Accept': 'application/json',
  'X-GamerHashAI-Version': '0.6.19',
  'User-Agent': 'GamerHashAI/0.6.19',
  'X-GamerHashAI-User': 'MikoPlayGames1',
  'X-GamerHashAI-Hash': '6CF198ADE1822ED901F04B6A3E03B25A',
  'Authorization': 'Bearer 81778|3MetFNXlnOVy9XOSkfd3Fbr03mglAcLnn3otTxLq',
  'Content-Type': 'application/json'
}

def send_update():
    try:
        url = api_url + "/api/v2/update"
        payload = "lang=en"
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Sent update request")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def send_me():
    try:
        url = api_url + "/api/v2/me/info"
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Sent me request")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def send_userinfo():
    url = api_url + "/api/v2/ai/userinfo"
    payload = {}
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = response.json()  # Parse the response as JSON
            total_points = response_json['data']['total']  # Access the "total" field
            print(f"Current points total: {total_points}")
            discord_webhook_url = "https://discord.com/api/webhooks/1042550561523904573/tE73oxjkCe3HGp8KQJ2rSvbwkpljH0Pojnm0EMxrvZ207aK5WsdPsKo66A62pon4HTjP"
            discord_message = {
                "content": f"Current points total: ``{total_points}``"
            }
            requests.post(discord_webhook_url, json=discord_message)
            break  # If the request is successful, break the loop
        except Exception as e:
            print(f"Wystąpił błąd: {e}. Ponawiam próbę.")


payload = json.dumps({
  "action": "bump",
  "valid": {
    "hard": {
      "cpu": "AMD Ryzen Threadripper 3990X",
      "ram": 130.44,
      "cores": 64,
      "storage": 742.9000000000001,
      "gpus": [
        {
          "model": "NVIDIA RTX A6000",
          "vendev": "VEN_10DE&DEV_2882",
          "vram": 49.13
        }
      ],
      "bip": "31bff9dcf2c7088c352c0bcc7b59aa271994782b6d91a1f3b60b2cd0b4383454"
    },
    "soft": {
      "resolution": "1920x1080",
      "hostname": "bdf8745f7d33fd5024e9ccf315270be6578663fe4b135d4ee344f0f9512d23cb",
      "username": "c49d9f13a6cc0b8686401777fb98d44fb406f430ebb854cd823d5342ed67020b",
      "id": "6CF198ADE1822ED901F04B6A3E03B25A",
      "os": "Microsoft Windows NT 10.0.22631.0",
      "uuid": "4a497fceba1774add89687b8f6236657b955df15d7f9c023bc7d12cbc7ce7d61",
      "guid": "1e85c81ca990b4411bad03a48ce5de601aa16fb7df06961c49e9d6b5cd209a4a",
      "version": "0.6.19",
      "uniq": "7a595b0aae8e42ecafe81be344a6a7bf5157b379f1fafd545e521b204556f3d2",
      "bip": "0c17d0ab9ab67031541651f6adaca386d7b9aa8291f9ab132b62ad1e6cfa4bb7"
    }
  }
})

max_vram = 48
max_ram = 32
max_cores = 2
max_storage = 1000

def get_ghxp_rate(payload):
    vram = payload["valid"]["hard"]["gpus"][0]["vram"]
    ram = payload["valid"]["hard"]["ram"]
    cores = payload["valid"]["hard"]["cores"]
    storage = payload["valid"]["hard"]["storage"]

    vram = min(vram, max_vram)
    ram = min(ram, max_ram)
    cores = min(cores, max_cores)
    storage = min(storage, max_storage)

    ghxp_rate = vram * 1.5 + ram + math.sqrt(cores) + math.pow(storage, 1.0 / 3.0)
    return ghxp_rate

print(get_ghxp_rate(json.loads(payload)))


def send_activity_update():
    while True:
        try:
            url = api_url + "/api/v2/ai/activity"

            response = requests.request("POST", url, headers=headers, data=payload)
            print("Sent activity update request")
            discord_webhook_url = "https://discord.com/api/webhooks/1172953307602501652/gDymW5qu3YDGtc2u5zSX1s4HQl0CDBAtI6sSFqIZ5wweJRir5tG-GlI2jdthV17dzzTO"
            discord_message = {
                "content": f"Zaktualizowano saldo."
            }
            requests.post(discord_webhook_url, json=discord_message)

            response = requests.request("POST", url, headers=headers, data=payload)
            break  # If the request is successful, break the loop
        except Exception as e:
            print(f"Wystąpił błąd: {e}. Ponawiam próbę za minutę.")
            time.sleep(60)  # Wait for a minute before trying again

# Send the requests once at the start
send_update()
send_me()
send_userinfo()


start_time = time.time()

activity_send_minutes = 55

def send_activity_update_loop():
    while True:
        time.sleep(activity_send_minutes * 60)  # wait for activity_send_minutes minutes
        send_activity_update()
        print(f"Sent activity update request. Waiting for {activity_send_minutes} minutes...")

# Start the activity update loop in a separate thread
activity_update_thread = threading.Thread(target=send_activity_update_loop, daemon=True)
activity_update_thread.start()

counter = -1
while True:
    elapsed_time = time.time() - start_time
    if elapsed_time > 300:  # 300 seconds = 5 minutes
        send_userinfo()
        if counter % 2 == 0 and counter != -1:  # if counter is even and not the first iteration
            send_me()
        start_time = time.time()  # reset the timer
        counter += 1  # increment the counter
    time.sleep(1)  # wait for 1 second before checking the time again