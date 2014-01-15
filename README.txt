The Hotspot Social Nightlife App
Coming soon to a city near you...

Django v1.6 Python v2.7
django-allauth
south

responsive mobile site

git:  
    gadd: git add $argv  
    apus: git push origin master --force  
    gpus: git push origin master  
    com: git commit -m "$argv"  
    acom: git commit -a -m "$argv; apus"  
    gs: git status  
    gl: git log  
  
bash:  
    t: tree -C --dirsontop $argv  
    l: ls -la $argv  
  
bash status loop:  
    while :; do clear; tree -C -t --dirsfirst; git status; python hotspot/manage.py validate| pygmentize -l python ; sleep 5; done  
  
django:  
    ./status.py: python status monitor with growl notifications on buildfail
    manage: python manage.py $argv  
    sdb: manage syncdb; manage migrate  
    runs: manage runserver  
    val: manage validate  
    startapp: django-admin.py startapp $argv  
  
modified fish_title  
