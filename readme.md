docker build -t ff .

docker run --rm -v $(pwd):/home ff /usr/bin/python /home/script.py
