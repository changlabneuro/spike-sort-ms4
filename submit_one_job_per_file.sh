i=1
for n in $(cat raw_file_list.txt)
do
    echo "Working on file $n now \n"
    python generate_submission_script.py --file "$n" $i
    sbatch "submit-$n.sh"
    i=$(expr $i + 1)
done
