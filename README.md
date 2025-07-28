# weed-mapping-through-CNN-preds
using a selected YOLO model's predictions into implementing weed maps through QGIS environment.

LESSSGO!

So part of my work as a researcher in the lovely sector of Precision Agriculture, was the development and assessment of various deep learning models for the automated detection of four selected weeds.
So what happens when we combine the selected model's weed predictions (.txt files where labels are in YOLO format) and the drone's metadata file (valuable info regarding the timestamp, rel_altitude, longitutde, latitude, etc.)

This rep is for organizing the scripts and files that were used to produce three types of weed maps, depending on the farmer's needs.

DISCLAIMER!!!!!!! THE MAPS CANT BE PROPERLY USED FOR ADVANCED APPLICATIONS SUCH AS EG. PATCH-SPRAYING DUE TO THE RELATIVELY LOW GPS PRECISION. AN RTK GPS FOR EXAMPLE SHOULD BE PROVIDED, FOR PRECISED GEO-REFERENCING.

Three types of maps were produced:

1)Dominant-weed-map.
As the name tells, each frame of the drone contains the most dominant weed that appeared in total. 
So if class 1 had 10 depictions, class 2 had 5 and class 3 had 3, the frame will show class 1.

2)Relative-%-weed (compared to others)
Moving on to the second category, this map will show the relative percentage (%) of coverage for each weed that is located per frame. This map is produced per each class (so for example, if the weeds were 10 then 10 maps per each class must be produced. 
Of course nothing is obligatory, but that's just how it works :p)
Case example: in a frame, class 1 has 10 depictions and class 2 has 1 depiction. So the same frame for class 1 will show class 1 as 90%, while for class 2 it will show 10%.

3)Absolute-number-of-weed (unrelevant in comparison to others)
The third and last category shows each frame per absolute number of the weed which as it's already spoiled, each frame is independant of the other classes. Similar to the second category, this map is produced per each class.
So if a frame has 10 weeds of class 1, 5 weeds of class 2 and 2 weeds of class 3, for the 3 seperate maps the same frame will show the number 10 for class 1, 5 for class 2 and 2 for class 3.

Each map can be used for a general knowing of the "weed-jungle" that can be taking place in a farmer's crop/land.

Might be "easy-work" but precision agriculture is about exploring new tools and helping farmers to adapt to this evolution called "Agriculture 4.0" (soon to be 5.0!)

