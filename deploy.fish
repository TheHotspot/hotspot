echo "[+] Updating from Remotes"
git remote update
echo "[+] Current tree status"
git status
if test "$argv"
    echo -n "[+] Pre-deploy Commit on local/"
    git branch | head -n1 | echo ""
    git commit -a -m "$argv"
else
    echo "[+] Pre-deploy Tag on Production"
    ssh root@nicksweeting.com 'cd /opt/hotspot/; git tag "PREDEPLOY:$(date)"`'
end
echo "[+] Pushing to production"
git push production
git tag "POSTDEPLOY"
git push origin
