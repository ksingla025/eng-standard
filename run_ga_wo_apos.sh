cat $1 | ./language_identifier.py > temp_language
if [ $# -ge 2 ]
then
  echo $2 > temp_language
fi


cat $1 |  ./escape_sequence_addition.py | ./easy_tokenize2.py | ./repetitions_hahe.py | ./abbreviations_replace.py | ./extended_words_trim2.py | ./trie_implementation.py | ./capitals.py | ./selecting_best_candidate.py | python remove_escape.py 
