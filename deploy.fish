echo "[+] Updating from Remotes"
git remote update

echo "[+] Current tree status"
git status

echo "[+] Updating Sphinx Documentation"
cd hotspot/docs
make html
cd ../../

echo -n "[+] Pre-deploy Commit on local/"
git branch | head -n1 | echo ""
git commit -a -m "$argv"

echo "[+] Pushing to production"
git push production
git push origin
