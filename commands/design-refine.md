---
allowed-tools: Bash, Read, Task, Glob, Grep, MultiEdit, Write, Edit, TodoWrite
argument-hint: [optional-url]
description: Analyze and iteratively refine website design until it meets professional standards
---

# Design Analysis and Refinement Loop

## Step 1: Determine the target URL
- If provided: use $1
- Otherwise: auto-detect from running dev server:
  - Next.js/React: localhost:3000
  - Vite: localhost:5173
  - Vue: localhost:8080
  - Nuxt: localhost:3000
  - Angular: localhost:4200
  - Python/Django: localhost:8000
  - Rails: localhost:3000
- Check package.json dev script for actual port configuration

## Step 2: Initial Screenshot Capture
Capture screenshots across different viewports using co command:
- Use Bash to run: co -b "screenshot of localhost:3000 full page"
- Use Bash to run: co -b "screenshot of localhost:3000 mobile"
- Use Bash to run: co -b "screenshot of localhost:3000 tablet"
- Use Bash to run: co -b "screenshot of localhost:3000 desktop"
(Replace localhost:3000 with detected URL)

## Step 3: Comprehensive Design Analysis
Use Task tool with ui-ux-design-auditor agent to analyze against 12 core design principles:

### 1. Visual Hierarchy ⭐ CRITICAL
**Target:** 5 clear levels of importance (H1 → H2 → H3 → Body → Caption)
- **Check:** Can user scan page in 5 seconds and understand structure?
- **Metrics:** Title = 2-3x body text size, H2 = 1.5-2x body, H3 = 1.25x body
- **Anti-pattern:** All text similar size, gradient text everywhere, competing focal points

### 2. Consistency ⭐ CRITICAL
**Target:** Same element = same style across entire site
- **Check:** Headers, buttons, cards, spacing uniform everywhere?
- **Metrics:** Max 3 button styles, max 5 text sizes, max 4 spacing values per section type
- **Anti-pattern:** py-12, py-16, py-20, py-24 mixed randomly; inconsistent button sizes

### 3. Typography Scale
**Target:** Systematic font size progression
- **Tailwind Scale:** text-xs (12px), text-sm (14px), text-base (16px), text-lg (18px), text-xl (20px), text-2xl (24px), text-3xl (30px), text-4xl (36px), text-5xl (48px), text-6xl (64px)
- **Recommended:**
  - Hero: text-6xl or text-5xl
  - Section H2: text-4xl or text-3xl
  - Section H3: text-2xl or text-xl
  - Body: text-base or text-lg
  - Small: text-sm
  - Caption: text-xs
- **Anti-pattern:** Random sizes like text-3xl and text-4xl for same heading level

### 4. Spacing System ⭐ CRITICAL
**Target:** 8px grid rhythm throughout
- **Tailwind Values:** 2 (8px), 4 (16px), 6 (24px), 8 (32px), 12 (48px), 16 (64px), 24 (96px), 32 (128px)
- **Section Padding:** py-12 (small), py-16 (medium), py-20 (large), py-24 (xl)
- **Element Spacing:** mb-4 (tight), mb-6 (normal), mb-8 (comfortable), mb-12 (spacious)
- **Anti-pattern:** mb-3, mb-5, mb-7, mb-9, mb-11 (breaks rhythm)

### 5. Color Harmony
**Target:** 3-color palette max (primary, accent, neutral)
- **Check:** Colors serve clear purpose (primary action, success, danger, info)?
- **WCAG AA:** Text contrast ratio ≥ 4.5:1, large text ≥ 3:1
- **Tool:** Use browser DevTools contrast checker
- **Anti-pattern:** 6+ colors, random color usage, purple button then green button

### 6. Responsive Layout
**Target:** Mobile-first, test at 375px, 768px, 1024px, 1440px
- **Breakpoints:** sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px)
- **Check:** Content readable without horizontal scroll at all sizes?
- **Anti-pattern:** Fixed pixel widths, content overflow, tiny mobile text

### 7. Alignment Grid
**Target:** Elements snap to invisible columns
- **Check:** Draw vertical lines - do elements align?
- **Max-width:** max-w-7xl (1280px) for most content, max-w-5xl (1024px) for text-heavy
- **Anti-pattern:** Random max-w-* values, elements not aligned, offset content

### 8. Interactive States
**Target:** All clickable elements have hover/focus/active states
- **Hover:** Color change, scale, shadow, underline
- **Focus:** Visible outline for keyboard navigation
- **Active:** Visual feedback on click
- **Anti-pattern:** No hover state, identical hover/default states

### 9. Accessibility
**Target:** WCAG AA compliance minimum
- **Keyboard:** Tab through all interactive elements
- **ARIA:** Labels on icons, descriptions on complex widgets
- **Focus indicators:** Visible outline on all focusable elements
- **Touch targets:** Minimum 44x44px (iOS) or 48x48px (Android)
- **Anti-pattern:** 32x32px buttons, no focus outline, unlabeled icons

### 10. User Flow
**Target:** Clear primary action per screen
- **Check:** What should user do first? Is it obvious?
- **CTA hierarchy:** 1 primary (bright/large), 2-3 secondary (subtle)
- **Anti-pattern:** 5 equal CTAs, no clear next step, buried main action

### 11. White Space
**Target:** 30-50% of page should be empty space
- **Check:** Does content breathe or feel cramped?
- **Sections:** 64-96px vertical spacing between major sections
- **Content:** 16-24px between paragraphs, 32-48px after headers
- **Anti-pattern:** Wall of text, no margins, cluttered layouts

### 12. Performance
**Target:** LCP < 2.5s, CLS < 0.1, FID < 100ms
- **Images:** Next.js Image component, WebP format, lazy loading
- **Layout shift:** Reserve space for images/ads, no pop-ins
- **Fonts:** Preload critical fonts, font-display: swap
- **Anti-pattern:** Huge images, no loading states, layout jumps

## Step 4: Create Prioritized Fix List
Use TodoWrite to track all issues found, categorized by severity:
- **Critical**: Accessibility failures, broken layouts, unreadable text
- **High**: Poor hierarchy, inconsistent spacing, bad contrast
- **Medium**: Missing hover states, alignment issues
- **Low**: Minor polish items

## Step 5: Iterative Refinement Loop
Repeat until all Critical and High issues are resolved:

1. Fix the top issue from the todo list
2. Capture new screenshots after fix:
   - Use Bash: co -b "screenshot of localhost:3000 full page"
   - Use Bash: co -b "screenshot of localhost:3000 mobile" (if mobile issues fixed)
   - Use Bash: co -b "screenshot of localhost:3000 tablet" (if tablet issues fixed)
   (Replace localhost:3000 with actual URL)
3. Verify the fix improved the design
4. Mark todo item as completed
5. Re-analyze if needed for new issues introduced
6. Continue to next issue

## Step 6: Final Quality Check
Design is considered "good" when:
- ✅ Clear visual hierarchy with proper emphasis
- ✅ Consistent spacing using 8px grid system
- ✅ All text meets WCAG AA contrast requirements
- ✅ Responsive at mobile, tablet, desktop breakpoints
- ✅ Consistent color palette throughout
- ✅ Professional typography with proper scale
- ✅ All interactive elements have clear states
- ✅ Proper alignment and grid structure
- ✅ Adequate white space and breathing room
- ✅ Clear user flow with prominent CTAs

## Step 7: Summary Report
Provide before/after comparison showing:
- Number of issues fixed
- Design score improvement
- Key transformations made
- Any remaining optional enhancements

Keep refining until the design looks professional and polished. Remember: keep simple things simple while ensuring the design is visually appealing and functional.