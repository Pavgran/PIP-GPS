"""
Program name: PIP/GPS interpreter
Module description: Program launcher
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

import PIPGPS

interp = PIPGPS.PIPGPS()

prog="""
/*
Program name: Countdown
Lang: PIP/GPS
Date: 20 dec 2014
*/

i=25; //smth
#LOOP
iPHONLY(i==0 OR i>0 AND i<0){
GOOGLEFOR LABEL;
}ANDROIDLY{
i=i*1-1;
SMS i; SMS "\n";
GOOGLEFOR LOOP;
};
i=15; //never
#LABEL
SMS "DONE\n";
"""

interp.run(prog)
