for f in *.lbl; 
do
 fname="$(cut -d. -f1-1 <<< $f)"
 gdal_translate $f $fname.tif
done
