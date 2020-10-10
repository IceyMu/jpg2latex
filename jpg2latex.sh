set +v

# Check for help option
for var in "$@"
do
    if [ "$var" = '-h' ] || [ "$var" = '--help' ]
        then echo "$(<$(dirname $0)/help.txt)" & exit
    fi
done


# Pass arguments to Python script
python "$(dirname $0)/JpgToLatex.py" "$@"

