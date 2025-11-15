---
allowed-tools: Bash, Read, Task, Glob, Grep, MultiEdit, Write, Edit, TodoWrite
argument-hint: [optional-url]
description: Analyze and iteratively refine website design until it meets professional standards
---

# Design Analysis and Refinement Loop

## ConnectOnion Design System (Single Fixed Pattern)

**CRITICAL: Use EXACTLY these values. No alternatives. No ranges. One pattern for consistency.**

### Typography (ONE size per element type)
- **Hero (H1):** `text-6xl` (64px) - Responsive: `text-4xl md:text-5xl lg:text-6xl`
- **Section Heading (H2):** `text-4xl` (36px) - Responsive: `text-2xl md:text-3xl lg:text-4xl`
- **Subsection (H3):** `text-2xl` (24px) - Responsive: `text-xl md:text-2xl`
- **Emphasized:** `text-xl` (20px)
- **Body:** `text-lg` (18px)
- **Small:** `text-sm` (14px)
- **Caption:** `text-xs` (12px)

### Spacing (8px grid - ONE value per use case)
- **Tight:** `mb-2` (8px) - icon + text
- **Normal:** `mb-4` (16px) - standard spacing
- **Comfortable:** `mb-6` (24px) - heading → content
- **Spacious:** `mb-8` (32px) - content blocks
- **Section:** `mb-12` (48px) - major sections
- **Large Section:** `mb-16` (64px) - rare cases
- **Section Padding:** `py-16 md:py-24` - ALL sections use this

### Colors (ONE color per purpose)
- **Primary Action:** `green-400` - success, CTAs
- **Interactive:** `purple-400` - links, focus
- **Info:** `blue-400` - secondary actions
- **Warning:** `orange-400` - alerts
- **Error:** `red-400` - errors
- **Text Heading:** `white` - headings
- **Text Body:** `slate-100` - body text (WCAG AA)
- **Text Muted:** `slate-200` - metadata
- **Borders:** `gray-300`, `gray-700`, `gray-800`

### Touch Targets
- **Minimum:** `min-h-[48px]` for all interactive elements

### Common Code Patterns

**Section Structure:**
```tsx
<section className="py-16 md:py-24 px-4 md:px-6">
  <div className="max-w-4xl mx-auto">
    <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold text-white mb-6">Section Title</h2>
    <p className="text-lg text-slate-100 mb-8">Body content...</p>
  </div>
</section>
```

**Card Pattern:**
```tsx
<div className="p-6 bg-gray-800/30 rounded-lg border border-gray-700 hover:border-purple-400/50 hover:bg-gray-800/50 transition-all">
  <Icon className="w-8 h-8 text-purple-400 mb-4" />
  <h3 className="font-semibold text-white mb-2">Card Title</h3>
  <p className="text-sm text-slate-100">Card content</p>
</div>
```

**Hero Pattern:**
```tsx
<section className="py-16 md:py-24 px-4 md:px-6">
  <div className="max-w-3xl mx-auto text-center">
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">Hero Title</h1>
    <p className="text-xl md:text-2xl lg:text-3xl text-slate-50 mb-10">Hero subtitle</p>
  </div>
</section>
```

### Anti-Patterns to Avoid
```tsx
❌ <h2 className="text-3xl">           // Should be text-4xl
❌ <h2 className="text-5xl">           // Should be text-4xl
❌ <section className="py-12">         // Should be py-16 md:py-24
❌ <p className="text-base">           // Should be text-lg
❌ <p className="text-slate-200">      // Should be text-slate-100
❌ <div className="mb-3">              // Should be mb-2 or mb-4
❌ <button className="h-10">           // Should have min-h-[48px]
```

---

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
Use Task tool with ui-ux-design-auditor agent to analyze against 13 core design principles:

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

### 3. Typography Scale ⭐ CRITICAL
**Target:** Single, consistent font size for each element type (NO alternatives)
- **Fixed Scale (ConnectOnion Standard):**
  - **Hero (H1):** text-6xl (64px) - ONE size only
  - **Section Heading (H2):** text-4xl (36px) - ONE size only
  - **Subsection (H3):** text-2xl (24px) - ONE size only
  - **Emphasized Text:** text-xl (20px) - for important body text
  - **Body Text:** text-lg (18px) - standard paragraph text
  - **Small Text:** text-sm (14px) - for metadata, labels
  - **Caption/Tiny:** text-xs (12px) - for captions, footnotes
- **Responsive Scaling:** Use md: and lg: prefixes for responsive growth, but keep same base scale
  - Example: `text-4xl md:text-5xl lg:text-6xl` for responsive hero (grows to 6xl on large screens)
  - Example: `text-2xl md:text-3xl lg:text-4xl` for responsive H2 (grows to 4xl on large screens)
- **Anti-pattern:** Multiple sizes for same heading level, text-3xl and text-4xl mixed for H2s, text-5xl anywhere except responsive hero

### 4. Spacing System ⭐ CRITICAL
**Target:** Single, consistent 8px grid spacing (NO alternatives)
- **Fixed Spacing Scale (ConnectOnion Standard):**
  - **Tight:** mb-2 (8px) - between related elements like icon + text
  - **Normal:** mb-4 (16px) - standard element spacing
  - **Comfortable:** mb-6 (24px) - between heading and content
  - **Spacious:** mb-8 (32px) - between distinct content blocks
  - **Section:** mb-12 (48px) - between major sections within a container
  - **Large Section:** mb-16 (64px) - rarely used, for special cases
- **Section Vertical Padding (ONE standard):**
  - **Standard:** py-16 md:py-24 - ALL sections use this (responsive: 64px mobile, 96px desktop)
  - Never use: py-12, py-20, py-32 - these break consistency
- **NEVER use:** mb-1, mb-3, mb-5, mb-7, mb-9, mb-10, mb-11 (breaks 8px grid rhythm)
- **Anti-pattern:** Mixing py-12, py-16, py-20, py-24 across sections; using odd spacing values

### 5. Color Harmony ⭐ CRITICAL
**Target:** Single, consistent color for each purpose (ConnectOnion Standard)
- **Fixed Color Palette:**
  - **Primary Action:** green-400 (#4ade80) - success, primary CTAs, positive indicators
  - **Interactive/Focus:** purple-400 (#c084fc) - links, hover states, focus indicators
  - **Information:** blue-400 (#60a5fa) - informational elements, secondary actions
  - **Warning:** orange-400 (#fb923c) - warnings, alerts
  - **Error:** red-400 (#f87171) - errors, destructive actions
  - **Text Primary:** white (#ffffff) - headings, important text
  - **Text Secondary:** slate-100 (#f1f5f9) - body text (WCAG AA compliant)
  - **Text Muted:** slate-200 (#e2e8f0) - metadata, less important text
  - **Borders/Dividers:** gray-300, gray-700, gray-800 - borders and separators
- **WCAG AA Compliance:**
  - Use slate-100 (not slate-200 or slate-300) for body text on dark backgrounds
  - Text contrast ratio ≥ 4.5:1, large text ≥ 3:1
- **Anti-pattern:** Using multiple shades for same purpose, text-slate-300 for body text (too low contrast), mixing color purposes

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

### 12. Icon Consistency
**Target:** Use brand-specific icons from react-icons for social media and platforms
- **Social Media:** Use FaDiscord, FaGithub, FaTwitter, FaYoutube, FaLinkedin, FaInstagram, FaTiktok from 'react-icons/fa'
- **Platforms:** Use FaGithub (not GitBranch), FaPython (for PyPI), FaDiscord (not MessageCircle)
- **UI Elements:** lucide-react is fine for generic UI icons (Copy, Check, ChevronDown, etc.)
- **Anti-pattern:** Using generic lucide icons (Github, MessageCircle, etc.) for branded platforms

### 13. Performance
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
Design is considered "good" when it follows the ConnectOnion Design System EXACTLY:

**Typography Compliance:**
- ✅ Hero uses ONLY text-6xl (or responsive text-4xl md:text-5xl lg:text-6xl)
- ✅ H2 uses ONLY text-4xl (or responsive text-2xl md:text-3xl lg:text-4xl)
- ✅ H3 uses ONLY text-2xl (no text-3xl mixed in)
- ✅ Body text uses text-lg (not text-base)
- ✅ NO text-5xl except in responsive hero scaling

**Spacing Compliance:**
- ✅ ALL sections use py-16 md:py-24 (no py-12, py-20, py-32)
- ✅ ONLY uses mb-2, mb-4, mb-6, mb-8, mb-12, mb-16 (no mb-1, mb-3, mb-5, mb-10, etc.)
- ✅ Consistent spacing: same element type = same mb-* value everywhere

**Color Compliance:**
- ✅ Body text uses slate-100 (not slate-200 or slate-300)
- ✅ WCAG AA: All text ≥ 4.5:1 contrast ratio
- ✅ Consistent color purpose: green-400 for primary, purple-400 for interactive, etc.

**Interaction Compliance:**
- ✅ All interactive elements have min-h-[48px]
- ✅ All cards have hover states (hover:border-*, hover:bg-*)
- ✅ Brand icons use react-icons (FaGithub, FaDiscord, not lucide)

## Step 7: Summary Report
Provide before/after comparison showing:
- Number of issues fixed
- Design score improvement
- Key transformations made
- Any remaining optional enhancements

Keep refining until the design looks professional and polished. Remember: keep simple things simple while ensuring the design is visually appealing and functional.