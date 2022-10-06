call .\venv\Scripts\activate.bat
python jav2quark.py
cd aww_blog_history
git add . && git commit --short > temp.txt && git commit -F temp.txt && del temp.txt && git push
pause