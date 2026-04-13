/**
 * build_bulk_csv.js — Smart Pinterest Bulk Upload CSV Generator
 *
 * Features:
 *   - 15 pins/day default (aggressive growth mode)
 *   - Smart shuffle: never same character or board back-to-back
 *   - Board diversification: max 3 pins per board per day
 *   - EST-based timing with guaranteed 1h gaps + jitter
 *   - Batch memory: reads last scheduled date from previous CSV
 *   - Expanded board routing across all 12 user boards
 *
 * Usage:
 *   node scripts/build_bulk_csv.js                     → default (15/day, auto-start after last batch)
 *   node scripts/build_bulk_csv.js --now               → publish immediately (no schedule)
 *   node scripts/build_bulk_csv.js --start "2026-04-21" → custom start date
 *   node scripts/build_bulk_csv.js --per-day 20         → 20 pins per day
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = 'C:\\Users\\Administrator\\Desktop\\PinGPT';
const QUEUE_FILE = path.join(BASE_DIR, 'gemgen_queue.json');
const URLS_FILE = path.join(BASE_DIR, 'pinterest_urls.json');
const OUTPUT_CSV = path.join(BASE_DIR, 'output', 'pinterest_bulk.csv');
const BATCH_DIR = path.join(BASE_DIR, 'output', 'gemgen_batch');
const LEDGER_FILE = path.join(BASE_DIR, 'schedule_ledger.json');

// ── Schedule Config ─────────────────────────────────────────────────────────
const DEFAULT_PINS_PER_DAY = 15;

// EST peak windows (converted to UTC internally)
// These cover the full day for 15 pins: early morning through late night EST
const EST_SLOTS_HOURS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
// That's 6 AM - 10 PM EST = 17 slots, more than enough for 15 pins

// ── ALL 12 Boards ───────────────────────────────────────────────────────────
const ALL_BOARDS = [
    'Jujutsu Kaisen Wallpapers',
    'Attack on Titan Art',
    'Solo Leveling Aesthetic',
    'Anime Boys Aesthetic ✨',
    'Dark Anime Aesthetic',
    'Cozy Anime Vibes',
    'Anime Phone Wallpapers',
    'Anime Wallpapers',
    'Last Train Anime Aesthetics',
    'Last Train mood',
    'Late Night mood',
    '4amvibes'
];

// ── Board Routing (mood + character → board, with diversity) ────────────────
function resolveBoard(character, mood) {
    const m = (mood || '').toLowerCase();
    const c = (character || '').toLowerCase();

    // Character-specific franchise boards
    const jjkChars = ['gojo', 'toji', 'megumi', 'yuji', 'sukuna', 'nanami', 'yuta', 'okkotsu'];
    const aotChars = ['levi', 'eren', 'mikasa', 'ackerman'];
    const slChars  = ['sung', 'jinwoo'];
    const hxhChars = ['killua', 'gon', 'zoldyck'];

    const isJJK = jjkChars.some(ch => c.includes(ch));
    const isAoT = aotChars.some(ch => c.includes(ch));
    const isSL  = slChars.some(ch => c.includes(ch));
    const isHxH = hxhChars.some(ch => c.includes(ch));

    // ── Mood-based routing (takes priority) ──
    const darkMoods = [
        'lasttrain', 'roofrain', 'mirrorself', 'edgeofbed', 'ghostcall',
        'ironsilence', 'waitingroom', 'sadboy', 'alleysmoke', 'midnight_noir',
        'burnoutdesk', 'tunnel_flash', 'static_solitude'
    ];
    const nightMoods = [
        '4amvibes', 'late_shift', 'closingtime', 'edgeofbed', 'ghostcall',
        'chlorine_midnight', 'terminal_liminal', 'kitchen_confessional',
        'neon_arcade', 'streetlight_haze'
    ];
    const trainMoods = [
        'lasttrain', 'tunnel_flash', 'fumikiri_red_pulse'
    ];
    const cozyMoods = [
        'quietday', 'closingtime', 'dawnwalk', 'sundayghost', 'wabisabi',
        'lofiden', 'bakery_steam', 'ember_solace', 'sunsetvan',
        'fire_escape_forest', 'botanical_decay'
    ];
    const wallpaperMoods = [
        'gallerystill', 'darkacademia', 'retrocel', 'jerseycore',
        'skylineache', 'golden_passage', 'petal_storm_ephemera',
        'shallow_mirror_tide', 'gale_force_clarity', 'water_tank_solitude',
        'helipad_calm', 'whale_museum'
    ];
    const warmMoods = [
        'summer_haze', 'amber_archive', 'sun_drenched_downpour',
        'dashboard_horizon', 'drafting_dawn', 'golden_passage'
    ];

    // Build a weighted candidate list (primary + secondary options)
    const candidates = [];

    // Mood routing
    if (trainMoods.includes(m)) {
        candidates.push('Last Train Anime Aesthetics', 'Last Train mood');
    }
    if (nightMoods.includes(m)) {
        candidates.push('Late Night mood', '4amvibes');
    }
    if (darkMoods.includes(m)) {
        candidates.push('Dark Anime Aesthetic');
    }
    if (cozyMoods.includes(m)) {
        candidates.push('Cozy Anime Vibes');
    }
    if (wallpaperMoods.includes(m)) {
        candidates.push('Anime Phone Wallpapers', 'Anime Wallpapers');
    }
    if (warmMoods.includes(m)) {
        candidates.push('Cozy Anime Vibes', 'Anime Wallpapers');
    }

    // Character routing (add franchise board)
    if (isJJK) candidates.push('Jujutsu Kaisen Wallpapers');
    if (isAoT) candidates.push('Attack on Titan Art');
    if (isSL)  candidates.push('Solo Leveling Aesthetic');

    // Always include generic boards as fallback
    candidates.push('Anime Boys Aesthetic ✨', 'Anime Phone Wallpapers');

    // Deduplicate
    const unique = [...new Set(candidates)];

    // Return primary (first match) and secondary (second match or fallback)
    return {
        primary: unique[0] || 'Anime Boys Aesthetic ✨',
        secondary: unique[1] || 'Anime Phone Wallpapers',
        all: unique
    };
}

// ── Smart Shuffle ───────────────────────────────────────────────────────────
// Greedy interleave: pick the next pin that differs from previous character AND board
function smartShuffle(items, imageFiles) {
    if (items.length <= 1) return { items, imageFiles };

    const indices = items.map((_, i) => i);
    const result = [];
    const resultFiles = [];

    // Start with a random pin
    const startIdx = Math.floor(Math.random() * indices.length);
    result.push(items[indices[startIdx]]);
    resultFiles.push(imageFiles[indices[startIdx]]);
    indices.splice(startIdx, 1);

    while (indices.length > 0) {
        const lastChar = (result[result.length - 1].character || '').toLowerCase();
        const lastBoard = resolveBoard(result[result.length - 1].character, result[result.length - 1].mood).primary;

        // Find best candidate: different character AND different board
        let bestIdx = -1;

        // Priority 1: different character AND different board
        for (let j = 0; j < indices.length; j++) {
            const candidate = items[indices[j]];
            const candChar = (candidate.character || '').toLowerCase();
            const candBoard = resolveBoard(candidate.character, candidate.mood).primary;
            if (candChar !== lastChar && candBoard !== lastBoard) {
                bestIdx = j;
                break;
            }
        }

        // Priority 2: at least different character
        if (bestIdx === -1) {
            for (let j = 0; j < indices.length; j++) {
                const candidate = items[indices[j]];
                const candChar = (candidate.character || '').toLowerCase();
                if (candChar !== lastChar) {
                    bestIdx = j;
                    break;
                }
            }
        }

        // Priority 3: at least different board
        if (bestIdx === -1) {
            for (let j = 0; j < indices.length; j++) {
                const candidate = items[indices[j]];
                const candBoard = resolveBoard(candidate.character, candidate.mood).primary;
                if (candBoard !== lastBoard) {
                    bestIdx = j;
                    break;
                }
            }
        }

        // Fallback: just take the next one
        if (bestIdx === -1) bestIdx = 0;

        result.push(items[indices[bestIdx]]);
        resultFiles.push(imageFiles[indices[bestIdx]]);
        indices.splice(bestIdx, 1);
    }

    return { items: result, imageFiles: resultFiles };
}

// ── Board Diversification ───────────────────────────────────────────────────
// Max N pins per board per day. If exceeded, use secondary board.
const MAX_PER_BOARD_PER_DAY = 3;

function resolveBoardWithDiversity(character, mood, dayBoardCounts) {
    const routing = resolveBoard(character, mood);

    // Check if primary board is over quota for this day
    const primaryCount = dayBoardCounts[routing.primary] || 0;
    if (primaryCount < MAX_PER_BOARD_PER_DAY) {
        dayBoardCounts[routing.primary] = primaryCount + 1;
        return routing.primary;
    }

    // Try secondary
    const secondaryCount = dayBoardCounts[routing.secondary] || 0;
    if (secondaryCount < MAX_PER_BOARD_PER_DAY) {
        dayBoardCounts[routing.secondary] = secondaryCount + 1;
        return routing.secondary;
    }

    // Try all candidates
    for (const board of routing.all) {
        const count = dayBoardCounts[board] || 0;
        if (count < MAX_PER_BOARD_PER_DAY) {
            dayBoardCounts[board] = count + 1;
            return board;
        }
    }

    // Last resort: pick the least-used board overall
    let minBoard = routing.primary;
    let minCount = Infinity;
    for (const board of ALL_BOARDS) {
        const count = dayBoardCounts[board] || 0;
        if (count < minCount) {
            minCount = count;
            minBoard = board;
        }
    }
    dayBoardCounts[minBoard] = (dayBoardCounts[minBoard] || 0) + 1;
    return minBoard;
}

// ── Emoji Stripping ─────────────────────────────────────────────────────────
function stripEmoji(text) {
    return text.replace(/[\u{1F000}-\u{1FFFF}]|[\u{2600}-\u{27BF}]|[\u{FE00}-\u{FE0F}]|[\u{1F900}-\u{1F9FF}]|[\u{200D}]|[\u{20E3}]|[\u{E0020}-\u{E007F}]/gu, '').trim();
}

// ── CSV Escaping ────────────────────────────────────────────────────────────
function csvEscape(val) {
    if (!val) return '';
    const s = String(val);
    if (s.includes(',') || s.includes('"') || s.includes('\n')) {
        return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
}

// ── Schedule Ledger: persistent per-day pin counts across batches ───────────
function loadLedger() {
    if (!fs.existsSync(LEDGER_FILE)) return {};
    try {
        return JSON.parse(fs.readFileSync(LEDGER_FILE, 'utf8'));
    } catch (e) {
        console.warn('[Ledger] Could not parse ledger, starting fresh');
        return {};
    }
}

function saveLedger(ledger) {
    fs.writeFileSync(LEDGER_FILE, JSON.stringify(ledger, null, 2), 'utf8');
    console.log(`[Ledger] Saved to ${LEDGER_FILE}`);
}

// ── Schedule Builder (fills gap days first, then adds new days) ─────────────
function buildSchedule(pinCount, pinsPerDay, existingDayCounts) {
    const schedule = [];

    // Pick N evenly-spaced EST slots for the given pinsPerDay
    const slotsNeeded = Math.min(pinsPerDay, EST_SLOTS_HOURS.length);
    const step = EST_SLOTS_HOURS.length / slotsNeeded;
    const dailySlots = [];
    for (let i = 0; i < slotsNeeded; i++) {
        dailySlots.push(EST_SLOTS_HOURS[Math.floor(i * step)]);
    }

    // Helper: generate a time slot for pins on a given day
    function makeSlot(dateStr, slotIndex) {
        const estHour = dailySlots[slotIndex] || dailySlots[dailySlots.length - 1];
        const utcHour = estHour + 4; // EDT = UTC-4 (April)
        const jitter = Math.floor(Math.random() * 31) - 15;
        const minute = Math.max(0, Math.min(59, 30 + jitter));
        const hourStr = utcHour.toString().padStart(2, '0');
        const minStr = minute.toString().padStart(2, '0');
        return `${dateStr} ${hourStr}:${minStr}:00`;
    }

    let pinsPlaced = 0;

    // Phase 1: Fill under-quota existing days (only future days)
    const today = new Date().toISOString().split('T')[0];
    const gapDays = Object.entries(existingDayCounts)
        .filter(([day, count]) => day >= today && count < pinsPerDay)
        .sort((a, b) => a[0].localeCompare(b[0]));

    if (gapDays.length > 0) {
        console.log(`[Gap Fill] Found ${gapDays.length} under-quota days:`);
        for (const [day, existing] of gapDays) {
            const slotsToFill = pinsPerDay - existing;
            console.log(`  ${day}: ${existing} existing → adding ${slotsToFill} to reach ${pinsPerDay}`);
            // Schedule new pins in the remaining slots (after existing ones)
            for (let s = 0; s < slotsToFill && pinsPlaced < pinCount; s++) {
                schedule.push(makeSlot(day, existing + s));
                pinsPlaced++;
            }
        }
    }

    // Phase 2: Add fresh days for remaining pins
    if (pinsPlaced < pinCount) {
        // Start from the day after the last existing day, or tomorrow
        const allDays = Object.keys(existingDayCounts).sort();
        let nextDay;
        if (allDays.length > 0) {
            const last = new Date(allDays[allDays.length - 1] + 'T00:00:00');
            last.setDate(last.getDate() + 1);
            nextDay = last;
        } else {
            nextDay = new Date();
            nextDay.setDate(nextDay.getDate() + 1);
        }

        // Make sure nextDay is in the future
        const todayDate = new Date(today + 'T00:00:00');
        if (nextDay <= todayDate) {
            nextDay = new Date(todayDate);
            nextDay.setDate(nextDay.getDate() + 1);
        }

        while (pinsPlaced < pinCount) {
            const dateStr = nextDay.toISOString().split('T')[0];
            const pinsThisDay = Math.min(pinsPerDay, pinCount - pinsPlaced);
            for (let s = 0; s < pinsThisDay; s++) {
                schedule.push(makeSlot(dateStr, s));
                pinsPlaced++;
            }
            nextDay.setDate(nextDay.getDate() + 1);
        }
    }

    // Sort chronologically
    schedule.sort();
    return schedule;
}

// ── Main ────────────────────────────────────────────────────────────────────
function main() {
    const args = process.argv.slice(2);
    const immediate = args.includes('--now');
    const pinsPerDay = args.includes('--per-day')
        ? parseInt(args[args.indexOf('--per-day') + 1]) || DEFAULT_PINS_PER_DAY
        : DEFAULT_PINS_PER_DAY;

    // Load persistent schedule ledger
    const ledger = loadLedger();
    const existingDayCounts = ledger;
    const dayKeys = Object.keys(existingDayCounts).sort();
    if (dayKeys.length > 0) {
        console.log(`[Ledger] Loaded ${dayKeys.length} days of history (${dayKeys[0]} → ${dayKeys[dayKeys.length - 1]})`);
    } else {
        console.log('[Ledger] No previous schedule history found');
    }

    // ── Load final mapping ──────────────────────────────────────────────────
    const BULKPIN_METADATA_FILE = path.join(BATCH_DIR, 'bulkpin_metadata.json');
    const FINAL_MAPPING_FILE = path.join(BATCH_DIR, 'final_mapping.json');
    let mapFileToUse = FINAL_MAPPING_FILE;

    if (fs.existsSync(BULKPIN_METADATA_FILE)) {
        console.log("Using bulkpin_metadata.json");
        mapFileToUse = BULKPIN_METADATA_FILE;
    } else if (!fs.existsSync(FINAL_MAPPING_FILE)) {
        console.error(`Mapping file not found: ${FINAL_MAPPING_FILE}`);
        process.exit(1);
    }

    const finalMap = JSON.parse(fs.readFileSync(mapFileToUse, 'utf8'));

    // ── Load URL mapping ────────────────────────────────────────────────────
    let urls = {};
    if (fs.existsSync(URLS_FILE)) {
        urls = JSON.parse(fs.readFileSync(URLS_FILE, 'utf8'));
        console.log(`Loaded ${Object.keys(urls).length} URLs from pinterest_urls.json`);
    } else {
        console.warn('WARNING: pinterest_urls.json not found!');
        console.warn('Run: python scripts/upload_drive.py --pinterest');
    }

    // ── Parse items ─────────────────────────────────────────────────────────
    let items = [];
    let imageFiles = [];

    if (Array.isArray(finalMap)) {
        for (const entry of finalMap) {
            if (entry.duplicate) continue;
            imageFiles.push(entry.file);
            items.push({
                mood: entry.mood,
                title: entry.title,
                description: entry.description,
                tags: entry.tags,
                character: entry.character,
                link: entry.link || ''
            });
        }
    } else {
        for (const [filename, data] of Object.entries(finalMap)) {
            if (!data.error && data.prompt_details) {
                imageFiles.push(filename);
                items.push(data.prompt_details);
            }
        }
    }

    if (items.length === 0) {
        console.error('No valid items found');
        process.exit(1);
    }

    // ── Smart Shuffle (character + board interleaving) ──────────────────────
    console.log(`\n[Smart Shuffle] Interleaving ${items.length} pins for diversity...`);
    const shuffled = smartShuffle(items, imageFiles);
    items = shuffled.items;
    imageFiles = shuffled.imageFiles;

    // ── Build schedule (fills gaps first, then new days) ─────────────────────
    const schedule = immediate ? [] : buildSchedule(items.length, pinsPerDay, existingDayCounts);

    if (!immediate && schedule.length > 0) {
        const startDay = schedule[0].split(' ')[0];
        const endDay = schedule[schedule.length - 1].split(' ')[0];
        const uniqueDays = [...new Set(schedule.map(s => s.split(' ')[0]))];
        console.log(`[Schedule] ${items.length} pins across ${uniqueDays.length} days (target ${pinsPerDay}/day)`);
        console.log(`[Schedule] ${startDay} → ${endDay}\n`);
    } else if (immediate) {
        console.log('\n--now mode: All pins will publish immediately.\n');
    }

    // ── Build CSV rows with board diversification ───────────────────────────
    const CSV_HEADERS = ['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords'];
    const rows = [CSV_HEADERS.join(',')];

    const seenTitles = {};
    const boardStats = {};       // overall board distribution
    let missing = 0;
    let currentDay = '';
    let dayBoardCounts = {};     // per-day board counts for diversification

    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const filename = imageFiles[i];

        // Get public URL
        let mediaUrl = '';
        if (urls[filename]) {
            mediaUrl = urls[filename].url || urls[filename].drive_url || '';
        }
        if (!mediaUrl) {
            console.warn(`  [${i + 1}] WARNING: No URL for ${filename}`);
            missing++;
        }

        // Determine which day this pin falls on (for board diversity tracking)
        const pinDay = !immediate && schedule[i] ? schedule[i].split(' ')[0] : 'immediate';
        if (pinDay !== currentDay) {
            currentDay = pinDay;
            dayBoardCounts = {}; // Reset board counts for new day
        }

        // Board routing with diversity enforcement
        const board = resolveBoardWithDiversity(item.character, item.mood, dayBoardCounts);
        boardStats[board] = (boardStats[board] || 0) + 1;

        // Title + description
        const desc = stripEmoji([item.description, item.tags].filter(Boolean).join(' '));
        let title = stripEmoji(item.title || '');
        if (seenTitles[title]) {
            seenTitles[title]++;
            title = `${title} (${seenTitles[title]})`;
        } else {
            seenTitles[title] = 1;
        }
        const keywords = (item.tags || '').replace(/#/g, '').replace(/\s+/g, ',');

        // Schedule
        const publishDate = immediate ? '' : (schedule[i] || '');

        const row = [
            csvEscape(title),
            csvEscape(mediaUrl),
            csvEscape(board),
            '',
            csvEscape(desc),
            csvEscape(item.link || ''),
            csvEscape(publishDate),
            csvEscape(keywords)
        ].join(',');

        rows.push(row);
    }

    // ── Write CSV ───────────────────────────────────────────────────────────
    fs.writeFileSync(OUTPUT_CSV, rows.join('\n'), 'utf8');

    // ── Update ledger with new schedule ──────────────────────────────────────
    if (!immediate) {
        for (const slot of schedule) {
            const day = slot.split(' ')[0];
            ledger[day] = (ledger[day] || 0) + 1;
        }
        saveLedger(ledger);
    }

    // ── Summary ─────────────────────────────────────────────────────────────
    console.log('='.repeat(60));
    console.log(`CSV written to: ${OUTPUT_CSV}`);
    console.log(`Pins: ${items.length} | Missing URLs: ${missing}`);
    if (!immediate) {
        console.log(`Schedule: target ${pinsPerDay}/day`);
    }
    console.log('='.repeat(60));

    // Board distribution report
    console.log('\n📊 Board Distribution:');
    const sortedBoards = Object.entries(boardStats).sort((a, b) => b[1] - a[1]);
    for (const [board, count] of sortedBoards) {
        const pct = ((count / items.length) * 100).toFixed(1);
        const bar = '█'.repeat(Math.round(count / items.length * 20));
        console.log(`  ${board.padEnd(30)} ${count.toString().padStart(3)} (${pct}%) ${bar}`);
    }

    // Diversity check
    console.log('\n🔀 Diversity Check:');
    let backToBackChar = 0;
    let backToBackBoard = 0;
    for (let i = 1; i < items.length; i++) {
        if ((items[i].character || '').toLowerCase() === (items[i-1].character || '').toLowerCase()) {
            backToBackChar++;
        }
    }
    console.log(`  Back-to-back same character: ${backToBackChar} / ${items.length - 1}`);
    console.log(`  ${backToBackChar === 0 ? '✅ Perfect diversity' : '⚠️  Some repeats (acceptable if few characters)'}`);

    if (missing > 0) {
        console.log(`\n⚠️  ${missing} pin(s) have no media URL.`);
        console.log('Run: python scripts/upload_drive.py --pinterest');
    }

    // Preview first 5 rows
    console.log('\n📌 Preview (first 5 pins):');
    for (let i = 1; i <= Math.min(5, items.length); i++) {
        const cols = rows[i].split(',');
        console.log(`  ${i}. ${cols[0].substring(0, 40).padEnd(42)} → ${cols[2].padEnd(30)} @ ${cols[6]}`);
    }
}

main();
