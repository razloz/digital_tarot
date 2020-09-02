#!../.env/bin/python3
import pandas as pd
import wave
import struct
import secrets


class Harmonics(object):
    def __init__(self, raw_path):
        """Tone generator."""
        raw = wave.open(raw_path)
        nframes = raw.getnframes()
        nchannels = raw.getnchannels()
        frames = raw.readframes(nframes)
        f = struct.unpack("%ih" % (nframes * nchannels), frames)
        self.TONES = [float(v) / pow(2, 15) for v in f]
        self.TL = len(self.TONES)
        self.next_tone = 0

    def next(self):
        if self.next_tone <= self.TL:
            self.next_tone += 1
            return self.TONES[self.next_tone]
        else:
            raise StopIteration()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()


class ShuffleGen(object):
    def __init__(self, deck_size, key_path):
        """Shuffle Machine."""
        self._secret = Harmonics(key_path)
        self._deck = list(range(deck_size))
        self._half_cut = int(deck_size * 0.5)
        self._variance = int(deck_size * 0.1)
        self._last_freq = None

    def next_freq(self):
        seeking = True
        while seeking:
            try:
                freq = self._secret.next()
                if freq < 0: freq *= -1
                if self._last_freq != freq:
                    self._last_freq = freq
                    seeking = False
            except StopIteration:
                self._last_freq = 0
                seeking = False
        return self._last_freq

    def next_shuffle(self):
        new_order = list()
        rng = secrets.randbelow
        rnd = lambda x: int(round(x, 0))
        get_variance = lambda: rnd(rng(self._variance) + self.next_freq())
        if rng(1) == 0:
            cut_pos = int(self._half_cut + get_variance())
        else:
            cut_pos = int(self._half_cut - get_variance())
        packets = [self._deck[:cut_pos], self._deck[cut_pos:]]
        def drop_card(p):
            re = len(packets[p]) - 1
            new_order.append(packets[p][re])
            packets[p].pop(re)
        shuffling = True
        while shuffling:
            right_len = len(packets[0])
            left_len = len(packets[1])
            if right_len == 0 == left_len: shuffling = False
            if right_len > 0:
                drop = get_variance()
                if drop != 0:
                    try:
                        for i in range(drop):
                            drop_card(0)
                    except IndexError:
                        pass
                else:
                    drop_card(0)
            if left_len > 0:
                drop = get_variance()
                if drop != 0:
                    try:
                        for i in range(drop):
                            drop_card(1)
                    except IndexError:
                        pass
                else:
                    drop_card(1)
        new_order.reverse()
        self._deck = new_order
        return self._deck

    def caste_reading(self, cards):
        suits = ('Cups', 'Wands', 'Coins', 'Swords')
        minor_arcana = (
            'Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
            'Eight', 'Nine', 'Ten', 'Jack', 'Knight', 'Queen', 'King'
            )
        major_arcana = (
            'The Magician', 'The High Priestess', 'The Empress',
            'The Emperor', 'The Hierophant', 'The Lovers', 'The Chariot',
            'Strength', 'The Hermit', 'Wheel of Fortune', 'Justice',
            'The Hanged Man', 'Death', 'Temperance', 'The Devil',
            'The Tower', 'The Star', 'The Moon', 'The Sun', 'Judgement',
            'The World', 'The Fool'
            )
        caste = list()
        for s in suits:
            for c in minor_arcana:
                caste.append(f'{c} of {s}')
        for m in major_arcana:
            caste.append(m)
        reading = list()
        for i in range(cards):
            top_card = self._deck[0]
            reading.append(caste[top_card])
            self._deck.pop(0)
            self._deck.append(top_card)
        return reading


if __name__ == '__main__':
    gen = ShuffleGen(78, '../key.wav')
    for i in range(9):
        shuffle = gen.next_shuffle()
    for i in range(13):
        shuffle = gen.next_shuffle()
        reading = gen.caste_reading(8)
    print(reading)
