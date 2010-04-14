#!/bin/bash

# find/cp iphone photos (from iPhoto)

PHOTO_DIR=$1
EXIF=`which exif`

IDIR="${HOME}/iphone_photos/"
mkdir -p $IDIR


find "${PHOTO_DIR}" -name "*.[jJ][pP][gG]" | while read PHOTO
do
    Y=$(${EXIF} -t PixelYDimension -m "${PHOTO}" )
    X=$(${EXIF} -t PixelXDimension -m "${PHOTO}" )

    if [[ $X == 1600 && $Y == 1200 ]]
    then
        echo ${PHOTO}
        cp "${PHOTO}" ${IDIR}
    fi
done



