# Dum-Tragut IPA transcriptions — spelling↔pronunciation deviations

Words whose attested IPA in Dum-Tragut, *Armenian: Modern Eastern
Armenian* (Benjamins 2009) **differs from the regular reading of
their spelling**. Harvested from the extracted text layer (nearly all
from Chapter 1, Phonology, corpus pages 29–75), then filtered: rows
whose IPA is fully predicted by ordinary reading rules are excluded.

*Not* counted as deviations (canonicalized away by the filter):
schwa epenthesis (never written), initial/medial glide readings of
ե/ո/և and intervocalic glides, nasal place assimilation, ɾ/r and ʋ/v
notation, liaison/stress/intonation marks, morpheme hyphens. What
remains is the real divergence inventory: voiced-stop
devoicing/aspiration (մարդ [mɑɾtʰ]), ղ→[χ] clusters (աղջիկ
[ɑχtʃʰik]), հ-loss (աշխարհ [ɑʃχɑɾ]), վ→[f] (հարավ [hɑɾɑf]), etc.

**Regenerate:** `python3 dumtragut/harvest_ipa.py` (rewrites this file
and `dumtragut/out/ipa_index.tsv`). The TSV keeps **all** bound rows —
regular ones included — occurrence-level with citation-ready y-ranges
and a `deviant` column (`deviant` / `regular` / `artifact`); this file
is the deduplicated deviations-only human view.

Reading notes:

- **Pages are corpus pages** (PDF pages, as cited everywhere in this
  workspace: `dumtragut pN`). Book-print page = corpus page − 17
  (corpus p40 = book p23).
- **Byte-faithful.** Words are verbatim corpus bytes, including
  apparent book typos (p36 `ռարդիո` for ռադիո), stray Latin glyphs
  inside Armenian-font spans (p55 `hագցնել`, p40 `անդjադար`), and the
  1922–40 reformed-orthography demonstration spellings on p29
  (`վորակ`, `յերկիր`, …). Don't "fix" entries here — the Stop-hook /
  `citation-check` verify against these bytes.
- **Aspiration** is normally superscript `ʰ`; a few pages set a plain
  `h` (e.g. p71 `[kaɾthatsh]`) — kept as printed.
- **Appendix codepoint quirks** (pp52, 694, 698–699): the PDF text
  layer encodes schwa as Cyrillic `ә` (U+04D9, not ə U+0259) and ʃ as
  `∫` (U+222B) in a few Regular-font IPA spans (`[mәkәɾtit∫h]`).
  Rendered glyphs look right; the codepoints differ. Kept byte-faithful
  — mind this when substring-searching IPA across those rows.
- **Prosody marks** (per `dumtragut/phonetic.py`): ◌́ acute = primary
  stress, ◌̂ circumflex = interrogative intonation, `‿` = enclitic
  liaison.
- A word may carry **several IPA variants** — the book itself prints
  different realisations in different sections. The filter judges each
  variant separately: որդի keeps its devoiced [ʋɔɾtʰi] here while its
  spelling-pronunciation [ʋɔɾdi] (p37) stays TSV-only as `regular`.
- `ʋ` (hooked script-v, labiodental approximant) is the corrected
  decode of the glyph earlier read as ʔ — see the 2026-07-02 note in
  `dumtragut/phonetic.py`.
- **`variant` / `book-preferred variant` notes**: where the book gives
  several IPA for one word (`[əs-kəs-ɛts] or preferably [skə-sɛl]`,
  p52 schwa-epenthesis section), each variant is its own row; the
  first-printed one is *not* always the recommended one — trust the
  note. Occasionally the first-printed variant is itself a book typo
  (p52 սկսել `[əs-kəs-ɛts]`, շտկել `[əʃ-kət-ɛl]`).
- **Headwords are whatever the book transcribed** — mostly citation
  forms, but also inflected/negated/derived demo forms (կորոշեմ
  "I shall decide", Աննայի "Anna's") and one hypocoristic from the
  name-formation appendix (Մակո p699). An occasional Armenian glyph
  appears *inside* an IPA (p54 `[հəɾ-məʃ-tə-kɛl]`) — same
  byte-faithful policy.

## Words — 208 entries

| word | translit | IPA | gloss | pages |
|------|----------|-----|-------|-------|
| gթալ | gt’al | [gətʰɑl] | to have mercy | p35 |
| hագցնել | hagc’nel | [hɑg-tsʰə-nɛl] | to dress somebody, to put on somebody | p55 |
| oդ | ōd | [ɔtʰ] | air | p40 |
| աբխազ | abxaz | [ɑpʰχɑz] | Abkhaz | p41 |
| ալբոմ | albom | [ɑljbɔm] | album | p38, p46 |
| ալմանախ | almanax | [ɑljmɑnɑχ] | almanac | p46 |
| աղբ | ałb | [aχp] | dirt | p41 |
| աղբյուր | ałbyur | [ɑχpjuɾ] | spring | p41 |
| աղջիկ | ałjik | [ɑχtʃʰik] | girl | p41, p44 |
| ամբողջ | ambołj | [ɑmbɔχtʃʰ] | whole, entire | p44 |
| ամենաարդար | amena-ardar | [ɑ.mɛ.nɑ.ɑɾ.tʰɑɾ] | the fairest | p63 |
| ամենաերկար | amena-erkar | [ɑmɛnɑjɛɾkʰɑɾ] | the longest | p32 |
| անբիծ | anbic | [ɑmbits] | spotless | p44 |
| անգամ | angam | [ɑŋkʰɑm] | times | p40, p42 |
| անդjադար | andadar | [ɑntʰɑtʰɑɾ] | unceasing | p40 |
| անդամ | andam | [ɑntʰɑm] | member | p40, p42 |
| անկաերլի | ankareli | [ɑŋkɑɾɛli] | impossible | p36 |
| անմեղ | anmeł | [ɑmmɛʁ] | innocent | p44 |
| անջնջելի | anjnjeli | [ɑɲdʒədʒɛli] | indestructible | p36 |
| աշխարհ | ašxarh | [ɑʃχɑɾ] | world | p45 |
| աշխարհայացք | ašxarhayac’k’ | [ɑʃχɑɾhɑjɑtʰskʰ] | outlook | p45 |
| ապերջանիկ | ap-erĴanik | [ɑpɛɾtʃʰɑnik] | unhappy | p32 |
| ապշել | apšel | [ɑpʰʃɛl] | to be surprised | p40 |
| ապստամբել | apstambel | [ɑpʰstɑmbel] | to revolt | p40 |
| աջ | aj | [ɑtʃʰ] | right | p40, p43 |
| առաջ | ar˚aj | [ɑrɑtʃʰ] | before, in front of | p43 |
| առաջին | ar˚ajin | [ɑrɑtʃʰin] | first | p43 |
| առաջնորդ | ar˚ajnord | [ɑrɑdʒnɔɾtʰ] | first; leader | p42 |
| առողջ | ar˚ołj | [ɑrɔχtʃʰ] | healthy | p44 |
| ավագ | avag | [ɑvɑkʰ] | elder, senior | p43 |
| ավտո | avto | [ɑftɔ] | auto-; car | p45 |
| արբել | arbel | [ɑɾpʰɛl] | to get drunk | p41 |
| արդար | ardar | [ɑɾtʰɑɾ] | fair, just | p41 |
| արդեն | arden | [ɑɾtʰɛn] | already | p39, p41 |
| արծաթյա | arcat’ya | [ɑɾtsɑtjɑ] | silvern | p39 |
| արհամարհել | arhamarhel | [ɑɾhɑmɑɾəl] | to despise, to scorn | p45 |
| արձակ | arjak | [ɑɾtsʰɑk] | prose | p43 |
| արձակուրդ | arjakurd | [ɑɾdzɑkuɾtʰ] | holiday, vacation | p42 |
| արջ | arj | [ɑɾtʃʰ] | bear | p39, p43 |
| բարդ | bard | [bɑɾtʰ] | complex | p39, p41 |
| բարձ | barj | [bɑɾtsʰ] | cushion | p43 |
| բարձր | barjr | [bɑɾtsʰɾ] | high | p43 |
| բերդ | berd | [bɛɾtʰ] | fortress | p41 |
| բոլշեվիկ | bolšewik | [boljʃɛvik] | Bolshevik | p46 |
| բուրդ | burd | [buɾtʰ] | wool | p41 |
| բռնցքամարտ | br˚nc’k’amart | [bər-nəts-kʰɑmɑɾt] | boxing | p54 |
| բրդել | brdel | [bəɾtʰɛl] | to crumble | p41 |
| Գաբրիել | Gabriel | [gɑpʰɾi(j)ɛl] | Gabriel | p41 |
| գրիր | grir!, | [uʁɑki] | send | p45 |
| դադար | dadar | [dɑtʰɑɾ] | pause, rest | p42 |
| դադրել | dadrel | [dɑtʰɾɛl] | to tire, to become tired | p42 |
| դաղձ | dałj | [dɑχtsʰ] | mint | p43 |
| դաստիարկել | dastiarkel | [dɑstji(j)ɑɾkɛl] | to educate | p46 |
| դարբին | darbin | [dɑɾpʰin] | smith | p41 |
| դարբնոց | darbnoc’ | [dɑɾpʰnɔtsʰ] | smithy | p39 |
| դարձյալ | darjyal | [dɑɾtsʰjɑl] | again | p39 |
| դեղձ | dełj | [dɛχtsʰ] | peach | p41, p43 |
| դեղձան | dełjan | [dɛχtsʰɑn] | yellowish; canary bird | p43 |
| դեղնուց | dełnuc’ | [dɛʁnutʰs] | yolk | p58 |
| դերձակ | derjak | [dɛɾtsʰɑk] | tay-lor | p43 |
| դերձան | derjan | [dɛɾtsʰɑn] | needleful, string | p43 |
| դիպլոմ | diploma | [djiplɔmɑ] | diplom | p46 |
| դրդել | drdel | [dəɾtʰɛl] | to incite | p41 |
| եղբայր | ełbayr | [jɛχpɑjɾ] | brother | p41 |
| եղբայրս | ełbayrs | [jɛχpɑjɾ-əs] | my brother | p55 |
| եղբորորդի | ełborordi | [jɛχpɔɾɔɾtʰi] | fraternal nephew; brother’s son | p33 |
| երբ | erb | [jɛɾpʰ] | when | p41 |
| երբ | erb | [jɛpʰ] | when | p45 |
| երգ | erg | [jɛɾkʰ] | song | p39 |
| երգել | ergel | [jɛɾkʰɛl] | to sing | p42 |
| երգիչ | ergič’ | [jɛɾkʰitʃʰ] | singer | p39 |
| երգում եմ | ergúm em | [jɛɾkʰúm‿ɛm] | I sing | p65 |
| երդ | erd | [jɛɾtʰ] | roof | p41 |
| երրորդ | errord | [jɛɾɾɔɾtʰ] | third | p42 |
| զագս | zags | [zɑkʰs] | regis-ter office | p43 |
| զարդ | zard | [zɑɾtʰ] | ornament | p35, p42 |
| զերդ | zerd | [zɛɾtʰ] | as, like | p42 |
| զղջալ | złjal | [zɛʁdʒɑl] | to regret | p44 |
| զնգզնգոց | zngzngoc’ | [zəŋg-zəŋ-gɔtʰs] | tinkle | p54 |
| զուգել | zugel | [zukʰɛl] | to dress up | p43 |
| էգ | ēg | [ɛkʰ] | female | p40, p43 |
| ընդահնուր | ěndhanur | [əntʰhɑnuɾ] | general | p42 |
| ընդամենը | ěndameně | [əntʰɑmɛnə] | in all, total | p42 |
| ընդունել | ěndunel | [əntʰunɛl] | to accept | p42 |
| թագավոր | t’agavor | [tʰɑkʰɑvɔɾ] | king | p43 |
| թարգմանիչ | t’argmanič’ | [tʰɑɾkʰmɑnitʃʰ] | interpreter | p42 |
| թերևս | t’erews | [tɛɾɛʋəs] | perhaps | p55 |
| թրջել | t’rjel | [tʰəɾtʃʰɛl] | to wet | p43 |
| ժողովուրդ | žołovurd | [ʒɔʁɔvuɾtʰ] | people | p42 |
| ժողովրդի | žołovrd-i | [ʒɔʁɔvəɾtʰi] |  | p61 |
| իբր | ibr | [ipʰɾ] | as, like | p41 |
| լերդ | lerd | [lɛɾtʰ] | liver; convolution | p42 |
| լյարդ | lyard | [ljɑɾtʰ] | liver | p42 |
| խաբել | xabel | [χɑpʰɛl] | to cheat | p40, p41 |
| խնդիր | xndir | [χəntʰiɾ] | problem, question; problem | p40, p42 |
| խոնարհ | xonarh | [χɔnɑɾ] | humble | p45 |
| խորհուրդ | xorhurd | [χɔɾuɾtʰ] | advice | p45 |
| խուրձ | xurj | [χuɾtʰs] | bundle | p43 |
| ծագել | cagel | [tsɑkʰɛl] | to rise, to origin | p43 |
| կuմիտեում | komite-um | [kɔmitɛjum] |  | p64 |
| կարագ | karag | [kɑɾɑkʰ] | butter | p43 |
| կարգ | karg | [kɑɾkʰ] | order, system | p42 |
| կարդալ | kardal | [kɑɾtʰɑl] | to read | p42 |
| կենդանի | kendani | [kɛntʰɑni] | alive; animal | p40, p42 |
| կերգեմ | kergem | [kɛɾkʰɛm] | I shall sing | p32 |
| կերգեմ | kergem | [kəjɛɾkʰɛm] | I shall sing | p32 |
| կինոյից | kino-y-ic’ | [kinojitʰs] |  | p64 |
| կոկորդ | kokord | [kɔkɔɾtʰ] | throat | p42 |
| կոմիտերն | komintern | [kɔmintɛrn] | komintern | p44 |
| կուլտուրա | kultura | [kuljtuɾɑ] | culture | p46 |
| հագնել | hagnel | [hɑkʰnɛl] | to wear, to put on | p43 |
| հագնել | hagnel | [hɑkʰ-nɛl] | to wear | p54 |
| հակաեկեղցական | haka-ekełec’akan | [hɑkɑjɛkɛʁɛtsʰɑkɑn] | anticlerical | p32 |
| Հակոբ | Hakob | [hɑkɔpʰ] | Hakob | p41 |
| հակոբենի | hakobeni | [hɑkɔpʰɛni] | winter cherry (tree) | p41 |
| հաղորդ | hałord | [hɑʁɔɾtʰ] | participating; social | p42 |
| համբարձում | hambarjum | [hɑmbɑɾtsʰum] | ascension | p43 |
| համբերել | hamberel | [hɑmpʰɛɾɛl] | to be patient | p41 |
| համբույր | hambuyr | [hɑmpʰujɾ] | kiss | p40, p41 |
| հանդերձ | handerj | [hɑndɛɾtsʰ] | with; clothes | p43 |
| հաջորդ | hajord | [hɑdʒɔɾtʰ] | next | p43, p55 |
| հարավ | harav | [hɑɾɑf] | south | p45 |
| հարբել | harbel ­ | [harpʰɛl] | to drink, to get drunk | p41 |
| հարձակվել | harjakvel | [hɑɾtʰsɑkvɛl] | to attack | p43 |
| հոգի | hogi | [hɔkʰi] | soul | p40, p43 |
| հոգնել | hognel | [hɔkʰnɛl] | to get tired | p43 |
| հրմշտկել | hrmštkel | [հəɾ-məʃ-tə-kɛl] | to jostle | p54 |
| ձագ | jag | [dzɑkʰ] | youngling | p43 |
| ձիգ | jig | [dzikʰ] | tight, stretched | p43 |
| ճանապարհ | čanaparh | [tʃɑnɑpɑɾ] | way, path | p45 |
| ճմրթված | čmrt’vac | [tʃə-məɾt-vɑts] | crinkled, crumpled | p54 |
| ճվտկել | čvtkel | [tʃəv-tə-kel] | to prune | p53 |
| ճրագ | črag | [tʃəɾɑkʰ] | lamp | p43 |
| մարագ | marag | [mɑɾɑkʰ] | hay-loft | p43 |
| մարգարե | margare | [mɑɾkʰɑɾɛ] | prophet | p42, p57 |
| մարգարեանալ | margare-anal | [mɑɾkh-ɑɾɛjɑnɑl] | to prophesy | p57 |
| մարգարեի | margare-i | [mɑɾkʰɑɾɛji] |  | p57 |
| մարդ | mard | [mɑɾtʰ] | man, person | p42 |
| մարմնամարզիկ | marmn-a-marzik | [mɑɾmənəməɾzik] | gymnast | p59 |
| մեծ ծով | mec cov | [mɛts‿tsov] | big sea | p47 |
| մեջ | mej | [mɛtʃʰ] | in | p43 |
| մեջընդմեջ | mejěndmej | [mɛdʒəntʰmɛdʒ] | some-times, from time to time | p57 |
| մուգ | mug | [mukʰ] | dark | p43 |
| մտցնել | mtc’nel | [mət-tsʰɛ-nɛl] | to bring in | p53 |
| յուրականչյուր | yurak’ anč’ yur | [juɾɑkʰɑɲtʃʰjuɾ] | each | p37 |
| նավթ | navt’ | [nɑftʰ] | oil, petroleum | p45 |
| նկարչություն | nkarč’ut’yun | [nəkɑɾtʰʃutʰjun] | painting | p58 |
| նյարդ | nyard | [njɑɾtʰ] | nerve | p42 |
| նորոգել | norogel | [nɔɾɔkʰɛl] | renew, renovate | p43 |
| նուրբ | nurb | [nuɾpʰ] | fine, delicate | p41 |
| շաբաթ | šabat’ | [ʃɑpʰɑtʰ] | week, Saturday | p41 |
| շաղգամ | šałgam | [ʃɑχkɑm] | turnip | p41 |
| շաղկամ | šałkam | [ʃɑχkɑm] | turnip | p43 |
| շնորհ | šnorh | [ʃnɔɾ] | mercy | p45 |
| շոգ | šog | [ʃɔkʰ] | hot | p43 |
| շտկել | štkel | [əʃ-kət-ɛl] | to repair; to straighten | p52 |
| ոձ | ōj | [ɔtsʰ] | snake | p43 |
| ողբալ | ołbal | [ʋɔχbɑl] | to lament | p41 |
| ողջ | ołj | [ʋɔχtʃʰ] | entire, whole | p44 |
| ոջիլ | ojil | [ʋɔtʃʰil] | louse | p40, p43 |
| որբ | orb | [ʋɔɾpʰ] | orphan | p39, p41 |
| որդ | ord | [ʋɔɾtʰ] | worm | p42 |
| որդի | ordi | [ʋɔɾtʰi] | son | p33, p42 |
| որձ | orj | [ʋɔɾtʰs] | male | p43 |
| որովհետև | orovhetew | [ʋɔɾɔhɛtɛʋ] | because, since | p37 |
| ուսուցչուհի | usuc’č’uhi | [usutʰstʰʃuhi] | female teacher | p59 |
| ուրբաթ | urbat’ | [uɾpʰɑtʰ] | Friday | p41 |
| չերգեցի | č’-ergec’i | [tʃʰɛɾkʰɛtsʰi] | I did not sing | p32 |
| չվի | č’v-i | [tʰʃəvi] |  | p61 |
| պատարագ | patarag | [pɑtɑɾɑkʰ] | holy mass | p43 |
| պարգև | pargew | [pɑɾkʰɛʋ] | gift | p37, p42 |
| պարերգ | par-erg | [pɑɾɛɾkʰ] | dance song | p32 |
| պարտիական | partiakan | [pɑɾtjiɑkɑn] | party; party member | p46 |
| ջարդ | jard | [dʒɑɾtʰ] | slaughter | p42 |
| ջութ | jut’ | [dzutʰ] | jute | p36 |
| ռարդիո | radio | [rɑdi(j)ɔ] | radio | p36 |
| սարդ | sard | [sɑɾtʰ] | spider | p35 |
| սլկվել | slkvel | [səlk(ə)-vel] | to slip | p53 |
| սկսել | sksel | [əs-kəs-ɛts] | to begin | p52 |
| սուգ | sug | [sukʰ] | grief | p43 |
| ստրկացնել | strkac’nel | [stʰə-rə-katsʰnɛl] | to enslave | p53 |
| սրբել | srbel | [səɾpʰɛl] | to clean | p41 |
| վալս | vals | [vɑljs] | waltz | p46 |
| վաղորդյան | vałordyan | [vɑʁɔɾtʰjɑn] | in the morning, early | p42 |
| վարդ | vard | [vɑɾtʰ] | rose | p42 |
| վարդապետ | vardapet | [vɑɾtʰɑpɛt] | master, Vardapet | p42 |
| վարձակ | varjak | [vɑɾtsʰɑk] | singer; whore | p43 |
| վերակուի | verarku-i | [vɛɾɑɾkuji] |  | p61 |
| վերջ | verj | [vɛɾtʃʰ] | end | p43 |
| վերջին | verjin | [vɛɾtʃʰin] | last | p39 |
| վրդովել | vrdovel | [vəɾtʰɔvɛl] | to perturb | p42 |
| վրձին | vrjin | [vəɾtsʰin] | brush | p43 |
| տասներկու | tasnerku | [tɑsənɛɾkʰu] |  | p32 |
| տեգր | tegr | [tɛkh(ə)ɾ] | husband’s brother | p43 |
| տեղ | teł | [tɛχ] | place | p35 |
| տիեզերք | tiezerk’ | [tji(j)ɛzɛɾkʰ] | cosmos, universe | p46 |
| տրտմություն | trtmut’yun | [tʰəɾt-mu-tʰjun] | sadness | p53 |
| տրտնջալ | trtnjal | [təɾ-təɲʒɑl] | to grumble, to complain | p54 |
| փորձ | p’orj | [pʰɔɾtsʰ] | test, attempt; արջ arj [ɑɾtʃʰ]; test | p39, p43 |
| քաջք | kajk’ | [kʰɑtʃʰkʰ] | demons | p43 |
| Քերոբ | k’erob | [kʰɛɾɔpʰ] | K’erob | p41 |
| օգնել | ognel | [ɔkʰnɛl] | to help | p33, p43 |
| օգուտ | ōgut | [ɔkʰut] | favour | p43 |
| օդ | ōd | [ɔtʰ] | air | p42 |
| օդանավ | ōdanav | [ɔtʰɑnɑv] | plane | p33 |
| օձ | ōj | [ɔtsʰ] | snake | p40 |
| օրիորդ | ōriord | [ɔɾi(j)ɔɾtʰ] | Miss, maid | p42 |
| օրհնել | ōrhnel | [ɔɾnɛl] | to bless | p45 |

## Phrases with a deviating word — 8 entries

Multi-word examples kept because at least one word in them deviates from its spelling (e.g. դուրս → [dus], կարդաց → [kaɾtʰatsʰ]).

| word | translit | IPA | gloss | pages |
|------|----------|-----|-------|-------|
| Անո՛ւշը կարդացել է այս գիրքը | AnÚš-ě kardac’el ē ays girk-ě. | [ɑnúʃə kaɾtʰatsʰɛl‿ɛ ɑjs giɾkʰə] | Anuš has read this book. | p69 |
| Անո՛ւշն է կարդացել այս գիրքը | AnÚš-n kardac’el ē ays girk-ě. | [ɑnúʃən‿ɛ kaɾtʰatsʰɛl ɑjs giɾkʰə] | It is Anuš who read the book | p69 |
| Անո՞ւշը գիրք կարդաց | Anǔš-ě girk’ kardac’? | [ɑnúʃə giɾkʰ kaɾtʰatsʰ] | Did ANUŠ read a book? | p71 |
| Անուշը գի՞րք կարդաց | Anǔš-ě girk’ kardac’? | [ɑnúʃə giɾkh kaɾthatsh] |  | p71 |
| Անուշը գիրք կարդա՞ց | Anuš-ě girk’ kardác’? | [ɑnuʃə giɾkʰ kɑɾtʰɑ̂tsʰ] |  | p71 |
| դուրս եկավ | durs ekav | [dus ɛkɑv] | he came out | p45 |
| Ինչքա՜ն գեղեցիկ է այս աղջիկը | inč’k’ân gełec’ik ē ays ałjik-ě! | [iɲktʃʰkʰɑ̂n gɛʁɛtsʰik‿ɛ ɑjs ɑχtʃʰikə] | This girl îs beautiful! | p74 |
| Սա ի՞նչ է։ Վագ՞ր, թե՞ առյուծ։ | sa ínč’ ē? Vagě´r t’é ar˚juc? | [sɑ ǐɲtʃh‿ɑ vɑkhə̌ɾ thɛ̌ ɑrjuts] |  | p73 |

