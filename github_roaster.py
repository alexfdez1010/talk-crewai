from datetime import datetime
from typing import Any, Dict, List

import requests
import streamlit as st
from crewai import Agent, Crew, Flow, Task
from crewai.flow import and_, listen, start
from pydantic import BaseModel, Field

# Set page config
st.set_page_config(
    page_title="GitHub Roaster",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# GitHub API Tools
class GitHubUserInfo(BaseModel):
    """Model for GitHub user information"""

    username: str = Field(description="GitHub username")
    name: str = Field(description="User's full name")
    bio: str = Field(description="User's bio")
    followers: int = Field(description="Number of followers")
    following: int = Field(description="Number of users following")
    public_repos: int = Field(description="Number of public repositories")
    location: str = Field(description="User's location")
    company: str = Field(description="User's company")
    blog: str = Field(description="User's blog or website")
    created_at: str = Field(description="Account creation date")
    avatar_url: str = Field(description="URL to user's avatar")


class GitHubRepoInfo(BaseModel):
    """Model for GitHub repository information"""

    name: str = Field(description="Repository name")
    description: str = Field(description="Repository description")
    language: str = Field(description="Primary language used")
    stars: int = Field(description="Number of stars")
    forks: int = Field(description="Number of forks")
    issues: int = Field(description="Number of open issues")
    created_at: str = Field(description="Repository creation date")
    updated_at: str = Field(description="Last update date")
    topics: List[str] = Field(description="Repository topics/tags")
    is_fork: bool = Field(description="Whether the repository is a fork")


def get_github_user_info(username: str) -> Dict[str, Any] | None:
    """Fetch GitHub user information"""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "username": data.get("login"),
        "name": data.get("name") or "Not provided",
        "bio": data.get("bio") or "No bio provided",
        "followers": data.get("followers", 0),
        "following": data.get("following", 0),
        "public_repos": data.get("public_repos", 0),
        "location": data.get("location") or "Not provided",
        "company": data.get("company") or "Not provided",
        "blog": data.get("blog") or "Not provided",
        "created_at": data.get("created_at"),
        "avatar_url": data.get("avatar_url"),
    }


def get_github_repos(username: str) -> List[Dict[str, Any]] | None:
    """Fetch GitHub repositories for a user"""
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    repos = response.json()

    return [
        {
            "name": repo.get("name"),
            "description": repo.get("description") or "No description provided",
            "language": repo.get("language") or "Not specified",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "issues": repo.get("open_issues_count", 0),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "topics": repo.get("topics", []),
            "is_fork": repo.get("fork", False),
        }
        for repo in repos
    ]


# CrewAI Agents and Flow
class GitHubRoasterFlow(Flow):
    """Flow for roasting a GitHub profile"""

    @start()
    def start_user_info(self):
        """Start the roasting process by gathering GitHub user data"""
        username = self.state["username"]
        user_info = get_github_user_info(username)

        # Check if there was an error
        if not user_info:
            return {"error": "Failed to fetch user data"}

        # Store data in state
        self.state["user_info"] = user_info

        # Trigger data analysis
        return user_info

    @start()
    def start_repo_info(self):
        """Start the roasting process by gathering GitHub repositories data"""
        username = self.state["username"]
        repos = get_github_repos(username)

        # Check if there was an error
        if not repos:
            return {"error": "Failed to fetch repositories data"}

        # Put repos information into a readable format
        repos = "\n\n".join(
            [
                f"""
                - Name: {repo['name']}
                - Description: {repo['description']}
                - Language: {repo['language']}
                - Stars: {repo['stars']}
                - Forks: {repo['forks']}
                - Created At: {repo['created_at']}
                - Updated At: {repo['updated_at']}
                - Topics: {repo['topics']}
                - Is Fork: {repo['is_fork']}
                """
                for repo in repos
            ]
        )

        # Store data in state
        self.state["repos"] = repos

        # Trigger data analysis
        return repos

    @listen(and_(start_user_info, start_repo_info))
    def generate_roast(self):
        """Generate a humorous roast based on the GitHub profile analysis"""
        if not self.state.get("user_info") or not self.state.get("repos"):
            return None

        # Create data analyst agent
        data_analyst = Agent(
            role="GitHub Data Analyst",
            goal="Analyze GitHub profiles to find patterns and interesting insights",
            backstory="""You are an expert at analyzing GitHub profiles and repositories.
            You can spot patterns, identify strengths and weaknesses, and understand what
            makes a developer tick just by looking at their GitHub activity.""",
            llm="gemini/gemini-2.0-flash",
            verbose=True,
        )

        # Create analysis task
        analysis_task = Task(
            description="""
            Current date: {date}
            Analyze the GitHub profile and repositories of user {username}.
            
            User Profile Information:
            {user_info}
            
            Repositories Information:
            {repos}  
            
            Identify patterns in:
            1. Programming languages used
            2. Types of projects created
            3. Commit frequency and activity patterns
            4. Code quality indicators
            5. Project originality vs. forks
            6. Documentation practices
            
            Provide a detailed analysis that can be used for creating a humorous roast.
            Focus on both strengths that can be exaggerated and weaknesses that can be playfully mocked.
            """,
            agent=data_analyst,
            expected_output="A detailed analysis of the GitHub profile with roastable insights",
        )

        # Create comedian agent
        comedian = Agent(
            role="Tech Comedian",
            goal="Create hilarious but insightful roasts of developers based on their GitHub profiles",
            backstory="""
            You are a brilliant tech comedian who specializes in roasting developers.
            You understand programming culture deeply and can craft witty, incisive jokes that
            highlight the quirks and patterns in someone's coding style and GitHub presence.
            Your roasts are funny but never cruel - they contain genuine insights wrapped in humor.
            """,
            llm="gemini/gemini-2.0-flash",
            verbose=True,
        )

        # Create roast task
        roast_task = Task(
            description="""
            Current date: {date}
            Create a hilarious but insightful roast of GitHub user {username} based on their profile.
            
            User Profile Information:
            {user_info}
            
            The roast should:
            1. Be structured with an introduction, 3-5 specific roasts, and a conclusion
            2. Include jokes about their programming languages, project choices, and coding patterns
            3. Contain tech humor that developers would appreciate
            4. Include some backhanded compliments that recognize their strengths
            5. Be funny but not mean-spirited or offensive
            6. Include a lot of emojis and formatting to make it visually engaging
            
            Format the roast as a comedy routine with clear sections and punchlines.
            It must be long with around 1000 words.
            """,
            agent=comedian,
            expected_output="A hilarious, well-structured roast of the GitHub profile",
        )

        crew = Crew(
            tasks=[analysis_task, roast_task],
            agents=[data_analyst, comedian],
            verbose=True,
        )

        # Execute the task
        roast = crew.kickoff(
            inputs={
                "username": self.state["username"],
                "repos": self.state["repos"],
                "user_info": self.state["user_info"],
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )

        return self.state["user_info"], roast


# Streamlit UI
def main():
    """
    Streamlit UI for roasting GitHub profiles
    """
    st.title("🔥 GitHub Profile Roaster 🔥")
    st.markdown(
        """
    Enter a GitHub username below to get a humorous, AI-generated roast of their profile.
    The roast is based on their public repositories, contribution patterns, and coding style.
    """
    )

    # Input for GitHub username
    username = st.text_input("GitHub Username to Roast", placeholder="octocat")

    if st.button("Roast This Profile! 🔥"):
        if not username:
            st.error("Please enter a GitHub username")
            return

        with st.spinner(
            f"Analyzing {username}'s GitHub profile... This might take a minute or two."
        ):
            # Create and run the flow
            flow = GitHubRoasterFlow()
            result = flow.kickoff(
                inputs={
                    "username": username,
                }
            )

            if not result:
                st.error("The username provided does not exist.")
                return

            user_info, roast = result

            # Display user info
            st.markdown("## GitHub Profile")
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(user_info["avatar_url"], width=200)

            with col2:
                st.markdown(
                    f"""
                    ### {user_info['name']} (@{user_info['username']})
                    - **Bio:** {user_info['bio']}
                    - **Location:** {user_info['location']}
                    - **Public Repos:** {user_info['public_repos']}
                    - **GitHub member since:** {user_info['created_at'][:10]}
                    """
                )

            # Display the roast
            st.markdown("## The Roast 🔥")
            st.markdown(roast)


if __name__ == "__main__":
    main()
