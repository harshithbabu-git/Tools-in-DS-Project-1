import requests
import csv

token = "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"

city = "Basel" 
followers = 10 

url = f"https://api.github.com/search/users?q=location:{city}+followers:>{followers}"
headers = {"Authorization": f"token {token}"}

all_users = []
page = 1
per_page = 100  # Max results per page is 100

while True:
    paginated_url = f"{url}&page={page}&per_page={per_page}"
    response = requests.get(paginated_url, headers=headers)

    if response.status_code == 200:
        users_data = response.json()
        all_users.extend(users_data['items'])
        # Break the loop if there are no more users
        if len(users_data['items']) < per_page:
            break
        page += 1  # Move to the next page
    else:
        print("Error fetching data:", response.status_code)
        break

print(f"Total users fetched: {len(all_users)}")

with open("users.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])
    
    for user in all_users:
        # Get detailed user information
        user_info = requests.get(user['url'], headers=headers).json()
        
        # Clean up the company name, defaulting to an empty string if None
        company = user_info.get('company')
        company = company.strip().lstrip('@').upper() if company else ""

        # Write to CSV
        writer.writerow([
            user_info['login'],
            user_info['name'],
            company,
            user_info['location'],
            user_info.get('email', ""),
            user_info['hireable'],
            user_info['bio'],
            user_info['public_repos'],
            user_info['followers'],
            user_info['following'],
            user_info['created_at']
        ])

with open("repositories.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"])
    
    for user in all_users:
        repos_url = user['repos_url']
        repos_response = requests.get(repos_url, headers=headers)
        
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            for repo in repos_data:
                writer.writerow([
                    user['login'],
                    repo['full_name'],
                    repo['created_at'],
                    repo['stargazers_count'],
                    repo['watchers_count'],
                    repo['language'],
                    repo['has_projects'],
                    repo['has_wiki'],
                    repo['license']['name'] if repo.get('license') else ""
                ])
