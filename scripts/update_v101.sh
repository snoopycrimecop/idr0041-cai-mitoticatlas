#!/bin/bash

# Performs atlas updates for version 1.0.1
# http://www.mitocheck.org/mitotic_cell_atlas/downloads/v1.0.1/


export omero=/opt/omero/server/OMERO.server/bin/omero
projectId=404

# Log in to local server
$omero login demo@localhost

# Delete existing map annotations
$omero metadata populate --batch 100 --wait 2000 --context deletemap --cfg experimentA/idr0041-experimentA-bulkmap-config.yml Project:$projectId --report

# Delete top-level bulk annotation
fId=$($omero hql --ids-only --limit 1 --style plain "select l.child.id from ProjectAnnotationLink l where l.parent.id=$projectId" | cut -d ',' -f2)

if [[ -z $fId ]]; then
    echo "No top-level annotation found"
else
    $omero delete FileAnnotation:$fId --report
fi

# Delete outdated concentration maps
datasets=$(grep 201807.*ftp experimentA/idr0041-experimentA-filePaths.tsv | awk -F ' ' '{print $1}' | awk -F 'Dataset:name:' '{print $2}' | uniq)

for dataset in $datasets; do
    datasetId=$($omero hql --ids-only --limit 1 --style plain "select d.id from Dataset d where d.name='$dataset'" | cut -d ',' -f2)
    echo " Deleting images of dataset $datasetId"
    
    # Delete images under dataset
    $omero delete Dataset/Image:$datasetId --report
done

# Generate list of import commands
tmpBulk=experimentA/tmp.yml
cp experimentA/idr0041-experimentA-bulk.yml experimentA/tmp.yml
echo 'dry_run: "true"' >> experimentA/tmp.yml
$omero import --bulk experimentA/tmp.yml | grep 201807.*ftp > commands.txt
rm experimentA/tmp.yml

# Re-import the updated images
import_image() {
  options=${1//\"/}
  $omero import $options
}
export -f import_image
parallel -a commands.txt --jobs 5 --results rslt --joblog log import_image
rm commands.txt

# Reannotate the project
$omero metadata populate --report --batch 1000 --file experimentA/idr0041-experimentA-annotation.csv Project:$projectId
$omero metadata populate --report --batch 100 --wait 2000 --context bulkmap --cfg experimentA/idr0041-experimentA-bulkmap-config.yml Project:$projectId

# Log out
$omero logout
