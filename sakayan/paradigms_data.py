"""Hand-curated verb conjugation paradigms from Sakayan.

Why hand-curated: the textbook's paradigm tables span multiple verbs in
parallel columns with no whitespace separators in the source PDF, which
makes auto-extraction fragile. Reading and typing the paradigm into this
file once is fast; the reusable Anki cards are then derived
mechanically by `paradigms.py`.

Each entry records one tense for one verb. Add new entries as you reach
new units. Keep `unit` accurate so tags stay sortable.
"""


# Pronoun keys are uniform across all paradigms. The `english` field
# carries the *fully conjugated* English form so we don't have to do
# English morphology — just look up and emit.
PARADIGMS: list[dict] = [
    # ---------------- Unit 1 ----------------
    {
        "verb": "ունենալ",
        "english_infinitive": "to have",
        "tense": "present (irregular)",
        "unit": 1,
        "page": 37,
        "forms": {
            "1sg": ("ունեմ",   "I have"),
            "2sg": ("ունես",   "you have (sg/informal)"),
            "3sg": ("ունի",    "he/she has"),
            "1pl": ("ունենք",  "we have"),
            "2pl": ("ունեք",   "you have (pl/formal)"),
            "3pl": ("ունեն",   "they have"),
        },
    },
    {
        "verb": "ունենալ",
        "english_infinitive": "to have",
        "tense": "present (regular continuative)",
        "unit": 1,
        "page": 37,
        "forms": {
            "1sg": ("ունենում եմ",   "I have (continuative)"),
            "2sg": ("ունենում ես",   "you have (sg, continuative)"),
            "3sg": ("ունենում է",    "he/she has (continuative)"),
            "1pl": ("ունենում ենք",  "we have (continuative)"),
            "2pl": ("ունենում եք",   "you have (pl, continuative)"),
            "3pl": ("ունենում են",   "they have (continuative)"),
        },
    },
    {
        "verb": "լինել",
        "english_infinitive": "to be",
        "tense": "present (irregular auxiliary)",
        "unit": 1,
        "page": 37,
        "forms": {
            "1sg": ("եմ",   "I am"),
            "2sg": ("ես",   "you are (sg/informal)"),
            "3sg": ("է",    "he/she is"),
            "1pl": ("ենք",  "we are"),
            "2pl": ("եք",   "you are (pl/formal)"),
            "3pl": ("են",   "they are"),
        },
    },

    # ---------------- Unit 2 (negation) ----------------
    {
        "verb": "լինել",
        "english_infinitive": "to be",
        "tense": "present negative",
        "unit": 2,
        "page": 55,
        "forms": {
            "1sg": ("չեմ",   "I am not"),
            "2sg": ("չես",   "you are not (sg)"),
            "3sg": ("չի",    "he/she is not"),
            "1pl": ("չենք",  "we are not"),
            "2pl": ("չեք",   "you are not (pl)"),
            "3pl": ("չեն",   "they are not"),
        },
    },
    {
        "verb": "ունենալ",
        "english_infinitive": "to have",
        "tense": "present negative (irregular)",
        "unit": 2,
        "page": 55,
        "forms": {
            "1sg": ("չունեմ",   "I don't have"),
            "2sg": ("չունես",   "you don't have (sg)"),
            "3sg": ("չունի",    "he/she doesn't have"),
            "1pl": ("չունենք",  "we don't have"),
            "2pl": ("չունեք",   "you don't have (pl)"),
            "3pl": ("չունեն",   "they don't have"),
        },
    },
    {
        "verb": "գիտենալ",
        "english_infinitive": "to know",
        "tense": "present negative (irregular)",
        "unit": 2,
        "page": 55,
        "forms": {
            "1sg": ("չգիտեմ",   "I don't know"),
            "2sg": ("չգիտես",   "you don't know (sg)"),
            "3sg": ("չգիտի",    "he/she doesn't know"),
            "1pl": ("չգիտենք",  "we don't know"),
            "2pl": ("չգիտեք",   "you don't know (pl)"),
            "3pl": ("չգիտեն",   "they don't know"),
        },
    },

    # ---------------- Unit 3 (imperfect) ----------------
    {
        "verb": "լինել",
        "english_infinitive": "to be",
        "tense": "imperfect",
        "unit": 3,
        "page": 78,
        "forms": {
            "1sg": ("էի",    "I was"),
            "2sg": ("էիր",   "you were (sg)"),
            "3sg": ("էր",    "he/she was"),
            "1pl": ("էինք",  "we were"),
            "2pl": ("էիք",   "you were (pl)"),
            "3pl": ("էին",   "they were"),
        },
    },
    {
        "verb": "ունենալ",
        "english_infinitive": "to have",
        "tense": "imperfect (irregular)",
        "unit": 3,
        "page": 78,
        "forms": {
            "1sg": ("ունեի",    "I had"),
            "2sg": ("ունեիր",   "you had (sg)"),
            "3sg": ("ուներ",    "he/she had"),
            "1pl": ("ունեինք",  "we had"),
            "2pl": ("ունեիք",   "you had (pl)"),
            "3pl": ("ունեին",   "they had"),
        },
    },
    {
        "verb": "գիտենալ",
        "english_infinitive": "to know",
        "tense": "imperfect (irregular)",
        "unit": 3,
        "page": 78,
        "forms": {
            "1sg": ("գիտեի",    "I knew"),
            "2sg": ("գիտեիր",   "you knew (sg)"),
            "3sg": ("գիտեր",    "he/she knew"),
            "1pl": ("գիտեինք",  "we knew"),
            "2pl": ("գիտեիք",   "you knew (pl)"),
            "3pl": ("գիտեին",   "they knew"),
        },
    },

    # ---------------- Unit 4 (aorist / simple past) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "aorist (simple past)",
        "unit": 4,
        "page": 99,
        "forms": {
            "1sg": ("գրեցի",    "I wrote"),
            "2sg": ("գրեցիր",   "you wrote (sg)"),
            "3sg": ("գրեց",     "he/she wrote"),
            "1pl": ("գրեցինք",  "we wrote"),
            "2pl": ("գրեցիք",   "you wrote (pl)"),
            "3pl": ("գրեցին",   "they wrote"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "aorist (simple past)",
        "unit": 4,
        "page": 99,
        "forms": {
            "1sg": ("կարդացի",    "I read (past)"),
            "2sg": ("կարդացիր",   "you read (sg, past)"),
            "3sg": ("կարդաց",     "he/she read (past)"),
            "1pl": ("կարդացինք",  "we read (past)"),
            "2pl": ("կարդացիք",   "you read (pl, past)"),
            "3pl": ("կարդացին",   "they read (past)"),
        },
    },

    # ---------------- Unit 5 (perfect / pluperfect) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "perfect",
        "unit": 5,
        "page": 122,
        "forms": {
            "1sg": ("գրել եմ",   "I have written"),
            "2sg": ("գրել ես",   "you have written (sg)"),
            "3sg": ("գրել է",    "he/she has written"),
            "1pl": ("գրել ենք",  "we have written"),
            "2pl": ("գրել եք",   "you have written (pl)"),
            "3pl": ("գրել են",   "they have written"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "perfect",
        "unit": 5,
        "page": 122,
        "forms": {
            "1sg": ("կարդացել եմ",   "I have read"),
            "2sg": ("կարդացել ես",   "you have read (sg)"),
            "3sg": ("կարդացել է",    "he/she has read"),
            "1pl": ("կարդացել ենք",  "we have read"),
            "2pl": ("կարդացել եք",   "you have read (pl)"),
            "3pl": ("կարդացել են",   "they have read"),
        },
    },
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "pluperfect",
        "unit": 5,
        "page": 123,
        "forms": {
            "1sg": ("գրել էի",    "I had written"),
            "2sg": ("գրել էիր",   "you had written (sg)"),
            "3sg": ("գրել էր",    "he/she had written"),
            "1pl": ("գրել էինք",  "we had written"),
            "2pl": ("գրել էիք",   "you had written (pl)"),
            "3pl": ("գրել էին",   "they had written"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "pluperfect",
        "unit": 5,
        "page": 123,
        "forms": {
            "1sg": ("կարդացել էի",    "I had read"),
            "2sg": ("կարդացել էիր",   "you had read (sg)"),
            "3sg": ("կարդացել էր",    "he/she had read"),
            "1pl": ("կարդացել էինք",  "we had read"),
            "2pl": ("կարդացել էիք",   "you had read (pl)"),
            "3pl": ("կարդացել էին",   "they had read"),
        },
    },

    # ---------------- Unit 6 (future indicative) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "future indicative",
        "unit": 6,
        "page": 149,
        "forms": {
            "1sg": ("գրելու եմ",    "I will write"),
            "2sg": ("գրելու ես",    "you will write (sg)"),
            "3sg": ("գրելու է",     "he/she will write"),
            "1pl": ("գրելու ենք",   "we will write"),
            "2pl": ("գրելու եք",    "you will write (pl)"),
            "3pl": ("գրելու են",    "they will write"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "future indicative",
        "unit": 6,
        "page": 149,
        "forms": {
            "1sg": ("կարդալու եմ",    "I will read"),
            "2sg": ("կարդալու ես",    "you will read (sg)"),
            "3sg": ("կարդալու է",     "he/she will read"),
            "1pl": ("կարդալու ենք",   "we will read"),
            "2pl": ("կարդալու եք",    "you will read (pl)"),
            "3pl": ("կարդալու են",    "they will read"),
        },
    },

    # ---------------- Unit 7 (subjunctive) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "subjunctive future",
        "unit": 7,
        "page": 174,
        "forms": {
            "1sg": ("գրեմ",   "(that) I write"),
            "2sg": ("գրես",   "(that) you write (sg)"),
            "3sg": ("գրի",    "(that) he/she write"),
            "1pl": ("գրենք",  "(that) we write / let's write"),
            "2pl": ("գրեք",   "(that) you write (pl)"),
            "3pl": ("գրեն",   "(that) they write"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "subjunctive future",
        "unit": 7,
        "page": 174,
        "forms": {
            "1sg": ("կարդամ",   "(that) I read"),
            "2sg": ("կարդաս",   "(that) you read (sg)"),
            "3sg": ("կարդա",    "(that) he/she read"),
            "1pl": ("կարդանք",  "(that) we read / let's read"),
            "2pl": ("կարդաք",   "(that) you read (pl)"),
            "3pl": ("կարդան",   "(that) they read"),
        },
    },
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "subjunctive past",
        "unit": 7,
        "page": 175,
        "forms": {
            "1sg": ("գրեի",    "(that) I wrote / would write"),
            "2sg": ("գրեիր",   "(that) you wrote (sg) / would write"),
            "3sg": ("գրեր",    "(that) he/she wrote / would write"),
            "1pl": ("գրեինք",  "(that) we wrote / would write"),
            "2pl": ("գրեիք",   "(that) you wrote (pl) / would write"),
            "3pl": ("գրեին",   "(that) they wrote / would write"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "subjunctive past",
        "unit": 7,
        "page": 175,
        "forms": {
            "1sg": ("կարդայի",    "(that) I read / would read"),
            "2sg": ("կարդայիր",   "(that) you read (sg) / would read"),
            "3sg": ("կարդար",     "(that) he/she read / would read"),
            "1pl": ("կարդայինք",  "(that) we read / would read"),
            "2pl": ("կարդայիք",   "(that) you read (pl) / would read"),
            "3pl": ("կարդային",   "(that) they read / would read"),
        },
    },

    # ---------------- Unit 8 (mandative I) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "mandative future I (պիտի)",
        "unit": 8,
        "page": 201,
        "forms": {
            "1sg": ("պիտի գրեմ",   "I must write / I should write"),
            "2sg": ("պիտի գրես",   "you must write (sg)"),
            "3sg": ("պիտի գրի",    "he/she must write"),
            "1pl": ("պիտի գրենք",  "we must write"),
            "2pl": ("պիտի գրեք",   "you must write (pl)"),
            "3pl": ("պիտի գրեն",   "they must write"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "mandative future I (պիտի)",
        "unit": 8,
        "page": 201,
        "forms": {
            "1sg": ("պիտի կարդամ",   "I must read / I should read"),
            "2sg": ("պիտի կարդաս",   "you must read (sg)"),
            "3sg": ("պիտի կարդա",    "he/she must read"),
            "1pl": ("պիտի կարդանք",  "we must read"),
            "2pl": ("պիտի կարդաք",   "you must read (pl)"),
            "3pl": ("պիտի կարդան",   "they must read"),
        },
    },
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "mandative past I (պիտի)",
        "unit": 8,
        "page": 202,
        "forms": {
            "1sg": ("պիտի գրեի",    "I should have written / I was supposed to write"),
            "2sg": ("պիտի գրեիր",   "you should have written (sg)"),
            "3sg": ("պիտի գրեր",    "he/she should have written"),
            "1pl": ("պիտի գրեինք",  "we should have written"),
            "2pl": ("պիտի գրեիք",   "you should have written (pl)"),
            "3pl": ("պիտի գրեին",   "they should have written"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "mandative past I (պիտի)",
        "unit": 8,
        "page": 202,
        "forms": {
            "1sg": ("պիտի կարդայի",    "I should have read"),
            "2sg": ("պիտի կարդայիր",   "you should have read (sg)"),
            "3sg": ("պիտի կարդար",     "he/she should have read"),
            "1pl": ("պիտի կարդայինք",  "we should have read"),
            "2pl": ("պիտի կարդայիք",   "you should have read (pl)"),
            "3pl": ("պիտի կարդային",   "they should have read"),
        },
    },

    # ---------------- Unit 9 (resultative) ----------------
    {
        "verb": "նստել",
        "english_infinitive": "to sit down",
        "tense": "resultative present",
        "unit": 9,
        "page": 228,
        "forms": {
            "1sg": ("նստած եմ",   "I am sitting"),
            "2sg": ("նստած ես",   "you are sitting (sg)"),
            "3sg": ("նստած է",    "he/she is sitting"),
            "1pl": ("նստած ենք",  "we are sitting"),
            "2pl": ("նստած եք",   "you are sitting (pl)"),
            "3pl": ("նստած են",   "they are sitting"),
        },
    },
    {
        "verb": "նստել",
        "english_infinitive": "to sit down",
        "tense": "resultative past",
        "unit": 9,
        "page": 228,
        "forms": {
            "1sg": ("նստած էի",    "I was sitting"),
            "2sg": ("նստած էիր",   "you were sitting (sg)"),
            "3sg": ("նստած էր",    "he/she was sitting"),
            "1pl": ("նստած էինք",  "we were sitting"),
            "2pl": ("նստած էիք",   "you were sitting (pl)"),
            "3pl": ("նստած էին",   "they were sitting"),
        },
    },
    {
        "verb": "հոգնել",
        "english_infinitive": "to get tired",
        "tense": "resultative present",
        "unit": 9,
        "page": 228,
        "forms": {
            "1sg": ("հոգնած եմ",   "I am tired"),
            "2sg": ("հոգնած ես",   "you are tired (sg)"),
            "3sg": ("հոգնած է",    "he/she is tired"),
            "1pl": ("հոգնած ենք",  "we are tired"),
            "2pl": ("հոգնած եք",   "you are tired (pl)"),
            "3pl": ("հոգնած են",   "they are tired"),
        },
    },

    # ---------------- Unit 10 (hypothetical) ----------------
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "hypothetical future I (կ-)",
        "unit": 10,
        "page": 247,
        "forms": {
            "1sg": ("կգրեմ",   "I would write / I'll write (probably)"),
            "2sg": ("կգրես",   "you would write (sg)"),
            "3sg": ("կգրի",    "he/she would write"),
            "1pl": ("կգրենք",  "we would write"),
            "2pl": ("կգրեք",   "you would write (pl)"),
            "3pl": ("կգրեն",   "they would write"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "hypothetical future I (կ-)",
        "unit": 10,
        "page": 247,
        "forms": {
            "1sg": ("կկարդամ",   "I would read / I'll read (probably)"),
            "2sg": ("կկարդաս",   "you would read (sg)"),
            "3sg": ("կկարդա",    "he/she would read"),
            "1pl": ("կկարդանք",  "we would read"),
            "2pl": ("կկարդաք",   "you would read (pl)"),
            "3pl": ("կկարդան",   "they would read"),
        },
    },
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "hypothetical past I (կ-)",
        "unit": 10,
        "page": 248,
        "forms": {
            "1sg": ("կգրեի",    "I would have written"),
            "2sg": ("կգրեիր",   "you would have written (sg)"),
            "3sg": ("կգրեր",    "he/she would have written"),
            "1pl": ("կգրեինք",  "we would have written"),
            "2pl": ("կգրեիք",   "you would have written (pl)"),
            "3pl": ("կգրեին",   "they would have written"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "hypothetical past I (կ-)",
        "unit": 10,
        "page": 248,
        "forms": {
            "1sg": ("կկարդայի",    "I would have read"),
            "2sg": ("կկարդայիր",   "you would have read (sg)"),
            "3sg": ("կկարդար",     "he/she would have read"),
            "1pl": ("կկարդայինք",  "we would have read"),
            "2pl": ("կկարդայիք",   "you would have read (pl)"),
            "3pl": ("կկարդային",   "they would have read"),
        },
    },
]


# --------------- Non-finite forms (դերբայ / participles) ---------------
# Source: Sakayan's "Grammar Tables" appendix, p359 ("THE INFINITIVE AND
# THE PARTICIPLES") for regular verbs, p354-355 ("TABLE OF IRREGULAR
# VERBS") for the high-frequency irregulars.
#
# Sakayan distinguishes "free" forms (independent use as nouns/adjectives/
# adverbs) and "bound" forms (only inside conjugation paradigms). We
# emit the free forms plus instrumental and negative — bound participles
# (`-ում` present and `-ել` past) are dropped because they don't have
# standalone meaning; the user already knows them through the finite
# tense paradigms (e.g. "գրում եմ" comes from the bound `գրում`).
#
# `instrumental` (-ելով) isn't in the appendix table but is widely used
# as an adverbial converb ("by writing") — included because it's needed
# for productive speech.
PARTICIPLES: list[dict] = [
    {
        "verb": "գրել",
        "english_infinitive": "to write",
        "tense": "participles",
        "unit": 12,  # appendix
        "page": 359,
        "forms": {
            "infinitive":   ("գրել",    "to write"),
            "active":       ("գրող",    "writer / one who writes"),
            "past":         ("գրած",    "written / having written"),
            "synchronic":   ("գրելիս",  "while writing"),
            "future":       ("գրելու",  "going to write / about to write"),
            "negative":     ("գրի",     "[negative participle — appears in 'չեմ գրի' I won't write]"),
            "instrumental": ("գրելով",  "by writing / through writing"),
        },
    },
    {
        "verb": "կարդալ",
        "english_infinitive": "to read",
        "tense": "participles",
        "unit": 12,
        "page": 359,
        "forms": {
            "infinitive":   ("կարդալ",     "to read"),
            "active":       ("կարդացող",   "reader / one who reads"),
            "past":         ("կարդացած",   "read / having read"),
            "synchronic":   ("կարդալիս",   "while reading"),
            "future":       ("կարդալու",   "going to read / about to read"),
            "negative":     ("կարդա",      "[negative participle — 'չեմ կարդա' I won't read]"),
            "instrumental": ("կարդալով",   "by reading / through reading"),
        },
    },
    {
        "verb": "ունենալ",
        "english_infinitive": "to have",
        "tense": "participles",
        "unit": 12,
        "page": 354,
        "forms": {
            "infinitive":   ("ունենալ",     "to have"),
            "active":       ("ունեցող",     "owner / one who has"),
            "past":         ("ունեցած",     "had / possessed"),
            "synchronic":   ("ունենալիս",   "while having"),
            "future":       ("ունենալու",   "going to have / about to have"),
            "negative":     ("ունենա",      "[negative — 'չեմ ունենա' I won't have]"),
            "instrumental": ("ունենալով",   "by having / through having"),
        },
    },
    {
        "verb": "լինել",
        "english_infinitive": "to be",
        "tense": "participles",
        "unit": 12,
        "page": 351,
        "forms": {
            "infinitive":   ("լինել",     "to be"),
            "active":       ("եղող",      "one who is / being"),
            "past":         ("եղած",      "having been / former"),
            "synchronic":   ("լինելիս",   "while being"),
            "future":       ("լինելու",   "going to be / about to be"),
            "negative":     ("լինի",      "[negative — 'չեմ լինի' I won't be]"),
            "instrumental": ("լինելով",   "by being / through being"),
        },
    },
    {
        "verb": "գալ",
        "english_infinitive": "to come",
        "tense": "participles",
        "unit": 12,
        "page": 354,
        "forms": {
            "infinitive":   ("գալ",       "to come"),
            "active":       ("եկող",      "comer / the one coming"),
            "past":         ("եկած",      "having come / arrived"),
            "synchronic":   ("գալիս",     "while coming / on arriving"),
            "future":       ("գալու",     "going to come / about to come"),
            "negative":     ("գա",        "[negative — 'չեմ գա' I won't come]"),
            "instrumental": ("գալով",     "by coming / through coming"),
        },
    },
    {
        "verb": "տեսնել",
        "english_infinitive": "to see",
        "tense": "participles",
        "unit": 12,
        "page": 354,
        "forms": {
            "infinitive":   ("տեսնել",      "to see"),
            "active":       ("տեսնող",      "viewer / one who sees"),
            "past":         ("տեսած",       "having seen / seen"),
            "synchronic":   ("տեսնելիս",    "while seeing / on seeing"),
            "future":       ("տեսնելու",    "going to see / about to see"),
            "negative":     ("տեսնի",       "[negative — 'չեմ տեսնի' I won't see]"),
            "instrumental": ("տեսնելով",    "by seeing / through seeing"),
        },
    },
    {
        "verb": "ուտել",
        "english_infinitive": "to eat",
        "tense": "participles",
        "unit": 12,
        "page": 354,
        "forms": {
            "infinitive":   ("ուտել",      "to eat"),
            "active":       ("ուտող",      "eater / one who eats"),
            "past":         ("կերած",      "eaten / having eaten"),
            "synchronic":   ("ուտելիս",    "while eating"),
            "future":       ("ուտելու",    "going to eat / about to eat"),
            "negative":     ("ուտի",       "[negative — 'չեմ ուտի' I won't eat]"),
            "instrumental": ("ուտելով",    "by eating / through eating"),
        },
    },
    {
        "verb": "տալ",
        "english_infinitive": "to give",
        "tense": "participles",
        "unit": 12,
        "page": 354,
        "forms": {
            "infinitive":   ("տալ",      "to give"),
            "active":       ("տվող",     "giver / one who gives"),
            "past":         ("տված",     "given / having given"),
            "synchronic":   ("տալիս",    "while giving / on giving"),
            "future":       ("տալու",    "going to give / about to give"),
            "negative":     ("տա",       "[negative — 'չեմ տա' I won't give]"),
            "instrumental": ("տալով",    "by giving / through giving"),
        },
    },
    # --- 14 more irregular verbs from Sakayan appendix p354-355 ---
    {
        "verb": "անել", "english_infinitive": "to do / to make",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("անել",     "to do / to make"),
            "active":       ("անող",     "doer / one who does"),
            "past":         ("արած",     "done / made (irregular: aorist արեցի)"),
            "synchronic":   ("անելիս",   "while doing"),
            "future":       ("անելու",   "going to do / about to do"),
            "negative":     ("անի",      "[negative — 'չեմ անի' I won't do]"),
            "instrumental": ("անելով",   "by doing / through doing"),
        },
    },
    {
        "verb": "առնել", "english_infinitive": "to take / to buy",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("առնել",     "to take / to buy"),
            "active":       ("առնող",     "taker / buyer"),
            "past":         ("առած",      "taken / bought (aorist առա)"),
            "synchronic":   ("առնելիս",   "while taking / while buying"),
            "future":       ("առնելու",   "going to take / about to take"),
            "negative":     ("առնի",      "[negative — 'չեմ առնի' I won't take]"),
            "instrumental": ("առնելով",   "by taking / through taking"),
        },
    },
    {
        "verb": "ասել", "english_infinitive": "to say / to tell",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("ասել",     "to say / to tell"),
            "active":       ("ասող",     "speaker / one who says"),
            "past":         ("ասած",     "said / told (aorist ասացի)"),
            "synchronic":   ("ասելիս",   "while saying / on saying"),
            "future":       ("ասելու",   "going to say / about to say"),
            "negative":     ("ասի",      "[negative — 'չեմ ասի' I won't say]"),
            "instrumental": ("ասելով",   "by saying / through saying"),
        },
    },
    {
        "verb": "բանալ", "english_infinitive": "to open",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("բանալ",      "to open"),
            "active":       ("բացող",      "opener (irregular present-stem բաց-)"),
            "past":         ("բացած",      "opened"),
            "synchronic":   ("բանալիս",    "while opening"),
            "future":       ("բանալու",    "going to open / about to open"),
            "negative":     ("բանա",       "[negative — 'չեմ բանա' I won't open]"),
            "instrumental": ("բանալով",    "by opening / through opening"),
        },
    },
    {
        "verb": "բերել", "english_infinitive": "to bring",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("բերել",     "to bring"),
            "active":       ("բերող",     "one who brings"),
            "past":         ("բերած",     "brought (aorist բերեցի/բերի)"),
            "synchronic":   ("բերելիս",   "while bringing"),
            "future":       ("բերելու",   "going to bring / about to bring"),
            "negative":     ("բերի",      "[negative — 'չեմ բերի' I won't bring]"),
            "instrumental": ("բերելով",   "by bringing / through bringing"),
        },
    },
    {
        "verb": "դառնալ", "english_infinitive": "to become / to turn",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("դառնալ",     "to become / to turn"),
            "active":       ("դարձող",     "one who becomes (aorist stem դարձ-)"),
            "past":         ("դարձած",     "become / turned"),
            "synchronic":   ("դառնալիս",   "while becoming"),
            "future":       ("դառնալու",   "going to become / about to become"),
            "negative":     ("դառնա",      "[negative — 'չեմ դառնա' I won't become]"),
            "instrumental": ("դառնալով",   "by becoming / through becoming"),
        },
    },
    {
        "verb": "դնել", "english_infinitive": "to put / to place",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("դնել",     "to put / to place"),
            "active":       ("դնող",     "one who places"),
            "past":         ("դրած",     "put / placed (aorist դրեցի/դրի, stem դր-)"),
            "synchronic":   ("դնելիս",   "while putting / while placing"),
            "future":       ("դնելու",   "going to put / about to put"),
            "negative":     ("դնի",      "[negative — 'չեմ դնի' I won't put]"),
            "instrumental": ("դնելով",   "by putting / through placing"),
        },
    },
    {
        "verb": "ելնել", "english_infinitive": "to go out / to rise",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("ելնել",     "to go out / to rise"),
            "active":       ("ելնող",     "one who goes out"),
            "past":         ("ելած",      "gone out / risen (aorist ելա, stem ել-)"),
            "synchronic":   ("ելնելիս",   "while going out / while rising"),
            "future":       ("ելնելու",   "going to go out / about to go out"),
            "negative":     ("ելնի",      "[negative — 'չեմ ելնի' I won't go out]"),
            "instrumental": ("ելնելով",   "by going out / through rising"),
        },
    },
    {
        "verb": "զարկել", "english_infinitive": "to hit / to strike",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("զարկել",     "to hit / to strike"),
            "active":       ("զարկող",     "hitter / striker"),
            "past":         ("զարկած",     "hit / struck"),
            "synchronic":   ("զարկելիս",   "while hitting / while striking"),
            "future":       ("զարնելու",   "going to hit (note: irregular զարն- stem in future)"),
            "negative":     ("զարկի",      "[negative — 'չեմ զարկի' I won't hit]"),
            "instrumental": ("զարկելով",   "by hitting / through striking"),
        },
    },
    {
        "verb": "ընկնել", "english_infinitive": "to fall",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("ընկնել",     "to fall"),
            "active":       ("ընկնող",     "one who falls"),
            "past":         ("ընկած",      "fallen (aorist ընկա, stem ընկ-)"),
            "synchronic":   ("ընկնելիս",   "while falling"),
            "future":       ("ընկնելու",   "going to fall / about to fall"),
            "negative":     ("ընկնի",      "[negative — 'չեմ ընկնի' I won't fall]"),
            "instrumental": ("ընկնելով",   "by falling / through falling"),
        },
    },
    {
        "verb": "թողնել", "english_infinitive": "to leave / to allow",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("թողնել",     "to leave / to allow"),
            "active":       ("թողնող",     "one who leaves / allows"),
            "past":         ("թողած",      "left / allowed (aorist թողեցի/թողի)"),
            "synchronic":   ("թողնելիս",   "while leaving / while allowing"),
            "future":       ("թողնելու",   "going to leave / about to leave"),
            "negative":     ("թողնի",      "[negative — 'չեմ թողնի' I won't leave]"),
            "instrumental": ("թողնելով",   "by leaving / through allowing"),
        },
    },
    {
        "verb": "լալ", "english_infinitive": "to cry / to weep",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("լալ",      "to cry / to weep"),
            "active":       ("լացող",    "crier / one who cries (stem լաց-)"),
            "past":         ("լացած",    "cried (aorist լացեցի/լացի)"),
            "synchronic":   ("լալիս",    "while crying / while weeping"),
            "future":       ("լալու",    "going to cry / about to cry"),
            "negative":     ("լացի",     "[negative — 'չեմ լացի' I won't cry]"),
            "instrumental": ("լալով",    "by crying / through crying"),
        },
    },
    {
        "verb": "լվանալ", "english_infinitive": "to wash",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("լվանալ",     "to wash"),
            "active":       ("լվացող",     "washer / one who washes (stem լվաց-)"),
            "past":         ("լվացած",     "washed (aorist լվացի)"),
            "synchronic":   ("լվանալիս",   "while washing"),
            "future":       ("լվալու",     "going to wash / about to wash"),
            "negative":     ("լվանա",      "[negative — 'չեմ լվանա' I won't wash]"),
            "instrumental": ("լվանալով",   "by washing / through washing"),
        },
    },
    {
        "verb": "տանել", "english_infinitive": "to take (away) / to lead",
        "tense": "participles", "unit": 12, "page": 354,
        "forms": {
            "infinitive":   ("տանել",     "to take (away) / to lead"),
            "active":       ("տանող",     "one who takes (away) / leader"),
            "past":         ("տարած",     "taken (away) / led (aorist տարա, stem տար-)"),
            "synchronic":   ("տանելիս",   "while taking / while leading"),
            "future":       ("տանելու",   "going to take / about to take"),
            "negative":     ("տանի",      "[negative — 'չեմ տանի' I won't take]"),
            "instrumental": ("տանելով",   "by taking / through leading"),
        },
    },
]

PARADIGMS.extend(PARTICIPLES)


# Possessive adjectives — included because Sakayan's Unit 3 treats them
# as a paradigm even though they're not verb conjugations. Six items,
# same shape as a 1sg-3pl table, with a 6sg/6pl split for "your" forms.
POSSESSIVE_ADJECTIVES = {
    "verb": "—",  # not a verb
    "english_infinitive": "possessive adjectives",
    "tense": "possessive (Unit 3)",
    "unit": 3,
    "page": 79,
    "forms": {
        "1sg":  ("իմ",      "my"),
        "2sg":  ("քո",      "your (sg/informal)"),
        "3sg":  ("իր",      "his/her/its (one's own)"),
        "3sg2": ("նրա",     "his/her/its (someone else's)"),
        "1pl":  ("մեր",     "our"),
        "2pl":  ("ձեր",     "your (pl/formal)"),
        "3pl":  ("իրենց",   "their (one's own)"),
        "3pl2": ("նրանց",   "their (someone else's)"),
    },
}
PARADIGMS.append(POSSESSIVE_ADJECTIVES)
