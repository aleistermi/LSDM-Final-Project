#!/bin/bash
set -x –e
apt-get update -y
apt-get install -y default-jre
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
apt install unzip
unzip stanford-corenlp-full-2018-10-05.zip
cd stanford-corenlp-full-2018-10-05
wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2018-10-05-models.jar
for file in `find . -name "*.jar"`; do export
CLASSPATH="$CLASSPATH:`realpath $file`"; done
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-spanish.properties -port 9000