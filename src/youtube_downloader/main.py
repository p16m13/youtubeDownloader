import os
import sys
import pathlib
import argparse
import typing as T
from datetime import datetime

from pytube import Playlist, YouTube


def resource_path(relative_path):
    """ Gets the absolute path to resource"""
    return os.path.join(pathlib.Path().resolve(), relative_path)


def parse_args(input_args):
    parser = argparse.ArgumentParser(description="Youtube downloader")
    parser.add_argument("--video-urls-file", default='video_urls.txt',
                        help='Provide the absolute path to the file with video URLs')
    parser.add_argument("--playlist-urls-file", default='playlist_urls.txt',
                        help='Provide the absolute path to the file with playlist URLs')
    parser.add_argument("--output-location", default=f'Downloads/{datetime.now().date()}',
                        help='Provide the absolute path to the location where the videos will be  downloaded to')
    args, _ = parser.parse_known_args(input_args[1:])
    return args


def get_playlist_video_urls(playlist_url: str) -> T.List[T.AnyStr]:
    """
    Retrieves the list of video urls the playlist contains
    :param playlist_url: the url of the Youtube playlist
    :return: the list of video URLs
    """
    try:
        return [url for url in Playlist(playlist_url)]
    except Exception as e:
        print(f'Failed to parse the following playlist url: {playlist_url}. Error message: {str(e)}')
        return []


def get_links_from_file(file_path) -> T.List[T.AnyStr]:
    """
    Parses the input file
    :param file_path: the path to the file need to be parsed
    :return: the list of URLs the input file contains
    """

    try:
        with open(file_path) as f:
            return f.readlines()
    except Exception as e:
        print(f'Failed to read the file. Please check if the passed path is correct. Error message: {str(e)}')
        return []


def download_video(link: str, output_location: str) -> None:
    try:
        yt = YouTube(link)
        video_title = yt.title
        print(f'Starting downloading the video `{video_title}`')
        yt.streams.filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path=output_location)
        print(f'The video `{video_title}` has downloaded successfully')
    except Exception as e:
        print(f'Failed to download the video using link `{link}`. Error message: {str(e)}')


def main(args):
    links = []
    output_location = resource_path(args.output_location)
    playlist_urls_file = resource_path(args.playlist_urls_file)
    video_urls_file = resource_path(args.video_urls_file)
    for playlist_url in get_links_from_file(playlist_urls_file):
        links.extend(get_playlist_video_urls(playlist_url.strip()))
    links.extend(get_links_from_file(video_urls_file))
    if links:
        for link in links:
            download_video(link, output_location)


if __name__ == '__main__':
    args = parse_args(sys.argv)
    main(args)
