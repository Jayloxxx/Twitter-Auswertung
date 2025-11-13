# Statistical Calculation Updates - is_excluded Filter

## Summary

This document summarizes the changes made to `app.py` to filter out posts where `is_excluded=True` from all statistical calculations.

## Changes Applied

The script `update_stats_for_exclusion.py` successfully applied **6 updates** to `app.py`. A backup was created at `app.py.backup`.

### Filter Logic

The updated filter logic now follows this order:

1. Get all posts from active session
2. Filter out archived posts (`is_archived=False`)
3. **NEW: Filter out excluded posts (`is_excluded=False` or `not p.is_excluded`)**
4. Filter to only reviewed posts (`is_reviewed=True`)
5. Calculate statistics

## Detailed Changes

### 1. AnalysisSession.to_dict() - Line 66

**Location**: Model method for session summary statistics

**Before**:
```python
'reviewed_count': len([p for p in self.posts if p.is_reviewed]),
```

**After**:
```python
'reviewed_count': len([p for p in self.posts if p.is_reviewed and not p.is_excluded]),
```

**Impact**: Session-level reviewed count now excludes posts marked as excluded.

---

### 2. get_statistics() - Lines 972-973

**Location**: `/api/stats` endpoint - Main statistics endpoint

**Before**:
```python
# Nur nicht-archivierte Posts für Statistiken
active_posts = [p for p in all_posts if not p.is_archived]

# NUR REVIEWED POSTS für Statistiken verwenden (von nicht-archivierten)
posts = [p for p in active_posts if p.is_reviewed]
```

**After**:
```python
# Nur nicht-archivierte Posts für Statistiken
active_posts = [p for p in all_posts if not p.is_archived]

# Filter out excluded posts (is_excluded=True)
active_posts = [p for p in active_posts if not p.is_excluded]

# NUR REVIEWED POSTS für Statistiken verwenden (von nicht-archivierten)
posts = [p for p in active_posts if p.is_reviewed]
```

**Impact**: All descriptive statistics (mean, median, std dev, etc.) for TER, views, followers, likes, retweets, replies, bookmarks, and quotes now exclude posts marked as excluded.

---

### 3. get_distribution() - Lines 1056-1057

**Location**: `/api/stats/distribution` endpoint - Distribution data for charts

**Before**:
```python
# NUR Posts der aktiven Session
posts = TwitterPost.query.filter_by(session_id=active_session.id).all()

# TER-Verteilung (Bins)
```

**After**:
```python
# NUR Posts der aktiven Session
posts = TwitterPost.query.filter_by(session_id=active_session.id).all()

# Filter out archived and excluded posts
posts = [p for p in posts if not p.is_archived and not p.is_excluded]

# TER-Verteilung (Bins)
```

**Impact**: TER distribution charts now exclude both archived and excluded posts.

---

### 4. get_timeline_stats() - Lines 1088-1093

**Location**: `/api/stats/timeline` endpoint - Timeline statistics for charts

**Before**:
```python
# NUR REVIEWED POSTS DER AKTIVEN SESSION (OHNE ARCHIVIERTE)
all_posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False
).all()
```

**After**:
```python
# NUR REVIEWED POSTS DER AKTIVEN SESSION (OHNE ARCHIVIERTE UND EXCLUDED)
all_posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False,
    is_excluded=False
).all()
```

**Impact**: Monthly and yearly timeline statistics now exclude posts marked as excluded.

---

### 5. get_advanced_stats() - Lines 1206-1212

**Location**: `/api/stats/advanced` endpoint - Advanced statistical analyses (correlation, regression, group comparisons)

**Before**:
```python
# NUR REVIEWED POSTS DER AKTIVEN SESSION mit TER-Werten (OHNE ARCHIVIERTE)
posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False
).all()
```

**After**:
```python
# NUR REVIEWED POSTS DER AKTIVEN SESSION mit TER-Werten (OHNE ARCHIVIERTE UND EXCLUDED)
posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False,
    is_excluded=False
).all()
```

**Impact**: All advanced statistics including:
- Correlation analysis (Pearson)
- Regression analysis (Linear regression)
- Group comparisons (t-tests)

Now exclude posts marked as excluded.

---

### 6. export_reviewed_posts_pdf() - Lines 2049-2055

**Location**: `/api/posts/reviewed/export-pdf` endpoint - PDF export of reviewed posts

**Before**:
```python
# Hole alle reviewed Posts der aktiven Session (ohne archivierte)
posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False
).order_by(TwitterPost.ter_manual.desc().nullslast()).all()
```

**After**:
```python
# Hole alle reviewed Posts der aktiven Session (ohne archivierte und excluded)
posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False,
    is_excluded=False
).order_by(TwitterPost.ter_manual.desc().nullslast()).all()
```

**Impact**: PDF exports now exclude posts marked as excluded.

---

### 7. export_reviewed_posts_excel() - Lines 2376-2382

**Location**: `/api/posts/reviewed/export-excel` endpoint - Excel export of reviewed posts

**Status**: ✓ Already correctly implemented

This endpoint was already filtering out excluded posts (the comment and query both included is_excluded=False). No changes were needed.

```python
# Hole alle reviewed Posts der aktiven Session (ohne archivierte und excluded)
posts = TwitterPost.query.filter_by(
    session_id=active_session.id,
    is_reviewed=True,
    is_archived=False,
    is_excluded=False
).order_by(TwitterPost.ter_manual.desc().nullslast()).all()
```

---

## Endpoints NOT Modified

The following endpoints were intentionally NOT modified as they should show all posts for UI/management purposes:

### get_posts() - Line 616
**Location**: `/api/posts` endpoint - Retrieves posts for the UI

**Why not modified**: This endpoint is used to display posts in the UI. Users need to see excluded posts so they can mark/unmark them as excluded. This is a display endpoint, not a statistics endpoint.

---

## Testing Recommendations

1. **Verify Statistics Calculation**:
   - Mark some posts as `is_excluded=True`
   - Check that they don't appear in:
     - Descriptive statistics (mean, median, etc.)
     - Distribution charts
     - Timeline charts
     - Advanced statistics (correlation, regression)
     - PDF/Excel exports

2. **Verify Session Counts**:
   - Check that the `reviewed_count` in session statistics excludes excluded posts

3. **Verify UI Display**:
   - Confirm that excluded posts are still visible in the main posts list
   - Verify that the exclusion toggle works correctly

4. **Verify Exports**:
   - Export reviewed posts to PDF and Excel
   - Confirm that excluded posts are not included in the exports

---

## Database Schema

The `is_excluded` field already exists in the database:

```python
is_excluded = db.Column(db.Boolean, default=False)  # Aus Statistiken ausschließen
```

No database migration is required.

---

## Files Modified

- `app.py` - Main application file with all statistical endpoints
- `app.py.backup` - Backup of original file before changes

## Files Created

- `update_stats_for_exclusion.py` - Script that applies the updates
- `EXCLUSION_FILTER_CHANGES.md` - This documentation file

---

## Rollback Instructions

If you need to rollback these changes:

```bash
# Restore from backup
cp app.py.backup app.py
```

Or use git:

```bash
# Discard changes
git checkout app.py
```

---

## Date

Changes applied: 2025-11-13
