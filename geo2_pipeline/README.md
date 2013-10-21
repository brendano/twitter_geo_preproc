This is the pipeline used for http://arxiv.org/abs/1210.5268
Steps are numbered like BASIC so you can figure out what order to run them in.

* [00]  Geo filter to coordinates
* [10]  Geo coding to country, USA county
* [20]  Message filter
    * to USA 48
    * user profile #fer/fing, retweets, URLs and other text content
    * Text processing
* [30] tokenization
* [within 40] downcase, repeats
* [40] Tweet smallification
* [45] First-pass vocab assembly
* [50] Quadification (time/region/user/word and time/region/word counts,
    * numberized and word-bucketed)
* [60] MSA centroid computation
* Future steps in post-quad world
    * Model!  Inference!


Internal version information ("v8"):
SVN ... /usr0/svn-base/brendano/GeoTM/geo2
Last Changed Rev: 27203
Last Changed Date: 2013-08-29 19:27:05 -0400 (Thu, 29 Aug 2013)
("svn export" then moved out the interesting subdirs.)
