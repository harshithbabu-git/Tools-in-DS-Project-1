import requests
import csv


token = "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"  

city = "Basel" 
followers = 10

url = f"https://api.github.com/search/users?q=location:{city}+followers:>{followers}"
headers = {"Authorization": f"token {token}"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    users_data = response.json()
else:
    print("Error fetching data:", response.status_code)

with open("users.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])
    
    for user in users_data['items']:
        # Get detailed user information
        user_info = requests.get(user['url'], headers=headers).json()
        
        # Clean up the company name
        company = user_info['company'].strip().lstrip('@').upper() if user_info['company'] else ""
        
        # Write to CSV
        writer.writerow([
            user_info['login'],
            user_info['name'],
            company,
            user_info['location'],
            user_info['email'] if 'email' in user_info else "",
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
    
    for user in users_data['items']:
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
