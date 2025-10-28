# create_songs.py
# No external modules used.

from typing import List  # only for type hints (optional)

class Song:
    """Simple Song container. Attributes are created from CSV header names."""
    def __init__(self, **fields):
        # create attributes for each field and keep dict copy
        self.fields = {}
        for k, v in fields.items():
            safe_name = k.strip()
            setattr(self, safe_name, v)
            self.fields[safe_name] = v

    def __repr__(self):
        # show a compact representation using possible title-like fields
        title_keys = ['track_name', 'title', 'name']
        title = None
        for k in title_keys:
            if k in self.fields:
                title = self.fields[k]
                break
        if title is None:
            # fallback: first field
            title = next(iter(self.fields.values()), '')
        return f"<Song {title!r}>"

def parse_csv_line(line: str) -> List[str]:
    """Parse a single CSV line into fields. Handles quoted fields and doubled quotes."""
    fields = []
    field = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                # potential end or escaped quote
                if i + 1 < len(line) and line[i+1] == '"':
                    # escaped quote -> add a single quote and skip next
                    field.append('"')
                    i += 1
                else:
                    # end quote
                    in_quotes = False
            else:
                field.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                fields.append(''.join(field))
                field = []
            else:
                field.append(ch)
        i += 1
    # append last field (strip trailing newline/carriage return)
    fields.append(''.join(field).rstrip('\r\n'))
    return fields

def convert_number_if_possible(s: str):
    """Try to convert string to int or float, otherwise return original stripped string."""
    s_trim = s.strip()
    if s_trim == '':
        return ''
    # Try int (but avoid converting strings with leading zeros that might be identifiers)
    try:
        if s_trim.isdigit() or (s_trim.startswith('-') and s_trim[1:].isdigit()):
            return int(s_trim)
    except Exception:
        pass
    # try float
    try:
        f = float(s_trim)
        return f
    except Exception:
        pass
    return s_trim

def load_songs_from_csv(path: str) -> List[Song]:
    """Load CSV at path and return list of Song objects. Minimal, no-external-parser CSV handling."""
    songs = []
    with open(path, 'r', encoding='utf-8') as fh:
        # read header line (handle possible BOM)
        header_line = fh.readline()
        if not header_line:
            return songs
        if header_line.startswith('\ufeff'):
            header_line = header_line.lstrip('\ufeff')
        headers = [h.strip() for h in parse_csv_line(header_line)]
        # read the rest
        for raw_line in fh:
            # skip empty lines
            if raw_line.strip() == '':
                continue
            values = parse_csv_line(raw_line)
            # If values < headers, pad with empty strings; if more, keep extras joined into last field
            if len(values) < len(headers):
                values += [''] * (len(headers) - len(values))
            elif len(values) > len(headers):
                # join extras into last field (simple fallback)
                values = values[:len(headers)-1] + [','.join(values[len(headers)-1:])]
            # convert numeric-looking fields
            converted = [convert_number_if_possible(v) for v in values]
            field_map = dict(zip(headers, converted))
            song = Song(**field_map)
            songs.append(song)
    return songs

if __name__ == '__main__':
    csv_path = r"C:\Users\jinas\Downloads\taylor_discography.csv"  # change if needed
    print("Loading songs from:", csv_path)
    songs = load_songs_from_csv(csv_path)
    print("Loaded", len(songs), "songs.")

    # show header fields (if at least one song loaded)
    if songs:
        sample_headers = list(songs[0].fields.keys())
        print("Detected fields:", sample_headers)

    # Replace the previous "print first 5 ..." block with the following:

def show_paginated(songs, page_size=20):
    """Interactively show songs page_size at a time. Press Enter to continue, 'q' to quit."""
    total = len(songs)
    if total == 0:
        print("No songs to show.")
        return
    idx = 0
    while idx < total:
        end = min(idx + page_size, total)
        for i, s in enumerate(songs[idx:end], start=idx+1):
            title = s.fields.get('track_name') or s.fields.get('title') or s.fields.get('name') or '<no title>'
            track_id = s.fields.get('track_id', '')
            duration = s.fields.get('duration_ms', '')
            print(f"{i:4d}. {title}  |  track_id: {track_id}  |  duration_ms: {duration}")
        idx = end
        if idx >= total:
            print(f"-- End (shown {total}/{total})")
            break
        # prompt user to continue
        try:
            cont = input(f"-- Showing {idx}/{total}. Press Enter to see next {page_size}, or type 'q' to quit: ")
        except (EOFError, KeyboardInterrupt):
            print("\n-- Input interrupted, exiting.")
            break
        if cont.strip().lower().startswith('q'):
            print("-- Quitting pagination.")
            break

# Call the paginator with your desired page size:
PAGE_SIZE = 24  # change this to view a different number per page
print(f"\nShowing songs {1}..{min(PAGE_SIZE, len(songs))} (page size = {PAGE_SIZE})")
show_paginated(songs, page_size=PAGE_SIZE)