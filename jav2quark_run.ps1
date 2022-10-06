call .\venv\Scripts\activate.ps1
python jav2quark.py
cd aww_blog_history
git add . && git commit --short > temp.txt && git commit -F temp.txt && rm temp.txt && git push
pause