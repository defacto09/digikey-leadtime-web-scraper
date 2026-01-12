# DigiKey Lead Time Scraper

Multi-method tool to extract DigiKey product availability and lead-time schedules.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Method

#### 🏆 Recommended: Digi-Key Official API (Mode 3)

```bash
# Setup: Register app at developer.digikey.com
# Set env vars: DIGIKEY_CLIENT_ID, DIGIKEY_CLIENT_SECRET

python main.py
# → Press Enter for mode 3 (default)
# → Enter part number (e.g., AD5412AREZ)
```

**Benefits:**
- ✓ No Cloudflare blocks
- ✓ Fast & reliable
- ✓ Official API, production-ready
- ✓ Free tier: ~100 requests/minute

**Setup:** See [DIGIKEY_API_SETUP.md](DIGIKEY_API_SETUP.md)

---

#### 🌐 Alternative: Web Scraping via Oxylabs (Mode 1)

```bash
# Setup: Get Oxylabs proxy credentials
# Set env vars: OXYLABS_USER, OXYLABS_PASS

python main.py
# → Select mode 1
# → Enter part number
```

**Benefits:**
- ✓ Detailed lead-time table (qty + date)
- ✓ JavaScript rendering via Oxylabs
- ⚠ Slower (browser overhead)
- ⚠ Costs money (Oxylabs is paid service)

---

#### 📄 Offline: Parse Saved HTML (Mode 2)

```bash
# First, manually save DigiKey product page as HTML
# Then:

python main.py
# → Select mode 2
# → Enter file path (e.g., AD5412AREZ.html)
```

**Benefits:**
- ✓ No internet needed
- ✓ Instant parsing
- ✓ Good for testing

---

## 📊 Comparison

| Feature | API (Mode 3) | Web Scraping (Mode 1) | Saved HTML (Mode 2) |
|---------|-----|---------|---------|
| **Speed** | ⚡ Fast | 🐢 Slow | ⚡ Instant |
| **Reliability** | ✓ High | ⚠ Medium | ✓ High |
| **Cloudflare** | ✓ No blocks | ✓ Bypassed | N/A |
| **Lead Time** | Aggregated | Detailed table | Detailed table |
| **Cost** | Free | Paid (Oxylabs) | Free |
| **Setup** | Medium | Medium | Easy |
| **Maintenance** | Low | High | N/A |

---

## 🔧 Installation

### Basic (API mode only):
```bash
pip install beautifulsoup4 digikey-api
```

### Full (all modes):
```bash
pip install -r requirements.txt
```

### Optional: Install Playwright for web scraping
```bash
python -m playwright install chromium
```

---

## 📝 Usage Examples

### Example 1: API lookup (recommended)
```bash
$ python main.py
Mode: 1 = live (Playwright), 2 = saved HTML, 3 = API [default 3]: 
Part number (e.g. AD5412AREZ): AD5412AREZ

============================================================
Part: AD5412AREZ
============================================================
→ Search via Digi-Key API
→ Found: AD5412AREZ
Stock: 1500 In Stock
ℹ Item in stock, no lead time needed.

  ✓ Parsed 1 rows:

  QTY             Ship Date
  ------------------------------
         1.500  11.01.2026
```

### Example 2: Web scraping
```bash
$ python main.py
Mode: 1 = live (Playwright), 2 = saved HTML, 3 = API [default 3]: 1
Part number (e.g. AD5412AREZ): UNKNOWN_PART

→ Fetching via Oxylabs: https://www.digikey.de/en/products/filter?keywords=UNKNOWN_PART...
→ Parsing search results
→ Fetching product page
→ Check stock status
Stock: 0 In Stock
→ Parse lead-time schedule

  ✓ Parsed 5 rows:

  QTY             Ship Date
  ------------------------------
         5.000  15.02.2026
        10.000  22.03.2026
        50.000  15.04.2026
       100.000  30.05.2026
```

---

## 🔐 Configuration

### Method 1: Environment Variables

```bash
# Digi-Key API
export DIGIKEY_CLIENT_ID="your_client_id"
export DIGIKEY_CLIENT_SECRET="your_client_secret"

# Oxylabs (optional, for web scraping)
export OXYLABS_USER="your_username"
export OXYLABS_PASS="your_password"
```

### Method 2: .env File
Create `.env` in project root:
```
DIGIKEY_CLIENT_ID=your_client_id
DIGIKEY_CLIENT_SECRET=your_client_secret
OXYLABS_USER=your_username
OXYLABS_PASS=your_password
```

Then load in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📦 Output Format

All modes return structured data:

```python
@dataclass
class IncomingStockRow:
    qty: int              # Quantity available/coming
    ship_date: datetime   # Estimated ship date (German format: dd.mm.yyyy)
```

Pretty-printed as table:
```
  QTY             Ship Date
  ------------------------------
       10.000  15.02.2026
       50.000  22.03.2026
```

---

## 🎯 Recommended Workflow

### For Development:
1. Use **Mode 2** (saved HTML) for testing parser logic
2. Use **Mode 1** (web scraping) for exploring DigiKey structure

### For Production:
1. Use **Mode 3** (API) as primary source ✓
2. Cache results (API has rate limits)
3. Implement fallback to saved HTML for known parts

---

## 🐛 Troubleshooting

### "digikey-api not available"
→ `pip install digikey-api`

### "Cloudflare verification triggered"
→ Use Oxylabs (Mode 1) or API (Mode 3)

### "Missing env vars"
→ Check [DIGIKEY_API_SETUP.md](DIGIKEY_API_SETUP.md)

### "No products found"
→ Part number may not exist on DigiKey Germany
→ Try exact manufacturer part number

---

## 📄 API Documentation

### Digi-Key API
- Official: https://developer.digikey.com/
- Setup Guide: [DIGIKEY_API_SETUP.md](DIGIKEY_API_SETUP.md)
- Python Client: https://pypi.org/project/digikey-api/

### Oxylabs (optional)
- Official: https://oxylabs.io/
- Pricing: Paid service (pay-as-you-go)

---

## 📈 Rate Limits

| Source | Limit | Cost |
|--------|-------|------|
| Digi-Key API | ~100 req/min | Free |
| Oxylabs | Depends on plan | Paid |
| Saved HTML | Unlimited | Free |

---

## 📝 License

MIT

---

## 🙋 Support

For issues with Digi-Key API setup, see [DIGIKEY_API_SETUP.md](DIGIKEY_API_SETUP.md)

For web scraping issues, check Oxylabs documentation.
