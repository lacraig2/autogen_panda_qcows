mkdir -p dbgsym
docker build --no-cache -t panda-limage-downloader .
docker run -v `pwd`/dbgsym:/var/cache/apt/archives/ panda-limage-downloader ls /var/cache/apt/archives
