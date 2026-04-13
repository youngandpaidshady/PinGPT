#!/usr/bin/env node
/**
 * TrendTok — Carousel Planner
 * 
 * Takes a trending topic and builds a complete slide deck JSON with:
 *   - Dynamic slide count (8-12 based on topic)
 *   - Hybrid art style: atmospheric NB2 AI art + manga-panel treatments
 *   - NB2 prompts per slide
 *   - Text overlay specs per slide
 *   - TikTok caption + hashtags
 * 
 * Usage:
 *   node scripts/carousel_planner.js                              → auto from trending_report.json
 *   node scripts/carousel_planner.js --topic "Top 7 Zenin Members"
 *   node scripts/carousel_planner.js --character gojo
 */

const fs = require('fs');
const path = require('path');

const PINGPT_ROOT = path.resolve(__dirname, '..');
const TRENDING_FILE = path.join(PINGPT_ROOT, 'trending_report.json');
const OUTPUT_FILE = path.join(PINGPT_ROOT, 'carousel_deck.json');
const CHARACTERS_FILE = path.join(PINGPT_ROOT, 'skill_characters.md');

// ─── Slide Style Enum ─────────────────────────────────────────
// HYBRID APPROACH: Mix atmospheric AI art with manga-panel treatments
const SLIDE_STYLES = {
  atmospheric: 'atmospheric',     // Full-color NB2 atmospheric render — stops the scroll
  MANGA_RAW: 'manga_raw',    // High-contrast B&W manga-panel look — raw, authentic
  MANGA_TINTED: 'manga_tint', // Manga panel with single-color tint (red, blue, purple)
  SPLIT_PANEL: 'split_panel', // Half atmospheric / half manga split — best of both
};

// Style assignments by slide type — cover and closer get the atmospheric treatment,
// middle entries alternate between atmospheric and manga for visual rhythm
function assignSlideStyle(slideType, slideIndex, totalSlides) {
  if (slideType === 'COVER') return SLIDE_STYLES.atmospheric;
  if (slideType === 'CLOSER') return SLIDE_STYLES.SPLIT_PANEL;

  // Alternate styles for entries: atmospheric → manga → tinted → atmospheric...
  const styles = [
    SLIDE_STYLES.atmospheric,
    SLIDE_STYLES.MANGA_RAW,
    SLIDE_STYLES.atmospheric,
    SLIDE_STYLES.MANGA_TINTED,
    SLIDE_STYLES.SPLIT_PANEL,
    SLIDE_STYLES.MANGA_RAW,
    SLIDE_STYLES.atmospheric,
    SLIDE_STYLES.MANGA_TINTED,
    SLIDE_STYLES.atmospheric,
    SLIDE_STYLES.MANGA_RAW,
  ];
  return styles[slideIndex % styles.length];
}

// ─── NB2 prompt modifiers per style ───────────────────────────
const STYLE_PROMPT_MODS = {
  [SLIDE_STYLES.atmospheric]: 'atmospheric cel-shaded 2D anime, vibrant color, dual-source dramatic lighting, film grain, Mixed Media cel-shading composite',
  [SLIDE_STYLES.MANGA_RAW]: 'high-contrast black and white manga panel, heavy ink strokes, stark shadows, dynamic speed lines, raw manga aesthetic, screentone texture',
  [SLIDE_STYLES.MANGA_TINTED]: 'manga panel with single dramatic color accent, high-contrast ink style, one bold color wash over black and white, cel-shaded highlights',
  [SLIDE_STYLES.SPLIT_PANEL]: 'split composition half atmospheric color half manga ink, dramatic contrast between styles, dual-reality aesthetic, Mixed Media cel-shading composite',
};

// ─── Text overlay specs per style ─────────────────────────────
const STYLE_TEXT_SPECS = {
  [SLIDE_STYLES.atmospheric]: { font: 'Impact', color: '#FFFFFF', stroke: '#000000', strokeWidth: 4, position: 'center-bottom' },
  [SLIDE_STYLES.MANGA_RAW]: { font: 'Impact', color: '#FFFFFF', stroke: '#000000', strokeWidth: 6, position: 'center' },
  [SLIDE_STYLES.MANGA_TINTED]: { font: 'Impact', color: '#FF3333', stroke: '#000000', strokeWidth: 4, position: 'center-bottom' },
  [SLIDE_STYLES.SPLIT_PANEL]: { font: 'Impact', color: '#FFFFFF', stroke: '#000000', strokeWidth: 5, position: 'center' },
};

// ─── Parse args ───────────────────────────────────────────────
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--topic' && args[i + 1]) opts.topic = args[++i];
    if (args[i] === '--character' && args[i + 1]) opts.character = args[++i];
    if (args[i] === '--slides' && args[i + 1]) opts.slides = parseInt(args[++i]);
  }
  return opts;
}

// ─── Pick best topic from trending report ─────────────────────
function pickTopicFromTrending(trendingReport, preferCharacter) {
  const ready = trendingReport.trending.filter(t => t.auto_prompt_ready);
  if (ready.length === 0) {
    console.error('No PinGPT-ready trending topics found!');
    process.exit(1);
  }

  // If user prefers a character, find a topic featuring them
  if (preferCharacter) {
    const charNorm = preferCharacter.toLowerCase();
    const match = ready.find(t =>
      t.pingpt_characters.some(c => c.toLowerCase().includes(charNorm))
    );
    if (match) return match;
    console.warn(`Character "${preferCharacter}" not found in trending. Using #1 instead.`);
  }

  return ready[0]; // #1 trending PinGPT-ready topic
}

// ─── Determine dynamic slide count ────────────────────────────
function pickSlideCount(topic, characterCount, requestedSlides) {
  if (requestedSlides) return Math.max(5, Math.min(12, requestedSlides));

  const topicLower = topic.toLowerCase();

  // Clan/group rankings → more slides
  if (topicLower.includes('ranking every') || topicLower.includes('clan') || topicLower.includes('member')) {
    return Math.min(12, Math.max(8, characterCount + 2)); // +2 for cover + closer
  }

  // "Who could beat" / "didn't fear" → tighter
  if (topicLower.includes('could beat') || topicLower.includes('fear')) {
    return Math.min(8, Math.max(6, characterCount + 2));
  }

  // "Moments" / "fights" → flexible
  if (topicLower.includes('moment') || topicLower.includes('fight')) {
    return Math.min(12, Math.max(8, 10));
  }

  // Default: 8-10 range
  return Math.min(10, Math.max(8, characterCount + 2));
}

// ─── Build the slide deck ─────────────────────────────────────
function buildDeck(topic, anime, characters, slideCount) {
  const entryCount = slideCount - 2; // minus cover and closer
  const animeName = anime.title_english || anime.title || 'Anime';

  // Pick characters for ranked entries (use PinGPT chars + fill with others)
  const rankedChars = [];
  // Prioritize PinGPT-known characters (we can generate their art)
  const pingptChars = characters.filter(c => c.pingpt_name);
  const otherChars = characters.filter(c => !c.pingpt_name);

  // Fill entries: PinGPT chars first, then others
  const allChars = [...pingptChars, ...otherChars];
  for (let i = 0; i < entryCount && i < allChars.length; i++) {
    rankedChars.push(allChars[i]);
  }

  // If we need more entries, generate generic ones
  while (rankedChars.length < entryCount) {
    rankedChars.push({
      name: `Character ${rankedChars.length + 1}`,
      pingpt_name: null,
      favorites: 0,
    });
  }

  // Build slides
  const slides = [];

  // COVER slide — atmospheric hook
  slides.push({
    slide_num: 1,
    type: 'COVER',
    style: assignSlideStyle('COVER', 0, slideCount),
    title: topic.toUpperCase() + ' >>>',
    character: rankedChars[0]?.pingpt_name || animeName,
    commentary: null,
    prompt_base: `extreme close-up dramatic face shot, intense expression, ${STYLE_PROMPT_MODS[SLIDE_STYLES.atmospheric]}`,
    text_overlay: {
      lines: [topic.toUpperCase(), '>>>'],
      spec: STYLE_TEXT_SPECS[SLIDE_STYLES.atmospheric],
    },
  });

  // ENTRY slides — ranked (countdown: N to 2)
  for (let i = 0; i < entryCount; i++) {
    const rank = entryCount - i;
    const char = rankedChars[i];
    const charName = char.pingpt_name || char.name;
    const style = assignSlideStyle('ENTRY', i, slideCount);
    const isLast = i === entryCount - 1;

    // Generate punchy Gen-Z commentary
    const commentaryPool = [
      `NOBODY TALKS ABOUT THIS ENOUGH`,
      `WENT CRAZY AND DIDN'T LOOK BACK`,
      `THE DISRESPECT TO THIS CHARACTER IS INSANE`,
      `ACTUALLY UNDERRATED FR FR`,
      `CARRIED THE ENTIRE ARC ON THEIR BACK`,
      `PROVED EVERYONE WRONG`,
      `THE GOAT AND I'M NOT ARGUING`,
      `HAD THE HARDEST ENTRANCE IN THE SERIES`,
      `WENT FROM MID TO MENACE REAL QUICK`,
      `LITERALLY CHANGED THE WHOLE GAME`,
    ];

    slides.push({
      slide_num: i + 2,
      type: 'ENTRY',
      style,
      rank,
      character: charName,
      title: `${rank}. ${charName.toUpperCase()}`,
      commentary: commentaryPool[i % commentaryPool.length],
      has_pingpt_dna: !!char.pingpt_name,
      prompt_base: `full-body action pose, ${STYLE_PROMPT_MODS[style]}`,
      text_overlay: {
        lines: [`${rank}. ${charName.toUpperCase()}`, commentaryPool[i % commentaryPool.length]],
        spec: STYLE_TEXT_SPECS[style],
      },
    });
  }

  // CLOSER slide — #1 pick, split-panel hybrid style
  const topChar = rankedChars[entryCount - 1] || rankedChars[0];
  const closerStyle = assignSlideStyle('CLOSER', 0, slideCount);
  slides.push({
    slide_num: slideCount,
    type: 'CLOSER',
    style: closerStyle,
    rank: 1,
    character: topChar?.pingpt_name || topChar?.name || 'Unknown',
    title: `1. ${(topChar?.pingpt_name || topChar?.name || 'UNKNOWN').toUpperCase()}`,
    commentary: 'THE GOAT AND I\'M NOT ARGUING',
    has_pingpt_dna: !!topChar?.pingpt_name,
    prompt_base: `hero shot iconic pose, ${STYLE_PROMPT_MODS[closerStyle]}`,
    text_overlay: {
      lines: [`1. ${(topChar?.pingpt_name || topChar?.name || 'UNKNOWN').toUpperCase()}`, 'THE GOAT AND I\'M NOT ARGUING'],
      spec: STYLE_TEXT_SPECS[closerStyle],
    },
  });

  return slides;
}

// ─── Generate TikTok caption + hashtags ───────────────────────
function generateCaption(topic, animeName) {
  const hooks = [
    'disagree or agree doesn\'t matter',
    'this list is personal don\'t come at me',
    'if you know you know',
    'the last one is gonna make you mad',
    'i know this is gonna start a war in the comments',
    'comment your list below',
  ];

  const caption = `${hooks[Math.floor(Math.random() * hooks.length)]} - #anime #${animeName.replace(/[^a-zA-Z0-9]/g, '').toLowerCase()} #animeedit #animetiktok #weeb`;

  return {
    text: caption,
    hashtags: [
      '#anime',
      `#${animeName.replace(/[^a-zA-Z0-9]/g, '').toLowerCase()}`,
      '#animeedit',
      '#animetiktok',
      '#animelist',
      '#top10anime',
    ],
    sound_suggestion: 'Phonk / dark trap beat (trending audio)',
  };
}

// ─── Main ─────────────────────────────────────────────────────
function main() {
  console.log('═══════════════════════════════════════');
  console.log('  TrendTok — Carousel Planner v1.0');
  console.log('═══════════════════════════════════════\n');

  const opts = parseArgs();

  let topic, anime, characters;

  if (opts.topic) {
    // Custom topic mode — use provided topic
    topic = opts.topic;
    anime = { title: 'Custom', title_english: 'Custom' };
    characters = [];
    console.log(`[Custom topic] "${topic}"\n`);
  } else {
    // Auto mode — read trending report
    if (!fs.existsSync(TRENDING_FILE)) {
      console.error('❌ No trending_report.json found. Run trend_fetch.js first!');
      process.exit(1);
    }

    const report = JSON.parse(fs.readFileSync(TRENDING_FILE, 'utf-8'));
    const selected = pickTopicFromTrending(report, opts.character);

    anime = selected;
    topic = selected.carousel_topics?.[0] || `Top characters in ${selected.title}`;

    // Build character list with PinGPT matching
    characters = selected.characters.map((name, i) => ({
      name,
      pingpt_name: selected.pingpt_characters.find(pc =>
        name.toLowerCase().includes(pc.toLowerCase()) ||
        pc.toLowerCase().includes(name.toLowerCase().split(' ').pop())
      ) || null,
      favorites: 10000 - (i * 1000),
    }));

    console.log(`[Auto-selected] ${selected.title}`);
    console.log(`[Topic] ${topic}`);
    console.log(`[Characters] ${characters.map(c => c.pingpt_name || c.name).join(', ')}\n`);
  }

  // Determine slide count
  const slideCount = pickSlideCount(topic, characters.length, opts.slides);
  console.log(`[Slides] ${slideCount} (cover + ${slideCount - 2} entries + closer)\n`);

  // Build the deck
  const slides = buildDeck(topic, anime, characters, slideCount);

  // Style breakdown
  const styleCount = {};
  slides.forEach(s => { styleCount[s.style] = (styleCount[s.style] || 0) + 1; });
  console.log('[Style Mix]');
  Object.entries(styleCount).forEach(([style, count]) => {
    console.log(`  ${style}: ${count} slides`);
  });

  // Generate caption
  const animeName = anime.title_english || anime.title || 'Anime';
  const caption = generateCaption(topic, animeName);

  // Build final deck
  const deck = {
    generated_at: new Date().toISOString(),
    topic,
    anime: animeName,
    slide_count: slideCount,
    style_approach: 'HYBRID — atmospheric NB2 AI art + manga-panel treatments mixed for visual rhythm',
    slides,
    tiktok_caption: caption.text,
    tiktok_hashtags: caption.hashtags,
    sound_suggestion: caption.sound_suggestion,
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(deck, null, 2));

  console.log(`\n═══════════════════════════════════════`);
  console.log(`✅ Carousel deck saved to: ${OUTPUT_FILE}`);
  console.log(`   ${slideCount} slides | Hybrid style mix`);
  console.log(`   Caption: "${caption.text.substring(0, 60)}..."`);
  console.log(`═══════════════════════════════════════`);

  // Print slide summary
  console.log('\n📋 SLIDE DECK:\n');
  for (const slide of slides) {
    const styleTag = `[${slide.style}]`;
    const rankTag = slide.rank ? `#${slide.rank}` : '';
    console.log(`  Slide ${slide.slide_num} ${slide.type.padEnd(7)} ${styleTag.padEnd(14)} ${rankTag.padEnd(4)} ${slide.character || ''}`);
    if (slide.commentary) console.log(`         "${slide.commentary}"`);
  }
}

main();
