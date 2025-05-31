import os
import requests
from datetime import datetime

def get_user_repos():
    github_token = os.environ.get('TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    username = 'anandan-bs'  # Your GitHub username
    repos = []
    page = 1
    
    while True:
        response = requests.get(
            f'https://api.github.com/users/{username}/repos',
            headers=headers,
            params={'page': page, 'per_page': 100}
        )
        if response.status_code != 200:
            break
        
        page_repos = response.json()
        if not page_repos:
            break
            
        repos.extend(page_repos)
        page += 1
    
    return repos

def update_readme():
    repos = get_user_repos()
    
    # Sort repositories by creation date (newest first)
    repos.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Create README content
    readme_content = """# Hi there 👋

## My Latest Repositories

"""
    
    # Add the 5 most recent repositories
    for repo in repos[:5]:
        name = repo['name']
        description = repo['description'] or 'No description available'
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        
        readme_content += f"### [{name}]({repo['html_url']})\n"
        readme_content += f"{description}\n"
        readme_content += f"⭐ Stars: {stars} | 🍴 Forks: {forks}\n\n"
    
    # Add timestamp
    readme_content += f"\n*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC*"
    
    # Write to README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)

if __name__ == '__main__':
    update_readme()
