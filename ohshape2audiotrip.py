import yaml
import json

with open("prrrum.yml", 'r') as ohshape_stream:
    with open("template.ats", 'r') as template_stream:
        try:
            oss = yaml.safe_load(ohshape_stream)
            song_title = oss['title']
            song_length = oss['audioTime']
            song_file = oss['clip'] + '.ogg'
            song_speed = oss['speed']
            song_preview = oss['preview']
            song_bpm = oss['gridBpm']
            song_author = oss['author']

            print(song_title + ' (' + str(song_length) + 's)')
            print(song_file)
            if song_bpm > 1:
                print(' (' + str(song_bpm) + ' bpm)\n')

            at_template = yaml.safe_load(template_stream)
            at_template['metadata']['title'] = song_title
            at_template['metadata']['artist'] = song_author
            at_template['metadata']['songEndTimeInSeconds'] = song_length
            at_template['metadata']['songFullLengthInSeconds'] = song_length
            at_template['metadata']['previewStartInSeconds'] = song_preview
            at_events = at_template['choreographies']['list'][0]['data']['events']

            song_levels = oss['levels']
            song_level_0 = song_levels[0]
            song_seq = song_level_0['sequence']
            for ev in song_seq:
                ev_time = ev['second']
                ev_obj = ev['obj']
                ev_beat_str = '0000.0'
                if song_bpm > 0.1:
                    # Calculate whch beat (if bpm provided)
                    ev_beat = ev_time * (song_bpm / 60.0)
                    # Round to nearest quarter beat
                    ev_beat = (round(ev_beat * 4)) / 4
                    ev_beat_str = "{:06.1f}".format(ev_beat)
                print(ev_beat_str + ': ' + ev_obj)
                ev_type = ev_obj[:2]
                new_ev = {}
                if ev_type == 'WA':
                    ev_sub_type = ev_obj[3:-3]
                    print('barrier: ' + ev_sub_type)
                    new_ev = {
                            "type": 8,
                            "hasGuide": False,
                            "time": {
                                "beat": ev_beat,
                                "numerator": 0,
                                "denominator": 1
                            },
                            "beatDivision": 2,
                            "position": {
                                "x": 0.6000000238418579,
                                "y": 1.5,
                                "z": 0.0
                            },
                            "subPositions": [
                                {
                                    "x": -45.0,
                                    "y": 45.0,
                                    "z": -1.0
                                }
                            ],
                            "broadcastEventID": 0
                    }
                elif ev_type == 'CN':
                    print('coin')
                elif ev_type == 'WP':
                    print('wall hole')
                if new_ev != {}:
                    at_events.append(new_ev)

            print(song_level_0)
            with open("output.ats", 'w') as output_stream:
                json.dump(at_template, output_stream, indent=4)

        except yaml.YAMLError as exc:
            print(exc)
