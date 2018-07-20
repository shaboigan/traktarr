from misc.log import logger

log = logger.get_logger(__name__)


def movies_to_tmdb_dict(radarrpq_movies):
    movies = {}
    try:
        for tmp in radarrpq_movies:
            if 'tmdbId' not in tmp:
                log.debug("Could not handle movie: %s", tmp['title'])
                continue
            movies[tmp['tmdbId']] = tmp
        return movies
    except Exception:
        log.exception("Exception processing Radarrpq movies to TMDB dict: ")
    return None


def remove_existing_movies(radarrpq_movies, trakt_movies):
    new_movies_list = []

    if not radarrpq_movies or not trakt_movies:
        log.error("Inappropriate parameters were supplied")
        return None

    try:
        # turn radarrpq movies result into a dict with tmdb id as keys
        processed_movies = movies_to_tmdb_dict(radarrpq_movies)
        if not processed_movies:
            return None

        # loop list adding to movies that do not already exist
        for tmp in trakt_movies:
            if 'movie' not in tmp or 'ids' not in tmp['movie'] or 'tmdb' not in tmp['movie']['ids']:
                log.debug("Skipping movie because it did not have required fields: %s", tmp)
                continue
            # check if movie exists in processed_movies
            if tmp['movie']['ids']['tmdb'] in processed_movies:
                log.debug("Removing existing movie: %s", tmp['movie']['title'])
                continue

            new_movies_list.append(tmp)

        log.debug("Filtered %d Trakt movies to %d movies that weren't already in Radarrpq", len(trakt_movies),
                  len(new_movies_list))
        return new_movies_list
    except Exception:
        log.exception("Exception removing existing movies from Trakt list: ")
    return None
