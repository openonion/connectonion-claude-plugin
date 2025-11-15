# ConnectOnion Design System

**ONE pattern. NO alternatives. Complete consistency.**

## Typography Scale

### Desktop Sizes (Base)
```
Hero (H1):     text-6xl (64px)
H2:            text-4xl (36px)
H3:            text-2xl (24px)
Emphasized:    text-xl  (20px)
Body:          text-lg  (18px)
Small:         text-sm  (14px)
Caption:       text-xs  (12px)
```

### Responsive Patterns
```tsx
// Hero - grows from 4xl → 5xl → 6xl
<h1 className="text-4xl md:text-5xl lg:text-6xl">

// H2 - grows from 2xl → 3xl → 4xl
<h2 className="text-2xl md:text-3xl lg:text-4xl">

// H3 - grows from xl → 2xl
<h3 className="text-xl md:text-2xl">

// Body stays consistent
<p className="text-lg">
```

## Spacing System (8px Grid)

### Margin Bottom
```
mb-2   (8px)   - Tight (icon + text)
mb-4   (16px)  - Normal (standard spacing)
mb-6   (24px)  - Comfortable (heading → content)
mb-8   (32px)  - Spacious (content blocks)
mb-12  (48px)  - Section (major sections)
mb-16  (64px)  - Large Section (rare)
```

### Section Padding
```tsx
// ALL sections use this pattern
<section className="py-16 md:py-24">
```

### NEVER Use
```
❌ mb-1, mb-3, mb-5, mb-7, mb-9, mb-10, mb-11
❌ py-12, py-20, py-32
```

## Color Palette

### Functional Colors
```
green-400   - Primary action, success, CTAs
purple-400  - Interactive, links, focus states
blue-400    - Information, secondary actions
orange-400  - Warnings, alerts
red-400     - Errors, destructive actions
```

### Text Colors
```
white       - Headings, important text
slate-100   - Body text (WCAG AA compliant)
slate-200   - Metadata, muted text
```

### UI Colors
```
gray-300, gray-700, gray-800  - Borders, dividers
```

### Examples
```tsx
// Primary CTA
<button className="bg-green-400 text-white hover:bg-green-500">

// Interactive link
<a className="text-purple-400 hover:text-purple-300">

// Body text on dark background
<p className="text-slate-100">

// Card border with hover
<div className="border-gray-700 hover:border-purple-400/50">
```

## Interactive States

### Touch Targets
```tsx
// Minimum size for all clickable elements
className="min-h-[48px]"
```

### Hover States
```tsx
// Cards
className="border-gray-700 hover:border-purple-400/50 hover:bg-gray-800/50 transition-all"

// Buttons
className="bg-green-400 hover:bg-green-500 transition-colors"

// Links
className="text-purple-400 hover:text-purple-300 transition-colors"
```

## Common Patterns

### Section Structure
```tsx
<section className="py-16 md:py-24 px-4 md:px-6">
  <div className="max-w-4xl mx-auto">
    <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold text-white mb-6">
      Section Title
    </h2>
    <p className="text-lg text-slate-100 mb-8">
      Body content goes here...
    </p>
  </div>
</section>
```

### Card Pattern
```tsx
<div className="p-6 bg-gray-800/30 rounded-lg border border-gray-700 hover:border-purple-400/50 hover:bg-gray-800/50 transition-all">
  <Icon className="w-8 h-8 text-purple-400 mb-4" />
  <h3 className="font-semibold text-white mb-2">Card Title</h3>
  <p className="text-sm text-slate-100">Card content</p>
</div>
```

### Hero Pattern
```tsx
<section className="py-16 md:py-24 px-4 md:px-6">
  <div className="max-w-3xl mx-auto text-center">
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
      Hero Title
    </h1>
    <p className="text-xl md:text-2xl lg:text-3xl text-slate-50 mb-10">
      Hero subtitle
    </p>
  </div>
</section>
```

## Validation Checklist

- [ ] Hero uses `text-6xl` (or responsive `text-4xl md:text-5xl lg:text-6xl`)
- [ ] All H2s use `text-4xl` (or responsive `text-2xl md:text-3xl lg:text-4xl`)
- [ ] All H3s use `text-2xl` (or responsive `text-xl md:text-2xl`)
- [ ] Body text uses `text-lg`
- [ ] All sections use `py-16 md:py-24`
- [ ] Only uses `mb-2, mb-4, mb-6, mb-8, mb-12, mb-16`
- [ ] Body text uses `slate-100` (not `slate-200` or `slate-300`)
- [ ] All interactive elements have `min-h-[48px]`
- [ ] All cards have hover states
- [ ] Brand icons use `react-icons/fa` (FaGithub, FaDiscord, etc.)

## Anti-Patterns to Avoid

```tsx
❌ <h2 className="text-3xl">           // Should be text-4xl
❌ <h2 className="text-5xl">           // Should be text-4xl
❌ <section className="py-12">         // Should be py-16 md:py-24
❌ <section className="py-20">         // Should be py-16 md:py-24
❌ <p className="text-slate-200">      // Should be text-slate-100
❌ <div className="mb-3">              // Should be mb-2 or mb-4
❌ <div className="mb-10">             // Should be mb-8 or mb-12
❌ <button className="h-10">           // Should have min-h-[48px]
```
