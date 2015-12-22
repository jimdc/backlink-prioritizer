Backlink-prioritizer
========

Wikipedia lists all the backlinks to a particular article on its ''Special:WhatLinksHere'' page. If, for example, you recently created a new article that has a more narrowly defined scope than an existing, but popularly linked article, you will want to comb through all of those backlinks to see where you can substitute your own article.

But what if there are hundreds of backlinks? Backlink-prioritizer finds the backlinks which have the most views within the last 90 days, by feeding the output of Wikipedia's ''WhatLinksHere'' (from the official API) to Domas Mituzas's Wikipedia article traffic statistics website. Since this can take a long time, Backlink-prioritizer live-prints and saves its progress: in case you want to do a keyboard interrupt (Ctrl+C) if it's taking too long, or if your internet connection is faulty, or the traffic statistics website refuses your connection, etc.

Example usage: <code>python whatlinkedhere.py Joseph_Feildon</code> 

It will create a file, <code>Joseph_Feildon_(wlh).txt</code> having newline-separated two-dimensional arrays of backlink title and backlink's number of views, in decreasing order of the latter.
