jupyter nbconvert --to notebook --execute *.ipynb
for i in *.nbconvert.ipynb; do
    mv "$i" "${i/.nbconvert.ipynb/.ipynb}"
done
jupyter nbconvert --to PDF *.ipynb
pdftk *_Portfolio*.pdf cat output Portfolio_Report_xyz.pdf
rm *_Portfolio*.pdf
