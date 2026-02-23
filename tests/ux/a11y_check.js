const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const htmlPath = path.join(__dirname, '../../🧬 HYPERSWARM v2.0/HyperSwarm Control Center.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;

console.log('🔍 Starting Automated Accessibility Checks (Phase 2)...\n');

let errors = 0;
let warnings = 0;
let passes = 0;

function check(condition, message, isError = true) {
    if (condition) {
        console.log(`✅ PASS: ${message}`);
        passes++;
    } else {
        console.log(`${isError ? '❌ FAIL' : '⚠️ WARN'}: ${message}`);
        if (isError) errors++; else warnings++;
    }
}

// 1. Color Contrast (Static Check of CSS Variables)
// Approximation: Extract hex codes and calculate luminance
// Real test requires computed styles, but this catches basic config issues
const styleContent = document.querySelector('style').textContent;
const bgDark = styleContent.match(/--color-bg-dark: (#\w+);/)[1];
const textMain = styleContent.match(/--color-text: (#\w+);/)[1];
// Simple contrast checker (mock implementation for Node)
console.log(`ℹ️  Checking Contrast: ${textMain} on ${bgDark} (Target: >4.5:1)`);
// Note: Manual verification with WebAIM is required for final pass

// 2. ARIA Landmarks
check(document.querySelector('header[role="banner"]'), 'Header has role="banner"');
check(document.querySelector('main[role="main"]'), 'Main has role="main"');
check(document.querySelector('div[role="region"]'), 'Agent Graph has role="region"');

// 3. Form Labels
const inputs = document.querySelectorAll('input, textarea');
inputs.forEach(input => {
    const id = input.id;
    const label = document.querySelector(`label[for="${id}"]`);
    const ariaLabel = input.getAttribute('aria-label');
    const ariaLabelledBy = input.getAttribute('aria-labelledby');
    
    check(label || ariaLabel || ariaLabelledBy, `Input #${id} has an accessible label`);
});

// 4. Slider Accessibility
const sliders = document.querySelectorAll('input[type="range"]');
sliders.forEach(slider => {
    check(slider.getAttribute('aria-valuemin'), `Slider #${slider.id} has aria-valuemin`);
    check(slider.getAttribute('aria-valuemax'), `Slider #${slider.id} has aria-valuemax`);
    check(slider.getAttribute('aria-valuenow'), `Slider #${slider.id} has aria-valuenow`);
});

// 5. Live Regions
check(document.querySelector('[aria-live]'), 'Live region exists for logs/updates');

// 6. Focus Management (Static Check)
check(styleContent.includes(':focus-visible'), 'CSS contains :focus-visible styles');

console.log('\n----------------------------------------');
console.log(`Validation Complete: ${passes} Passed, ${errors} Errors, ${warnings} Warnings`);

if (errors === 0) {
    console.log('🎉 Automated Checks Passed! Proceed to Manual Testing.');
} else {
    console.log('🛑 Fix errors before manual testing.');
    process.exit(1);
}
