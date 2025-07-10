import streamlit as st
from utils.auth import require_role


if require_role(["admin"]) and st.user.is_logged_in:
    st.error("UNAUTHORIZED ACCESS")
    st.stop()

notes1 = '''
Git Commands Used and Suggested
1. Checking Repository Status and History:


git status


Purpose: Shows the state of the working directory and the staging area. It tells you which changes have been staged, which haven't, and which files aren't being tracked by Git. Crucial for understanding merge conflicts.
When used: Frequently, to check progress during conflict resolution, merges, and rebases.
git log


Purpose: Displays the commit history.
When used: To see what commits are on your branch, what commits are on a remote branch, or to inspect the history of a specific file.
Common variations:
git log --oneline: Shows each commit on a single line (short hash, commit message).
git log --graph --decorate --oneline: Adds a text-based graphical representation of the commit history and shows branch/tag pointers.
git log <remote>/<branch>..HEAD: Shows commits that are on your current branch (HEAD) but not on the specified remote branch.
2. Managing Branches:


git checkout <branch_name>
Purpose: Switches to a different branch.
When used: To ensure you are on the correct branch before performing operations like merging, pulling, or pushing.
3. Resolving Merge Conflicts:


Manual Editing of Files


Purpose: To remove <<<<<<<, =======, >>>>>>> markers and choose the desired content from conflicting versions.
When used: After Git pauses a merge or rebase due to conflicts.
git add <file_name>


Purpose: Stages changes for the next commit. For conflict resolution, it tells Git that you have manually resolved the conflicts in that file.
When used: After manually editing a conflicted file.
Common variations:
git add .: Stages all changes (modifications, additions, deletions) in the current directory and its subdirectories. Highly recommended for staging multiple resolved conflict files.
git add -u or git add --update: Stages changes to tracked files (modifications and deletions), but not new untracked files.
git add <directory_path>/: Stages all changes within a specific directory.
git commit


Purpose: Records the staged changes as a new commit in the repository history.
When used:
To finalize a merge operation after resolving conflicts. Git will open an editor with a pre-filled merge commit message.
To finalize a rebase step after resolving conflicts (often followed by --continue).
4. Aborting Operations:


git merge --abort


Purpose: Stops the current merge process and resets the branch to its state before the merge attempt.
When used: If you decide not to proceed with a merge, or if you get stuck and want to start over.
git rebase --abort


Purpose: Stops the current rebase process and resets the branch to its state before the rebase attempt.
When used: If you decide not to proceed with a rebase, or if you get stuck and want to start over.
5. Integrating Remote Changes (Getting Updates):


git fetch origin


Purpose: Downloads new commits and branches from the remote repository (origin) to your local repository, but does not merge them into your current working branch. It updates your remote-tracking branches (e.g., origin/eCost_Aluminum5_migration_target).
When used: To see what's new on the remote without changing your local branch, or as a preparatory step before merging/rebasing.
git pull origin <remote_branch_name>


Purpose: A shortcut command that performs git fetch followed by git merge. It fetches changes from the specified remote branch and then merges them into your current local branch.
When used: The most common way to get updates from a remote branch.
Example: git pull origin eCost_Aluminum5_migration_target
git pull --rebase origin <remote_branch_name>


Purpose: Performs git fetch followed by git rebase. It fetches changes from the specified remote branch and then "replays" your local commits on top of the fetched changes, creating a linear history.
When used: When you prefer a clean, linear history without merge commits.
Caution: Can be more complex to resolve conflicts and should be used carefully on branches that others have already pulled.
git merge origin/<remote_branch_name>


Purpose: Merges the specified remote-tracking branch (which git fetch updates) into your current local branch. This is the merge step that git pull performs automatically.
When used: After git fetch if you want to explicitly control the merge, or if git pull is not desired.
Example: git merge origin/eCost_Aluminum5_migration_target
git rebase --continue


Purpose: Continues a rebase operation after you have resolved conflicts or made changes during an interactive rebase.
When used: After resolving conflicts during a git pull --rebase or git rebase command, and after staging the resolved files.
6. Sending Changes to Remote (Publishing):


git push origin <local_branch_name>
Purpose: Uploads your local commits to the specified remote branch.
When used: After your local branch is up-to-date with the remote and contains the changes you want to share.
Example: git push origin eCost_Aluminum5_migration_target
7. Advanced/Cautionary Commands:


git reset --hard <commit_hash>


Purpose: Moves the current branch pointer to the specified commit and discards all changes in the working directory and staging area that occurred after that commit. This is a destructive command.
When used: To completely undo local commits and changes, often to revert to a clean state. Use with extreme caution.
git push --force origin <branch_name> (or git push -f)


Purpose: Overwrites the remote branch with your local branch's history, even if the histories have diverged. This is a destructive command.
When used: Only when you are absolutely certain you want to discard the remote's history and replace it with yours (e.g., after a rebase on a branch that no one else has pulled). Avoid on shared branches
'''

notes2 = '''
I have this scenarion origin/eCost_Aluminum5_migration_target was created from origin/eCost_server_Code_Cleanup_bkp_CR
there was changes pushed in origin/eCost_server_Code_Cleanup_bkp_CR , from other branch (origin/Q2FY25_InfosecFix)
for which update was not taken in origin/eCost_Aluminum5_migration_target which is create from origin/eCost_server_Code_Cleanup_bkp_CR,
today i have create one pull request for merging from origin/eCost_Aluminum5_migr

Okay, this clarifies the situation significantly! It's a classic scenario of diverging branches and missed updates.

Let's break down the history you've described and then outline the solution.

### Understanding Your Git History

Based on your description, here's a simplified timeline/graph:

1.  **Initial State:**
    ```
    ... -- A -- B -- C (origin/eCost_server_Code_Cleanup_bkp_CR)
                     \
                      (origin/eCost_Aluminum5_migration_target was created here, so it's also at C initially)
    ```

2.  **Changes to `cleanup_bkp`:**
    Someone merged `origin/Q2FY25_InfosecFix` into `origin/eCost_server_Code_Cleanup_bkp_CR`.
    ```
    ... -- A -- B -- C -- F -- G (origin/eCost_server_Code_Cleanup_bkp_CR)
                     \         ^
                      \        | (commits from origin/Q2FY25_InfosecFix)
                       \
                        (origin/eCost_Aluminum5_migration_target is still conceptually at C, or at least doesn't have F, G)
    ```

3.  **Your Work on `eCost_Aluminum5_migration_target`:**
    You've been working on your local `eCost_Aluminum5_migration_target` branch, adding your own commits (let's call them D, E).
    ```
    ... -- A -- B -- C -- F -- G (origin/eCost_server_Code_Cleanup_bkp_CR)
                     \
                      D -- E (your local eCost_Aluminum5_migration_target)
    ```

4.  **The Problem (`non-fast-forward`):**
    When you tried to `git push` your `D` and `E` commits to `origin/eCost_Aluminum5_migration_target`, Git rejected it. This means that `origin/eCost_Aluminum5_migration_target` on the remote *also* moved forward, likely by receiving the `F` and `G` commits (or similar ones) from `eCost_server_Code_Cleanup_bkp_CR` or another source.

    So, the remote `origin/eCost_Aluminum5_migration_target` now looks like this:
    ```
    ... -- A -- B -- C -- F -- G (origin/eCost_server_Code_Cleanup_bkp_CR)
                     \
                      F -- G (origin/eCost_Aluminum5_migration_target on remote)
                     /
                    D -- E (your local eCost_Aluminum5_migration_target)
    ```
    Your local branch has `D` and `E`, but is missing `F` and `G`. The remote branch has `F` and `G`, but is missing `D` and `E`. Their histories have diverged.

5.  **Your Pull Request (PR):**
    You've created a PR *from* `origin/eCost_Aluminum5_migration_target`. This PR will likely show that `eCost_Aluminum5_migration_target` is both "ahead" (with D, E) and "behind" (missing F, G) the target branch of the PR (e.g., `main` or `cleanup_bkp`).

### The Solution: Integrate Remote Changes, Then Push

You need to bring the `F` and `G` commits (and any other new commits) from `origin/eCost_Aluminum5_migration_target` into your local `eCost_Aluminum5_migration_target` branch.

**Assumptions:**
*   You are currently on your local `eCost_Aluminum5_migration_target` branch. (You can check with `git branch`).
*   You have already resolved the initial merge conflict you mentioned and committed it.

**Steps to Resolve and Push:**

1.  **Ensure you're on the correct branch:**
    ```bash
    git checkout eCost_Aluminum5_migration_target
    ```

2.  **Fetch the latest state from the remote:**
    This updates your local knowledge of what's on `origin`.
    ```bash
    git fetch origin
    ```

3.  **Integrate the remote changes into your local branch:**
    This is the crucial step to resolve the `non-fast-forward` issue. You have two main options:

    *   **Option A: `git pull` (Merge) - Recommended for most cases**
        This will fetch the changes from `origin/eCost_Aluminum5_migration_target` and merge them into your local `eCost_Aluminum5_migration_target`. This creates a new merge commit.
        ```bash
        git pull origin eCost_Aluminum5_migration_target
        ```
        *   **What happens:** Git will try to merge `origin/eCost_Aluminum5_migration_target` (which has F, G) with your local `eCost_Aluminum5_migration_target` (which has D, E).
        *   **Potential Conflicts:** It's highly likely you will encounter *new* merge conflicts here. This happens if your `D` and `E` commits modified the same lines of code as the `F` and `G` commits.
        *   **If conflicts occur:**
            *   Git will pause and tell you there are conflicts.
            *   Run `git status` to see which files are conflicted.
            *   Manually edit each conflicted file to resolve the differences (remove `<<<<<<<`, `=======`, `>>>>>>>` markers).
            *   After resolving a file, `git add <file_name>`.
            *   Once all conflicts are resolved and staged, `git commit` to complete this merge.

    *   **Option B: `git pull --rebase` (Rebase) - For a cleaner history**
        This will fetch the changes from `origin/eCost_Aluminum5_migration_target` and then "replay" your local commits (`D`, `E`) on top of the remote's latest (`F`, `G`). This results in a linear history without an extra merge commit.
        ```bash
        git pull --rebase origin eCost_Aluminum5_migration_target
        ```
        *   **What happens:** Git will temporarily "undo" your `D` and `E` commits, apply `F` and `G`, and then re-apply `D` and `E` on top.
        *   **Potential Conflicts:** Conflicts can also occur during a rebase. If they do:
            *   Resolve the conflict in the file.
            *   `git add <file_name>`.
            *   `git rebase --continue`.
            *   Repeat until the rebase is complete.
            *   If you need to stop: `git rebase --abort`.
        *   **Caution:** Rebasing rewrites history. If anyone else has already pulled your `D` and `E` commits (unlikely if you couldn't push them, but good to be aware), rebasing can cause issues for them. For a branch that's primarily yours and not yet pushed, it's generally fine.

4.  **Push your updated branch:**
    Once you've successfully integrated the remote changes (either via merge or rebase) and resolved any conflicts, your local `eCost_Aluminum5_migration_target` branch will have a unified history. Now you can push:
    ```bash
    git push origin eCost_Aluminum5_migration_target
    ```
    This push should now succeed because your local branch's history is a direct descendant of the remote's, or it includes a merge commit that incorporates the remote's history.

### After Pushing: The Pull Request

Once you successfully push, your Pull Request on GitHub (or your Git hosting platform) will automatically update to reflect the new, unified history of your `eCost_Aluminum5_migration_target` branch. It should then show that it's ready to be merged into its target branch (e.g., `origin/eCost_server_Code_Cleanup_bkp_CR` or `main`).
'''

emoji_links = '''
| Tool / Site                             | Link                                                                                                           |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 🌐 [Emojipedia](https://emojipedia.org) | [https://emojipedia.org](https://emojipedia.org)                                                               |
| 💻 [Get Emoji](https://getemoji.com)    | [https://getemoji.com](https://getemoji.com)                                                                   |
| 📦 Unicode list                         | [https://unicode.org/emoji/charts/full-emoji-list.html](https://unicode.org/emoji/charts/full-emoji-list.html) |

'''

to_do_tasks = """
Use case 1:
  - User will upload resume
  - Extract technical skill
  - Extract contact info like Name, Emai, Mobile number, Year of experience , Domain knowledge
  - If AI model enabled
  - Create Prompt to call to AI model
  - Prompt
      Tech skills: []
      Level : [Year of experience]
      Question Type: ['mcq', objective, coding]
      Question: Create sample question for the skills and level, question type and give sample answer also with input/output sample if required.



  - response will be saved in excel
  - show in dashboard
  - generate test paper

Use Case 2:
 - User upload question bank in excel, pdf, docx
 - store the information in vercto db
 - User will ask question to generate and that should be answered from uplaoded one
 - Implement speech to speech for the same  

"""

to_do_tasks_2 = """
Task of today:*****
 - Fix the voice error   //done
 - Add support for file type txt also , currently it supports pdf, excel, docx
 - spelling mistakes of the question should be auto corrected.
 - Memory of the conversation should be handled, ie. While responding to the 3rd question of the user, 
    first and second questions/responses should be in context.
 - After responding to each question, system should list related augmented questions that user could probably ask.
 - If there are any data tables in the document, user should be able to render charts using the same  
 - When user register himself, we Language preference, mobile number,email id we can take default support should also be there.
 - Implement forgot password link.
 - Implement Login/Register functionality, Logging can be multiauth also google, github, twitter.
 - Implement OTP based authentication
 - User based document management, Logged in user will interact with their documents only
 - Multi-lingual support
      - User can upload document of any language.
      - User can interact with the document in any language.
      - In UI user will have options to set the language preference.
  - response of voice can be customized with sample voice selected , like if user wants to listen in Amitabh bachan voice he can listen.    
      
 - User can ask the AI to send the details in his email.
 - User can ask the AI to send the response details in Whatsapp.
 - Correct the UI , User theme, material UI
 - Implement dashboard, show the user stats, and feedback, language stas , country stats
 - User can have avtar which will give response, to be more attractive , like live AI model.
 - Make architecture diagram by your own.
 - Implement sonar for this code based
 - Use best practice for python development.
 - scan the code add custom exceptions, custom Loggers.
 - Integrate splunk
 
Testing:
  - Register user
  - Login with registered id 
  - uplaod the document excel, docx, pdf, text
  - Logged in user should see only their document
  - interact with the document in English
  - Interact with the document in Hindi
  - Interact with the document in chinese
  - Interact with the document in 10 different language
"""
with st.expander("To do Tasks 1"):
    st.code(to_do_tasks, language="text")

with st.expander("To do Tasks 2"):
    st.code(to_do_tasks_2, language="text")

with st.expander("Github Commands"):
    st.code(notes1, language="python")

with st.expander("Github Scenario"):
    st.code(notes2, language="python")

with st.expander("Emoji Links"):
    st.code(emoji_links, language="python")


