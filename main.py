from urllib.parse import urlparse
import requests
import random
import concurrent.futures
import json
import os
import argparse
from colorama import Fore, Style
import functools
import time
import shutil
import tempfile

def create_temp_hidden_dir():
    # Get the current working directory
    current_dir = os.getcwd()

    # Create a temporary directory with a unique name
    temp_dir = tempfile.mkdtemp(dir=current_dir)

    # Make the temporary directory hidden by adding a dot prefix
    hidden_temp_dir = os.path.join(current_dir, '.' + os.path.basename(temp_dir))

    # Rename the temporary directory to make it hidden
    os.rename(temp_dir, hidden_temp_dir)

    return hidden_temp_dir
def delete_temp_hidden_dir(dir_path):
    try:
        # Remove the directory and its contents
        shutil.rmtree(dir_path)
        print(f"Temporary hidden directory deleted: {dir_path}")
    except FileNotFoundError:
        print(f"Directory not found: {dir_path}")
    except Exception as e:
        print(f"Error deleting directory {dir_path}: {e}")

def extract_username_from_url(url):
    try:
        parsed_url = urlparse(url)
        # Split the path and get the last component as the username
        username = parsed_url.path.split('/')[-1]
        return username
    except Exception as ex:
        print(f"An error occurred while extracting username: {ex}")
        return None

def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        return urls
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# def make_request(url, headers=None, params=None):
#     try:
#         response = requests.get(url, headers=headers, params=params)
#         status_code = response.status_code
#         response_text = response.text
#         return status_code, response_text
#     except requests.RequestException as e:
#         # Handle exceptions, you can modify this part based on your needs
#         print(f"Request failed with error: {e}")
#         return None, None

def make_request(url, headers=None, params=None):
    try:
        proxy_with_auth = {
            'http': 'http://gazfQIdkP5Nj1DNV:KfWUfWjHQ0lzPFrn@geo.iproyal.com:12321',
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxy_with_auth)
        status_code = response.status_code
        response_text = response.text
        return status_code, response_text
    except requests.RequestException as e:
        # Handle exceptions, you can modify this part based on your needs
        print(f"Request failed with error: {e}")
        return None, None
def check_file_in_directory(username):
    current_dir = os.getcwd()  
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                if username in file:
                    return True, file_path  

    return False, None

# Read user agents from file
def read_user_agents(file_path='user_agents.txt'):
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file.readlines()]
        return user_agents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def save_list_to_file(my_list, file_path):
    try:
        with open(file_path, 'w') as file:
            for item in my_list:
                file.write(str(item) + '\n')
        print("List successfully saved to", file_path)
    except Exception as e:
        print("Error:", e)

def generate_random_headers(user_agents):
    try:
        # Randomly choose a user agent
        user_agent = random.choice(user_agents)

        # Create headers with the chosen user agent
        headers = {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

      

        return headers

    except IndexError:
        print("Empty list of user agents.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 
    

def process_response(response_text,url=None):
    try:

        # print(response_text)
        
        
        # Find the position where the JSON starts
        start_index = response_text.find('{"seller":')

        # Check if the starting position is found
        if start_index != -1:

            # Extract the substring starting from the found position
            json_data_string = response_text[start_index:]

            # Find the outermost JSON object
            stack = []
            end_index = None

            for i, char in enumerate(json_data_string):
                if char == '{':
                    stack.append(i)
                elif char == '}':
                    stack.pop()
                    if not stack:
                        end_index = i
                        break

            if end_index is not None:
                json_data_string = json_data_string[:end_index + 1]

                # Load the JSON data
                try:
                    json_data = json.loads(json_data_string)
                    
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            else:
                print("End of outermost JSON object not found.")
        else:
            print(f"JSON starting point not found for: {url}")
           
    except Exception as ex:
        print(f"An error occurred in response: {ex}")

def validate_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        print(f"Error: {file_path} does not exist.")
        return


def process_url(url,dir_path=None):
    try:
        
        print(f"\nProcessing URL: {Fore.BLUE}{url}{Style.RESET_ALL}")
        username = extract_username_from_url(url=url)
        is_exist,file_path=check_file_in_directory(username=username)
        
        if not is_exist:
            
            headers = generate_random_headers(user_agents=user_agents)
            status_code, response_text = make_request(url=url, headers=headers)

            if status_code < 400:
                json_data = process_response(response_text=response_text,url=url)

                if json_data:
                    file_name=f"{json_data['seller']['user']['name']}.json"
                    with open(f"{dir_path}/{file_name}", 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

            else:
                print(f"Failed to fetch data from {Fore.RED}{url}{Style.RESET_ALL}. Status Code: {status_code}")

            time.sleep(1)  # Adjust sleep duration as needed
        else:
            print(f"{url} Already Scraped!")
            copy_file(file_path,dir_path)

    except Exception as e:
        print(f"Error processing URL {Fore.RED}{url}{Style.RESET_ALL}: {str(e)}")



def copy_files(source_dir, destination_dir):
    # Ensure that both source and destination directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(destination_dir):
        print(f"Destination directory '{destination_dir}' does not exist. Creating it.")
        os.makedirs(destination_dir)

    # Get all files in the source directory
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Copy each file to the destination directory, replacing if already exists
    for file in files:
        source_path = os.path.join(source_dir, file)
        destination_path = os.path.join(destination_dir, file)
        
        try:
            shutil.copy2(source_path, destination_path)
           
        except Exception as e:
            print(f"Error copying.")
    print(f"Files copied from {source_dir}  to {destination_dir}")


def get_json_files_in_directory(directory):
   
    try:
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        return json_files
    except Exception as ex:
        print(f"An error occurred while getting JSON files: {ex}")
        return None

def count_elements(lst):
    element_count = {}

    for element in lst:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1

    return element_count

def read_json_data(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except Exception as ex:
        print(f"Error in reading json data from: {file_name}: {ex}")


def find_common_elements(list_of_lists):
    element_count = {}
    common_elements = set()

    for sublist in list_of_lists:
        unique_elements = set(sublist)

        for element in unique_elements:
            element_count[element] = element_count.get(element, 0) + 1

            # If an element is found in more than two sublists, add it to common_elements
            if element_count[element] > 1:
                common_elements.add(element)

    return list(common_elements)



def copy_file(source_path, destination_dir):
    # Ensure that the source file exists
    if not os.path.exists(source_path):
        print(f"Source file '{source_path}' does not exist.")
        return

    # Ensure that the destination directory exists
    if not os.path.exists(destination_dir):
        print(f"Destination directory '{destination_dir}' does not exist. Creating it.")
        os.makedirs(destination_dir)

    # Extract the file name from the source path
    file_name = os.path.basename(source_path)

    # Construct the destination path
    destination_path = os.path.join(destination_dir, file_name)

    # Check if source and destination paths are the same
    if os.path.abspath(source_path) == os.path.abspath(destination_path):
        
        return

    try:
        shutil.copy2(source_path, destination_path)
        

    except Exception as e:
        print(f"Error copying '{file_name}': {e}")

            
def print_elements_with_count_greater_than_two(lst):
    element_count = count_elements(lst)

    for element, count in element_count.items():
        if count >= 2:
            print(f"{element}")


def main():
    parser = argparse.ArgumentParser(description="Script to process fake and profiles options.")
    parser.add_argument('--get-reviewers', action='store', help='Specify the url')
    parser.add_argument('--get-profiles', action='store', metavar='profiles_file', help='Specify profiles file')
    parser.add_argument('--get-fake', action='store', metavar='fake profiles_file', help='Specify profiles file')
    parser.add_argument('-w', '--workers', type=int, default=5, help='Number of workers (default: 5)')

    
    args = parser.parse_args()
    num_workers=args.workers

    if not args.get_fake and not args.get_profiles:
        print("Error: At least one of --get-fake or --get-profiles should be present.")
        return
    
    
    if args.get_fake:
        temp_dir_path = create_temp_hidden_dir()
        print(f"Temporary hidden directory created: {temp_dir_path}")
        profiles_file_path = args.get_fake
        file_exist=validate_file(profiles_file_path)
        if file_exist:
            urls=read_urls_from_file(profiles_file_path)
            urls=list(set(urls))
            print(f"total urls:{len(urls)}")
            for url in urls:
                process_url(url,temp_dir_path)
            # process_url_partial = functools.partial(process_url, dir_path=temp_dir_path)

            # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            #     executor.map(process_url_partial, urls)

                tmp_urls=[]
                username=extract_username_from_url(url)
                is_exist,file_path=check_file_in_directory(username=username)
                if is_exist:
                    username_json_result=read_json_data(file_path)
                    if username_json_result:
                        temp_reviews=username_json_result['reviewsData']['selling_reviews']['reviews']
                        for review in temp_reviews:
                            username=review['username']
                            tmp_url=f"https://www.fiverr.com/{username}"
                            tmp_urls.append(tmp_url)
                
                print(f"Found {len(tmp_urls)} Buying links from: {url}")
                print(tmp_urls)
                process_url_partial = functools.partial(process_url, dir_path=temp_dir_path)

                with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                    executor.map(process_url_partial, tmp_urls)
            
            fake_lists=[]
            
            json_files=get_json_files_in_directory(temp_dir_path)
            
            for file in  json_files:
                buying_urls=[]
                json_data=read_json_data(f"{temp_dir_path}/{file}")
                if json_data:
                    
                    buying_reviews=json_data['reviewsData']['buying_reviews']['reviews']
                    
                   
                    for review in buying_reviews:            
                        username=review['username']
                        url=f"https://www.fiverr.com/{username}"          
                        buying_urls.append(url)

                    fake_lists.append(buying_urls)
                    print(f"Selling links for {file}:\n{buying_urls}")
                    print("----------------------")
            fake_links=find_common_elements(fake_lists)
            for url in urls:
                fake_links.append(url)
            print(f"Common links:\n{fake_links}")
            fake_links=list(set(fake_links))
            print(len(fake_links))
            save_list_to_file(fake_links,"fake_links.txt")
            copy_files(temp_dir_path,"results")
            delete_temp_hidden_dir(temp_dir_path)

            
   

    if args.get_profiles:
        profiles_file_path = args.get_profiles
        file_exist=validate_file(profiles_file_path)
        if file_exist:
            urls=read_urls_from_file(profiles_file_path)
            
            process_url_partial = functools.partial(process_url, original=True)

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                executor.map(process_url_partial, urls)
if __name__=="__main__":
    user_agents = read_user_agents()
    main()