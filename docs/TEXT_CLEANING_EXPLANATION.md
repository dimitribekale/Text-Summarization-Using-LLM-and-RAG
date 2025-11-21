# Text Cleaning & Chunking Detailed Explanation

## Part 1: _clean_text() - The Matching Logic

Let me walk you through the tricky section step by step.

### The Setup

```python
earliest_match = None
earliest_position = len(text)
```

**What this does:**
- `earliest_match = None` - Initially, we haven't found any match
- `earliest_position = len(text)` - Set to the END of the entire text

**Example:**
```python
text = "The document starts here. References\n Some citations. Appendix A\n More stuff."
len(text) = 78  # Total characters

earliest_position = 78  # Assume no section found initially
earliest_match = None
```

---

### The Loop: Finding the Earliest Section

```python
for pattern in sections_to_remove:
    match = re.search(pattern, text_lower)
    if match:
        if match.start() < earliest_position:
            earliest_position = match.start()
            earliest_match = match
```

**What this does:**

For EACH pattern (References, Bibliography, Appendix, etc.), we:
1. Search for it in the text
2. If found, check if it comes BEFORE our current earliest match
3. If so, update our "earliest" position

**Concrete Example:**

```python
text = """
Introduction

Main content here.

References
[1] Smith, J. 2020
[2] Jones, M. 2021

Appendix A
Additional information
"""

text_lower = text.lower()

# Pattern 1: r'references?\s*\n'
match1 = re.search(r'references?\s*\n', text_lower)
if match1:
    print(f"Found 'References' at position: {match1.start()}")
    # Output: Found 'References' at position: 47

earliest_position = 47
earliest_match = match1

# Pattern 2: r'appendix\s+[a-z]?\s*\n'
match2 = re.search(r'appendix\s+[a-z]?\s*\n', text_lower)
if match2:
    print(f"Found 'Appendix A' at position: {match2.start()}")
    # Output: Found 'Appendix A' at position: 95

# Is 95 < 47? NO
# So we DON'T update. Keep earliest_position = 47
# Because References comes BEFORE Appendix
```

**Why track the earliest?**

Because we want to remove from the FIRST unwanted section onwards. Everything after that point is probably not useful.

---

### The Final Cut

```python
if earliest_match:
    text = text[:earliest_match.start()]
    self.logger.debug(f"Removed text after: {earliest_match.group()}")

return text.strip()
```

**What this does:**

```python
# Original text with positions marked:
text = "Intro. [0-46] References [47-95] Appendix [96-end]"
#                                  ↑ earliest_match.start() = 47

# text[:47] keeps everything BEFORE position 47
text = "Intro. [0-46]"
#       Everything up to (but not including) position 47

# .strip() removes leading/trailing whitespace
text = "Intro."
```

**Visual Example:**

```python
original = "The document starts here.\n\nReferences\n[1] Smith\n[2] Jones"
           "0         1         2         3         4         5"
           "0123456789012345678901234567890123456789012345678901234"

# Find "References\n"
match.start() = 31

text[:31] = "The document starts here.\n\n"
text.strip() = "The document starts here."
```

---

## Part 2: _chunk_text() - The While Loop Explained

Now let's go through the chunking logic with multiple detailed examples.

### The Variables

```python
chunks = []
start = 0

while start < len(text):
    end = min(start + chunk_size, len(text))
    chunk = text[start:end]
    chunks.append(chunk)
    step = chunk_size - overlap
    start += step
```

Let me trace through this with a detailed example.

---

### Example 1: Simple Case

```python
text = "AAABBBCCCDDDEEEFFFGGG"
chunk_size = 5
overlap = 2
```

**Visual representation of the text:**

```
Position: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
Content:  A  A  A  B  B  B  C  C  C  D  D  D  E  E  E  F  F  F  G  G  G
```

**Iteration 1:**
```python
start = 0
end = min(0 + 5, 21) = min(5, 21) = 5
chunk = text[0:5] = "AAABB"
chunks = ["AAABB"]

step = 5 - 2 = 3
start = 0 + 3 = 3  # Move forward by 3 positions
```

**After iteration 1:**
```
Positions we took:  [0,1,2,3,4]
Next will start at: 3
                    ↓
Position: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
Content:  A  A  A  B  B  B  C  C  C  D  D  D  E  E  E  F  F  F  G  G  G
Chunk 1:  [     ]
                 ↑ Overlap: positions 3,4 will be in next chunk
```

---

**Iteration 2:**
```python
start = 3  # From previous iteration
end = min(3 + 5, 21) = min(8, 21) = 8
chunk = text[3:8] = "BBBCC"
chunks = ["AAABB", "BBBCC"]

# Notice: positions 3,4 (BB) are in BOTH chunks = overlap
# Position 0,1,2 only in chunk 1
# Position 5,6,7 only in chunk 2

step = 5 - 2 = 3
start = 3 + 3 = 6  # Move forward by 3 more positions
```

**After iteration 2:**
```
Position: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
Content:  A  A  A  B  B  B  C  C  C  D  D  D  E  E  E  F  F  F  G  G  G
Chunk 1:  [     ]
Chunk 2:        [     ]  ← Notice overlap with chunk 1
                 ↑ Overlap: positions 5,6 will be in next chunk
```

---

**Iteration 3:**
```python
start = 6
end = min(6 + 5, 21) = min(11, 21) = 11
chunk = text[6:11] = "CCCDD"
chunks = ["AAABB", "BBBCC", "CCCDD"]

step = 5 - 2 = 3
start = 6 + 3 = 9
```

---

**Iteration 4:**
```python
start = 9
end = min(9 + 5, 21) = min(14, 21) = 14
chunk = text[9:14] = "DDDEE"
chunks = ["AAABB", "BBBCC", "CCCDD", "DDDEE"]

step = 5 - 2 = 3
start = 9 + 3 = 12
```

---

**Iteration 5:**
```python
start = 12
end = min(12 + 5, 21) = min(17, 21) = 17
chunk = text[12:17] = "EEEEF"
chunks = ["AAABB", "BBBCC", "CCCDD", "DDDEE", "EEEEF"]

step = 5 - 2 = 3
start = 12 + 3 = 15
```

---

**Iteration 6:**
```python
start = 15
end = min(15 + 5, 21) = min(20, 21) = 20
chunk = text[15:20] = "FFFGG"
chunks = ["AAABB", "BBBCC", "CCCDD", "DDDEE", "EEEEF", "FFFGG"]

step = 5 - 2 = 3
start = 15 + 3 = 18
```

---

**Iteration 7:**
```python
start = 18
end = min(18 + 5, 21) = min(23, 21) = 21  # min() chooses 21!
chunk = text[18:21] = "GGG"
chunks = ["AAABB", "BBBCC", "CCCDD", "DDDEE", "EEEEF", "FFFGG", "GGG"]

step = 5 - 2 = 3
start = 18 + 3 = 21
```

---

**While condition check:**
```python
while start < len(text):
    # 21 < 21? NO
    # Loop ends!
```

---

### Final Result

```python
chunks = [
    "AAABB",  # Positions 0-4
    "BBBCC",  # Positions 3-7  (overlaps "BB" with previous)
    "CCCDD",  # Positions 6-10 (overlaps "CC" with previous)
    "DDDEE",  # Positions 9-13 (overlaps "DD" with previous)
    "EEEEF",  # Positions 12-16 (overlaps "EE" with previous)
    "FFFGG",  # Positions 15-19 (overlaps "FF" with previous)
    "GGG"     # Positions 18-20 (overlaps "GG" with previous)
]
```

**Overlap visualization:**
```
Chunk 1: AAABB
Chunk 2:    BBBCC     ← "BB" overlaps
Chunk 3:       CCCDD  ← "CC" overlaps
```

---

### Example 2: With Real Text

```python
text = "The quick brown fox jumps over the lazy dog"
#      Positions: 0        10       20       30       40
chunk_size = 15
overlap = 5
```

**Iteration 1:**
```python
start = 0
end = min(0 + 15, 44) = 15
chunk = text[0:15] = "The quick brow"
step = 15 - 5 = 10
start = 0 + 10 = 10
```

**Iteration 2:**
```python
start = 10
end = min(10 + 15, 44) = 25
chunk = text[10:25] = "brown fox jumps"
#              Notice "brown " overlaps with previous chunk

step = 15 - 5 = 10
start = 10 + 10 = 20
```

**Iteration 3:**
```python
start = 20
end = min(20 + 15, 44) = min(35, 44) = 35
chunk = text[20:35] = "jumps over the "
#          Notice "jumps " overlaps with previous chunk

step = 15 - 5 = 10
start = 20 + 10 = 30
```

**Iteration 4:**
```python
start = 30
end = min(30 + 15, 44) = min(45, 44) = 44  # min() picks 44!
chunk = text[30:44] = "e lazy dog"
#          Only 14 characters because text ends at 44

step = 15 - 5 = 10
start = 30 + 10 = 40
```

**Iteration 5:**
```python
while 40 < 44:  # YES, continue
start = 40
end = min(40 + 15, 44) = min(55, 44) = 44
chunk = text[40:44] = "dog"

step = 15 - 5 = 10
start = 40 + 10 = 50
```

**Iteration 6:**
```python
while 50 < 44:  # NO, stop!
```

---

## Why the `min()` is Important

```python
end = min(start + chunk_size, len(text))
```

This ensures we don't go beyond the text length.

**Without `min()`:**
```python
text = "AAABBB"  # Length 6
start = 4
end = 4 + 5 = 9  # WRONG! Out of bounds

chunk = text[4:9]  # Would be "BB" (Python handles it, but inefficient)
```

**With `min()`:**
```python
text = "AAABBB"  # Length 6
start = 4
end = min(4 + 5, 6) = min(9, 6) = 6  # Correct!

chunk = text[4:6]  # "BB"
```

---

## Key Takeaways

### For `_clean_text()`:
- `earliest_position` tracks which section comes first
- We compare each match to find the earliest one
- Then we keep only text BEFORE that section
- Everything after (References, Bibliography, etc.) is discarded

### For `_chunk_text()`:
- Start at position 0
- Take `chunk_size` characters
- Move forward by `(chunk_size - overlap)` positions
- This creates overlapping chunks for context
- The overlap helps semantic search understand connections
- `min()` handles the last chunk which might be smaller
