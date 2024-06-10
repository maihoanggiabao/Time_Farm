import requests
import time
import json
import random
import brotli
import schedule
import time

# Function to send HTTP request
def send_request(url, headers, method='GET', params=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print(f"Error during request: {e}")
        return None

# Function to process token and send request
def process_tokens(token, url, method='GET', index=None):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        'Authorization': f'Bearer {token}',
        "If-None-Match": 'W/"1f-ouhhUVclchn5/eA42dEj1B9830E"',
        "Origin": "https://tg-tap-miniapp.laborx.io",
        "Referer": "https://tg-tap-miniapp.laborx.io/",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    data = send_request(url, headers, method)
    if index is not None:
        print(f"TimeFarm {index}: {data}")
    else:
        print(f"Response: {data}")

def process_response(response):
    if response.headers.get('Content-Encoding') == 'br':
        decompressed_data = brotli.decompress(response.content)
        return decompressed_data.decode('utf-8')
    else:
        return response.text

# Function to get new token from refresh token
def get_new_tokens(refresh_token):
    url = "https://tg-bot-tap.laborx.io/api/v1/auth/validate-init"
    
    # The payload you have
    payload = refresh_token
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Origin": "https://tg-tap-miniapp.laborx.io"
    }
    
    # Send the POST request
    response = requests.post(url, data=payload, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            # Parse the JSON response
            response_data = response.json()
            # Check if 'token' is in the response
            if 'token' in response_data:
                return response_data['token']
        except ValueError:
            print("Failed to parse JSON response")
    else:
        print(f"Error {response.status_code}: {response.text}")
    
    print("Failed to get new tokens")
    return None

# Function to check remaining claim time
def check_claim_time(headers, url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "nextClaimTime" in data:
            next_claim_time = data["nextClaimTime"]
            current_time = time.time()
            remaining_time = next_claim_time - current_time
            return max(0, remaining_time)
    return None

# Main function
def main():
    run_once = True
    # Prompt user for enabling auto play and auto task completion
    while run_once:
        try:
            try:
                with open('tokens_timefarm.txt', 'r') as file:
                    refresh_tokens = [line.strip() for line in file if line.strip()]
                    if not refresh_tokens:
                        continue
            except:
                print(f"Error in here")
            for index, refresh_token in enumerate(refresh_tokens, start=0):
                try:
                    access_token = get_new_tokens(refresh_token)
                except:
                    print(f"Error in here")
                if not access_token:
                    continue

                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
                    'Authorization': f'Bearer {access_token}',
                    "If-None-Match": 'W/"1f-ouhhUVclchn5/eA42dEj1B9830E"',
                    "Origin": "https://tg-tap-miniapp.laborx.io",
                    "Referer": "https://tg-tap-miniapp.laborx.io/",
                    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                }

                laborx_balance = 'https://tg-bot-tap.laborx.io/api/v1/balance'
                laborx_claim_url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
                laborx_farming_url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
                #daily_reward_url = 'https://game-domain.laborx.io/api/v1/daily-reward'
                #daily_reward = "https://game-domain.laborx.io/api/v1/daily-reward?offset=-420"
                tasks_url = "https://tg-bot-tap.laborx.io/api/v1/tasks"


                #response = requests.get(daily_reward_url, headers=headers, params=params)
                #if response.status_code == 200:
                   #response = requests.post(daily_reward, headers=headers)
                    #print(f'TimeFarm {index} Daily check-in successful')
                #else:
                    #pass

                response_balance = send_request(laborx_balance, headers=headers)

                # Check balance and farming status
                if 'balance' in response_balance:
                    available_balance = response_balance['balance']
                    print(f"TimeFarm {index} - Balance: {available_balance}")                                
                try: 
                    try:
                        process_tokens(access_token, laborx_claim_url, method='POST', index=index)
                        process_tokens(access_token, laborx_farming_url, method='POST', index=index)
                    except:
                        process_tokens(access_token, laborx_farming_url, method='POST', index=index)
                except Exception as e:
                    print(f"Error: {e}")
                

                try:
                    tasks = requests.get(tasks_url, headers=headers)
                    tasklist = json.loads(tasks.text)

                    if tasklist:
                        try:
                            for task in tasklist:
                                task_id = task["id"]
                                title = task["title"]
                                reward = task["reward"]
                                if "submission" not in task or task["submission"]["status"] == "COMPLETED" or task["submission"]["status"] == "REJECTED":
                                    if task_id in ["666414ff5e7893dd79f8b97a", "666318485e7893dd79f8b978", "665dd515a34653000747c2c7", "665dd51ea34653000747c2c8", "665dd526a34653000747c2c9", "665dd530a34653000747c2ca", "665dd53ca34653000747c2cb", "665dd547a34653000747c2cc", "665dd551a34653000747c2cd"]:
                                        task_start_url = f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions"
                                        response_start = requests.post(task_start_url, headers=headers)
                                        print(f"Task {title} starting")
                                        task_claim_url = f"https://tg-bot-tap.laborx.io/api/v1/tasks/665dd51ea34653000747c2c8/{task_id}"
                                        response_claim = requests.post(task_claim_url, headers=headers)
                                        print(f"Task {title} ready to claim: {reward}")
                                        task_claim_url = f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims"
                                        response_claim = requests.post(task_claim_url, headers=headers)
                                        print(f"Task {title} claimed: {reward}")
                                    else:
                                        pass
                                    
                                else:
                                    pass

                        except Exception as e:
                            print(f"Error: {e}")
                except requests.RequestException as e:
                    print(f"An error occurred: {e}")
                except:
                    pass

                print('-' * 50)
            print('=' * 50)

        except Exception as e:
            print(f"Error: {e}")

        run_once = False 

#if __name__ == "__main__":
#    main()

def run_main():
    main()
    print("Waiting for the next run...")
    # Schedule main to run every 2 minutes
    schedule.every(5).minutes.do(run_main)

if __name__ == "__main__":
    # Run main immediately
    run_main()

while True:
    schedule.run_pending()
    time.sleep(1)