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
    
    # Read existing README content
    try:
        with open('README.md', 'r') as f:
            current_content = f.read()
    except FileNotFoundError:
        current_content = '# Hi there 👋\n\n'
    
    # Create repositories section
    repos_section = '## My Latest Repositories\n\n'
    
    # Add the 5 most recent repositories
    for repo in repos[:5]:
        name = repo['name']
        description = repo['description'] or 'No description available'
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        
        repos_section += f"### [{name}]({repo['html_url']})\n"
        repos_section += f"{description}\n"
        repos_section += f"⭐ Stars: {stars} | 🍴 Forks: {forks}\n\n"
    
    repos_section += f"\n*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC*\n"
    
    # Replace the repositories section in the current content
    import re
    pattern = r'## My Latest Repositories.*?(?=\n## |$)'
    if '## My Latest Repositories' in current_content:
        updated_content = re.sub(pattern, repos_section.strip(), current_content, flags=re.DOTALL)
    else:
        # If section doesn't exist, add it before the first ## or at the end
        if '##' in current_content:
            updated_content = re.sub(r'(##.*?)', f'{repos_section}\n\n\1', current_content, count=1)
        else:
            updated_content = current_content.rstrip() + '\n\n' + repos_section
    
    # Write updated content back to README.md
    with open('README.md', 'w') as f:
        f.write(updated_content)

if __name__ == '__main__':
    update_readme()
