#!/usr/bin/env node
/**
 * TrendTok — Trend Fetch Script
 * 
 * Queries multiple sources for trending anime data, cross-references with
 * PinGPT's character roster, and outputs a ranked trending_report.json.
 * 
 * Sources:
 *   1. Jikan API (MyAnimeList) — primary backbone, free, no auth
 *   2. Google Trends / Pinterest Trends / AniTrendz — stubs for browser scraping
 * 
 * Usage: node scripts/trend_fetch.js [--season spring|summer|fall|winter] [--year 2026]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ─── Config ────────────────────────────────────────────────────
const PINGPT_ROOT = path.resolve(__dirname, '..');
const CHARACTERS_FILE = path.join(PINGPT_ROOT, 'skill_characters.md');
const OUTPUT_FILE = path.join(PINGPT_ROOT, 'trending_report.json');
const TOPIC_HISTORY_FILE = path.join(PINGPT_ROOT, 'topic_history.json');

const JIKAN_BASE = 'https://api.jikan.moe/v4';
const JIKAN_DELAY_MS = 1000; // rate limit: 3 req/s, we stay safe

// Topic templates for carousel generation
// ─── Topic Templates (8 categories for diversity) ──────────────
const TOPIC_TEMPLATES = {
  power_scaling: [
    'Top {N} strongest characters in {anime}',
    '{N} characters who could solo {character}',
    'Top {N} characters who didn\'t fear {character}',
    'Ranking every {group} member by raw power in {anime}',
    'Top {N} most broken abilities in {anime}',
    '{N} characters who would beat {character} in a rematch',
  ],
  emotional: [
    '{N} characters with the saddest backstory in {anime}',
    'Top {N} moments that made you cry in {anime}',
    '{N} characters who deserved better in {anime}',
    'Most heartbreaking deaths in {anime}',
    '{N} characters who suffered the most in {anime}',
    'Top {N} sacrifices that actually meant something in {anime}',
  ],
  hypothetical: [
    'What if {character} never died in {anime}',
    '{N} characters who would switch the outcome of {anime}',
    'What if {character} turned villain in {anime}',
    '{N} "what if" scenarios that would break {anime}',
    'If {character} trained for 10 more years in {anime}',
  ],
  character_development: [
    '{N} characters with the best glow-up in {anime}',
    'Top {N} character arcs in {anime}',
    '{N} characters who carried their entire arc in {anime}',
    'Most wasted potential characters in {anime}',
    '{N} characters who peaked too early in {anime}',
    'Top {N} mentor figures in {anime}',
  ],
  legacy: [
    '{N} moments that broke the internet in {anime}',
    'Top {N} most iconic scenes in {anime}',
    '{N} characters everyone remembers from {anime}',
    'Top {N} entrances that gave you chills in {anime}',
    'Most quotable characters in {anime}',
  ],
  design_aesthetic: [
    'Top {N} best character designs in {anime}',
    '{N} coldest fits in {anime}',
    'Most intimidating character designs in {anime}',
    'Top {N} transformation sequences in {anime}',
    '{N} characters with the hardest drip in {anime}',
  ],
  comedy: [
    '{N} funniest moments in {anime}',
    'Most unhinged characters in {anime}',
    '{N} characters who had no business being that funny in {anime}',
    'Top {N} menace moments in {anime}',
    '{N} characters who chose violence for no reason in {anime}',
  ],
  villain: [
    'Top {N} villains who were actually right in {anime}',
    '{N} most terrifying villains in {anime}',
    'Ranking every villain in {anime} by threat level',
    '{N} villains with better drip than the hero in {anime}',
    'Most underrated antagonists in {anime}',
    'Top {N} villain monologues in {anime}',
  ],
};

// Mood workflows for auto-recommendation
const MOODS = [
  '/roofrain', '/lasttrain', '/4amvibes', '/ironsilence', '/mirrorself',
  '/alleysmoke', '/closingtime', '/dawnwalk', '/ghostcall', '/waitingroom',
  '/greenbreath', '/quietday', '/edgeofbed', '/sundayghost', '/backstreet',
];

// ─── HTTP helper (no deps) ────────────────────────────────────
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'TrendTok/1.0' } }, (res) => {
      if (res.statusCode === 429) {
        return reject(new Error(`Rate limited (429) on ${url}`));
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse failed for ${url}: ${e.message}`)); }
      });
    }).on('error', reject);
  });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ─── Parse PinGPT character roster ────────────────────────────
function parseCharacterRoster() {
  const content = fs.readFileSync(CHARACTERS_FILE, 'utf-8');
  const characters = [];

  // Match table rows: | Name | Series | ...
  const tableRegex = /\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|/g;
  let match;
  while ((match = tableRegex.exec(content)) !== null) {
    const name = match[1].trim();
    const series = match[2].trim();
    // Skip header rows
    if (name === 'Character' || name.startsWith('---')) continue;
    characters.push({
      name,
      series,
      // Normalize for matching
      nameNorm: name.toLowerCase().replace(/[^a-z0-9]/g, ''),
      seriesNorm: series.toLowerCase().replace(/[^a-z0-9]/g, ''),
    });
  }
  return characters;
}

// ─── Jikan API: Current Season ────────────────────────────────
async function fetchJikanSeason() {
  console.log('[Jikan] Fetching current season top airing...');
  const url = `${JIKAN_BASE}/seasons/now?order_by=members&sort=desc&limit=25`;
  const data = await fetchJSON(url);
  return (data.data || []).map(anime => ({
    mal_id: anime.mal_id,
    title: anime.title,
    title_english: anime.title_english,
    score: anime.score || 0,
    members: anime.members || 0,
    episodes: anime.episodes,
    airing: anime.airing,
    genres: (anime.genres || []).map(g => g.name),
    url: anime.url,
  }));
}

// ─── Jikan API: Top Characters for an anime ───────────────────
async function fetchAnimeCharacters(malId) {
  await sleep(JIKAN_DELAY_MS);
  try {
    const url = `${JIKAN_BASE}/anime/${malId}/characters`;
    const data = await fetchJSON(url);
    return (data.data || [])
      .filter(c => c.role === 'Main' || c.favorites > 1000)
      .slice(0, 10)
      .map(c => ({
        name: c.character?.name || 'Unknown',
        favorites: c.favorites || 0,
        role: c.role,
      }));
  } catch (e) {
    console.warn(`[Jikan] Failed to fetch characters for MAL ID ${malId}: ${e.message}`);
    return [];
  }
}

// ─── Cross-reference with PinGPT roster ───────────────────────
function crossReference(animeCharacters, roster) {
  const matched = [];
  const unmatched = [];

  for (const ac of animeCharacters) {
    // Normalize: "Fushiguro, Toji" → "tojifushiguro"
    const nameNorm = ac.name.toLowerCase().replace(/[^a-z0-9]/g, '');
    // Also try reversed (Jikan uses "Last, First")
    const parts = ac.name.split(',').map(s => s.trim());
    const reversedNorm = parts.length > 1
      ? (parts[1] + parts[0]).toLowerCase().replace(/[^a-z0-9]/g, '')
      : nameNorm;

    // Also extract just the first name for matching (e.g., "Fushiguro, Toji" → "toji")
    const firstName = parts.length > 1
      ? parts[1].toLowerCase().replace(/[^a-z0-9]/g, '')
      : parts[0].toLowerCase().replace(/[^a-z0-9]/g, '');
    const lastName = parts[0].toLowerCase().replace(/[^a-z0-9]/g, '');

    const found = roster.find(r => {
      // Exact full-name match (strongest signal)
      if (nameNorm === r.nameNorm || reversedNorm === r.nameNorm) return true;

      // For short names (<6 chars), require exact match only
      // to avoid cross-series false positives (e.g., "Nanami" from Dr. Stone ≠ "Nanami Kento" from JJK)
      if (nameNorm.length < 6 && r.nameNorm.length < 6) {
        return nameNorm === r.nameNorm;
      }
      if (nameNorm.length < 6 || r.nameNorm.length < 6) return false;

      // Substring match for longer names (e.g., "tojifushiguro" contains "toji")
      // But require the roster name to be a significant portion (>= 4 chars matched)
      if (reversedNorm.includes(r.nameNorm) || r.nameNorm.includes(reversedNorm)) return true;
      if (nameNorm.includes(r.nameNorm) || r.nameNorm.includes(nameNorm)) return true;

      // First-name or last-name match against roster (for partial roster entries like "Toji" or "Gojo")
      if (firstName.length >= 4 && r.nameNorm.includes(firstName)) return true;
      if (lastName.length >= 4 && r.nameNorm.includes(lastName)) return true;

      return false;
    });

    if (found) {
      matched.push({ ...ac, pingpt_name: found.name, pingpt_series: found.series });
    } else {
      unmatched.push(ac);
    }
  }

  return { matched, unmatched };
}

// ─── Trend Signal Scoring ─────────────────────────────────────
function scoreTrend(anime) {
  let score = 0;

  // Popularity weight (members on MAL)
  if (anime.members > 2000000) score += 40;
  else if (anime.members > 1000000) score += 30;
  else if (anime.members > 500000) score += 20;
  else if (anime.members > 100000) score += 10;

  // Quality weight (MAL score)
  if (anime.score >= 8.5) score += 25;
  else if (anime.score >= 8.0) score += 20;
  else if (anime.score >= 7.5) score += 15;
  else if (anime.score >= 7.0) score += 10;

  // Currently airing bonus
  if (anime.airing) score += 15;

  return score;
}

function getTrendSignal(score) {
  if (score >= 60) return 'PEAK';
  if (score >= 40) return 'RISING';
  if (score >= 20) return 'WARM';
  return 'FADING';
}

// ─── Topic History ────────────────────────────────────────────
function loadTopicHistory() {
  try {
    if (fs.existsSync(TOPIC_HISTORY_FILE)) {
      const data = JSON.parse(fs.readFileSync(TOPIC_HISTORY_FILE, 'utf-8'));
      return data.topics || [];
    }
  } catch (e) {
    console.warn(`[History] Failed to load topic_history.json: ${e.message}`);
  }
  return [];
}

function recordTopic(topic, series, model = 'unknown') {
  const history = loadTopicHistory();
  history.push({
    topic,
    series: series || 'unknown',
    date: new Date().toISOString().split('T')[0],
    model,
  });
  const data = { topics: history };
  fs.writeFileSync(TOPIC_HISTORY_FILE, JSON.stringify(data, null, 2));
  console.log(`[History] Recorded topic: "${topic}" (${history.length} total in history)`);
}

function isTopicUsed(topic, history) {
  const normalize = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  const normTopic = normalize(topic);
  return history.some(h => {
    const normH = normalize(h.topic);
    // Exact match or >70% overlap (fuzzy dedup)
    if (normH === normTopic) return true;
    // Check if one contains the other (catches minor rephrases)
    if (normH.includes(normTopic) || normTopic.includes(normH)) return true;
    return false;
  });
}

// ─── Generate carousel topic suggestions (diversity-aware) ────
function generateTopicSuggestions(anime, matchedChars) {
  const title = anime.title_english || anime.title;
  const history = loadTopicHistory();
  const allTopics = [];

  // Pick up to 2 unused templates from EACH category for max diversity (8 cats × 2 = 16 pool → pick 10)
  const categories = Object.keys(TOPIC_TEMPLATES);
  for (const cat of categories) {
    const templates = TOPIC_TEMPLATES[cat];
    // Shuffle templates within category
    const shuffled = [...templates].sort(() => Math.random() - 0.5);
    let pickedFromCat = 0;

    for (const tmpl of shuffled) {
      if (pickedFromCat >= 2) break; // Max 2 per category

      // Fill template variables
      const N = matchedChars.length >= 5 ? matchedChars.length : Math.min(10, Math.max(5, matchedChars.length + 2));
      const strongChar = matchedChars.find(c =>
        c.pingpt_name.toLowerCase().includes('gojo') ||
        c.pingpt_name.toLowerCase().includes('sukuna') ||
        c.pingpt_name.toLowerCase().includes('guts') ||
        c.pingpt_name.toLowerCase().includes('eren')
      );

      let topic = tmpl
        .replace('{N}', N)
        .replace('{anime}', title)
        .replace('{character}', strongChar ? strongChar.pingpt_name : 'the strongest')
        .replace('{group}', 'main');

      // Skip if already used
      if (!isTopicUsed(topic, history)) {
        allTopics.push({ topic, category: cat });
        pickedFromCat++;
      }
    }
  }

  // Shuffle across categories so suggestions aren't always in the same order
  allTopics.sort(() => Math.random() - 0.5);

  return allTopics.slice(0, 10).map(t => `[${t.category}] ${t.topic}`);
}

// ─── Recommend moods for matched characters ───────────────────
function recommendMoods(matchedChars) {
  // Shuffle and pick 3-5 moods
  const shuffled = [...MOODS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(5, Math.max(3, matchedChars.length)));
}

// ─── Browser scrape stubs (for future implementation) ─────────
async function fetchGoogleTrends() {
  // Stub: returns empty. Implement via browser_subagent scraping.
  console.log('[Google Trends] Stub — browser scraping not yet implemented');
  return { source: 'google_trends', status: 'stub', data: [] };
}

async function fetchPinterestTrends() {
  console.log('[Pinterest Trends] Stub — browser scraping not yet implemented');
  return { source: 'pinterest_trends', status: 'stub', data: [] };
}

async function fetchAniTrendz() {
  console.log('[AniTrendz] Stub — browser scraping not yet implemented');
  return { source: 'anitrendz', status: 'stub', data: [] };
}

// ─── Main ─────────────────────────────────────────────────────
async function main() {
  console.log('═══════════════════════════════════════');
  console.log('  TrendTok — Trend Fetch Engine v1.0');
  console.log('═══════════════════════════════════════\n');

  // 1. Parse PinGPT character roster
  console.log('[Roster] Parsing skill_characters.md...');
  const roster = parseCharacterRoster();
  console.log(`[Roster] Found ${roster.length} characters in PinGPT roster\n`);

  // 2. Fetch data from all sources in parallel
  const [seasonAnime, googleTrends, pinterestTrends, aniTrendz] = await Promise.all([
    fetchJikanSeason(),
    fetchGoogleTrends(),
    fetchPinterestTrends(),
    fetchAniTrendz(),
  ]);

  console.log(`[Jikan] Got ${seasonAnime.length} airing anime\n`);

  // 3. For top 10 anime, fetch their characters and cross-reference
  const trending = [];

  for (let i = 0; i < Math.min(10, seasonAnime.length); i++) {
    const anime = seasonAnime[i];
    console.log(`[${i + 1}/${Math.min(10, seasonAnime.length)}] Processing: ${anime.title}...`);

    const chars = await fetchAnimeCharacters(anime.mal_id);
    const { matched, unmatched } = crossReference(chars, roster);

    const trendScore = scoreTrend(anime);
    const trendSignal = getTrendSignal(trendScore);

    const entry = {
      rank: i + 1,
      title: anime.title_english || anime.title,
      title_jp: anime.title,
      mal_id: anime.mal_id,
      mal_score: anime.score,
      members: anime.members,
      airing: anime.airing,
      genres: anime.genres,
      trend_score: trendScore,
      trend_signal: trendSignal,
      characters: chars.map(c => c.name.split(',').reverse().map(s => s.trim()).join(' ')),
      known_in_pingpt: matched.length > 0,
      pingpt_characters: matched.map(m => m.pingpt_name),
      unknown_characters: unmatched.map(u => u.name.split(',').reverse().map(s => s.trim()).join(' ')),
      recommended_moods: recommendMoods(matched),
      carousel_topics: generateTopicSuggestions(anime, matched),
      auto_prompt_ready: matched.length > 0,
      supplementary_signals: {
        google_trends: googleTrends.status,
        pinterest_trends: pinterestTrends.status,
        anitrendz: aniTrendz.status,
      },
    };

    trending.push(entry);
  }

  // 4. FALLBACK: If no airing anime matched PinGPT roster, query our known series
  if (trending.filter(t => t.known_in_pingpt).length === 0) {
    console.log('\n[Fallback] No airing anime match PinGPT roster. Querying known series...');

    // Extract unique series from PinGPT roster
    const knownSeries = [...new Set(roster.map(r => r.series))];
    const KNOWN_MAL_IDS = {
      'Jujutsu Kaisen': 40748,
      'Attack on Titan': 16498,
      'Baki': 34443,
      'Chainsaw Man': 44511,
      'Berserk': 33,
      'Solo Leveling': 52299,
      'SPY x FAMILY': 50265,
      'Hunter x Hunter': 11061,
      'My Hero Academia': 31964,
      'Blue Lock': 49596,
      'Oshi no Ko': 52034,
    };

    for (const series of knownSeries) {
      const malId = KNOWN_MAL_IDS[series];
      if (!malId) continue;

      console.log(`[Fallback] Querying: ${series} (MAL ID: ${malId})...`);
      await sleep(JIKAN_DELAY_MS);

      try {
        const url = `${JIKAN_BASE}/anime/${malId}`;
        const animeData = await fetchJSON(url);
        const anime = animeData.data;
        if (!anime) continue;

        const chars = await fetchAnimeCharacters(malId);
        const { matched } = crossReference(chars, roster);

        if (matched.length === 0) continue;

        const animeEntry = {
          mal_id: anime.mal_id,
          title: anime.title,
          title_english: anime.title_english,
          score: anime.score || 0,
          members: anime.members || 0,
          airing: anime.airing || false,
          genres: (anime.genres || []).map(g => g.name),
        };

        const trendScore = scoreTrend(animeEntry) + 5; // Small bonus for being in our roster
        trending.push({
          rank: 0,
          title: anime.title_english || anime.title,
          title_jp: anime.title,
          mal_id: anime.mal_id,
          mal_score: anime.score || 0,
          members: anime.members || 0,
          airing: anime.airing || false,
          genres: animeEntry.genres,
          trend_score: trendScore,
          trend_signal: getTrendSignal(trendScore),
          source: 'PINGPT_ROSTER_FALLBACK',
          characters: chars.map(c => c.name.split(',').reverse().map(s => s.trim()).join(' ')),
          known_in_pingpt: true,
          pingpt_characters: matched.map(m => m.pingpt_name),
          unknown_characters: [],
          recommended_moods: recommendMoods(matched),
          carousel_topics: generateTopicSuggestions(animeEntry, matched),
          auto_prompt_ready: true,
          supplementary_signals: { google_trends: 'stub', pinterest_trends: 'stub', anitrendz: 'stub' },
        });
      } catch (e) {
        console.warn(`[Fallback] Failed for ${series}: ${e.message}`);
      }
    }
  }

  // 5. Sort by trend score (highest first)
  trending.sort((a, b) => b.trend_score - a.trend_score);
  trending.forEach((t, i) => t.rank = i + 1);

  // 6. Build final report
  const now = new Date();
  const seasons = ['winter', 'spring', 'summer', 'fall'];
  const currentSeason = seasons[Math.floor(now.getMonth() / 3)];

  const report = {
    generated_at: now.toISOString(),
    season: `${currentSeason.charAt(0).toUpperCase() + currentSeason.slice(1)} ${now.getFullYear()}`,
    sources: {
      jikan: { status: 'active', entries: seasonAnime.length },
      google_trends: googleTrends.status,
      pinterest_trends: pinterestTrends.status,
      anitrendz: aniTrendz.status,
    },
    total_trending: trending.length,
    pingpt_ready: trending.filter(t => t.known_in_pingpt).length,
    trending,
  };

  // 7. Write output
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(report, null, 2));
  console.log(`\n═══════════════════════════════════════`);
  console.log(`✅ Trending report saved to: ${OUTPUT_FILE}`);
  console.log(`   ${report.total_trending} anime ranked`);
  console.log(`   ${report.pingpt_ready} have PinGPT characters ready`);
  console.log(`═══════════════════════════════════════`);

  // 8. Print summary table
  console.log('\n📊 TRENDING NOW:\n');
  console.log('Rank | Signal  | Score | Title                          | PinGPT Chars');
  console.log('─────┼─────────┼───────┼────────────────────────────────┼─────────────');
  for (const t of trending) {
    const signal = t.trend_signal.padEnd(7);
    const score = String(t.trend_score).padStart(5);
    const title = t.title.substring(0, 30).padEnd(30);
    const chars = t.pingpt_characters.length > 0
      ? t.pingpt_characters.join(', ')
      : '(none)';
    console.log(`  ${t.rank}  | ${signal} | ${score} | ${title} | ${chars}`);
  }

  return report;
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});
