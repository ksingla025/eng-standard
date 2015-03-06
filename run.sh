cat $1 | ./language_identifier.py > temp_language
if [ $# -ge 2 ]
then
  echo $2 > temp_language
fi

cat $1 | ./emoticon_remove_regexp.py | ./easy_tokenize2.py | ./escape_sequence_addition.py | ./repetitions_hahe.py | ./superblank_addition.py | ./emoticons_remove.py | ./abbreviations_replace.py |  ./extended_words_trim2.py | ./apostrophe_correction.py | ./trie_implementation.py | ./capitals.py | ./selecting_best_candidate.py  
