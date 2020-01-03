docker build -t ff .
docker run --rm -v $(pwd):/home ff /home/script.pe
