# **youtubeDownloader**

**youtubeDownloader** is an application for downloading playlists and videos from youtube.com  

## Usage

### Installation

Using make

```bash
$ make init
```

OR using poetry

```bash
$ poetry install
```

### Providing required links

#### Downloading playlists or videos

Add URLs of desired playlists on Youtube to the file `playlist_urls.txt`, and videos to the file `video_urls.txt`.

```bash
$ python src/youtube_downloader/main.py 
```
