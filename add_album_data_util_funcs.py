def duration_str_to_mins(track_dur):
    track_dur_split = track_dur.split(":")
    hours = mins = secs = 0
    if len(track_dur_split) > 2:
        hours = int(track_dur_split[0])
        mins = int(track_dur_split[1])
        secs = int(track_dur_split[2])
    elif len(track_dur_split) > 1:
        mins = int(track_dur_split[0])
        secs = int(track_dur_split[1])
    else:
        secs = int(track_dur_split[0])

    return (hours * 60) + mins + (secs / 60)
