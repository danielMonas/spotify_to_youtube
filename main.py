import argparse

from log import logger
from spotify_fetcher import SpotifyFetcher
from youtube_scraper import YoutubeFetcher
from youtube_api import YoutubeInterface

def main():
    parser = argparse.ArgumentParser(
        prog='Spotify2Youtube',
        description='Convert a Spotify playlist into a Youtube Music playlist'
    )
    parser.add_argument('spotify_playlist_url', help='The Spotify playlist URL link')
    parser.add_argument('youtube_playlist_id', help='The Youtube playlist ID')
    parser.add_argument('--songs', default=100, type=int)
    args = parser.parse_args()

    # Fetch the songs from the playlist    
    spotify = SpotifyFetcher(args.spotify_playlist_url, args.songs)
    entries = list(spotify.load_all_entries())
    
    youtube_api = YoutubeInterface(args.youtube_playlist_id)
    youtube_scraper = YoutubeFetcher()
    for entry in entries:
        query = f'{entry[0]} by {entry[1]}'
        logger.info(f'Querying YoutubeMusic for: {query} ...')
        video_id = ''
        try:
            video_id = youtube_scraper.load_song(query)
            youtube_api.save_to_playlist(video_id)
            logger.info(f'Saved video: {query}')
        except Exception as e:
            logger.exception(f'Failed to save video: {query}. Got: {video_id}.')


if __name__ == '__main__':
    main()
