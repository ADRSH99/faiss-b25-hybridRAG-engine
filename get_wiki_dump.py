import wikipedia

titles = [
    # Core Music Concepts
    "Music", "Music theory", "Musical instrument", "Western classical music",
    "Indian classical music", "Carnatic music", "Hindustani classical music",
    "Pop music", "Rock music", "Hip hop music", "Electronic music",
    "Jazz", "Blues", "Heavy metal music", "Folk music", "Bollywood music",
    "Music production", "Sound design", "Music composition", "Music history",
    "Musicology", "Ethnomusicology", "Music education", "Music psychology",
    "Music technology", "Music genre", "Chord (music)", "Harmony (music)",
    "Melody", "Rhythm", "Musical notation", "Tempo", "Dynamics (music)",
    "Timbre", "Musical form", "Scale (music)", "Raga", "Gamaka (music)",
    "Solfège", "Counterpoint", "Orchestration", "Improvisation",
    "Music theory of India", "Music cognition", "Acoustics", "Psychoacoustics",

    # Instruments
    "Piano", "Guitar", "Electric guitar", "Bass guitar", "Drum kit",
    "Violin", "Tabla", "Sitar", "Flute", "Saxophone", "Trumpet",
    "Cello", "Veena", "Mridangam", "Harmonium",

    # Genres (extended)
    "Classical music", "Opera", "Baroque music", "Romantic music",
    "Contemporary classical music", "Country music", "R&B", "Soul music",
    "Reggae", "K-pop", "Indie rock", "Alternative rock",
    "Progressive rock", "Punk rock", "EDM", "House music", "Techno",
    "Trance music", "Drum and bass", "Dubstep", "Ambient music", 
    "Lo-fi music",

    # Bollywood & Indian Music
    "Indian pop", "Indian rock", "Bhangra", "Ghazal", "Sufi music",
    "Qawwali", "Playback singing", "Bollywood playback singer",
    "Indian film music",

    # Production & Industry
    "Audio engineering", "Mixing (music)", "Mastering (audio)",
    "Digital audio workstation", "Auto-Tune", "MIDI",
    "Music streaming service", "Music industry", "Record label",
    "Music copyright", "Performing rights organization",

    # History & Culture
    "History of music", "Music of India", "Music of the United States",
    "Music of Europe", "Music of Africa", "Music of East Asia",
    "Music of the Middle East", "Music festival", "Concert", 
    "Orchestra", "Choir",

    # Famous People (safe, high-context pages)
    "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach",
    "A.R. Rahman", "Ravi Shankar", "Michael Jackson", "The Beatles",
    "Freddie Mercury", "Taylor Swift", "Beyoncé", "Eminem",
    "Kanye West", "Daft Punk"
]


dataset_text = ""

for title in titles:
    try:
        print(f"Fetching: {title}")
        summary = wikipedia.summary(title)
        dataset_text += f"### {title}\n{summary}\n\n"
    except Exception as e:
        print(f"Skipping {title}: {e}")

with open("music_wiki_dump.txt", "w", encoding="utf-8") as f:
    f.write(dataset_text)

print("\nMUSIC WIKI DUMP SAVED TO music_wiki_dump.txt")
