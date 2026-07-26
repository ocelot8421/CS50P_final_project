More notes for leaners: study_notes.md


# Install dependencies:
```pip install -r requirements.txt```

# Generate exe file:
```pyinstaller --noconfirm --onedir --clean --hidden-import=dash --collect-data dash --collect-data dash_cytoscape --collect-data dash_extensions project.py```
```
[user]@[user]-IdeaPad-5-14ALC05:~$ cd ~
[user]@[user]-IdeaPad-5-14ALC05:~$ mkdir dash_project
[user]@[user]-IdeaPad-5-14ALC05:~$ cd dash_project/
[user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ sudo apt update && sudo apt install python3-venv python3-pip -y
[user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ python3 -m venv venv
[user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ source venv/bin/activate
(venv) [user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ pip install dash dash-cytoscape dash-extensions pyinstaller
```

copy program files here to build

```
(venv) [user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ pyinstaller --noconfirm --onedir --clean --hidden-import=dash --collect-data dash --collect-data dash_cytoscape --collect-data dash_extensions project.py
(venv) [user]@[user]-IdeaPad-5-14ALC05:~/dash_project$ cd dist/
(venv) [user]@[user]-IdeaPad-5-14ALC05:~/dash_project/dist$ cd project/
(venv) [user]@[user]-IdeaPad-5-14ALC05:~/dash_project/dist/project$ ./project 
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'project'
 * Debug mode: off
```

# Testing
```pytest test_project.py ```
