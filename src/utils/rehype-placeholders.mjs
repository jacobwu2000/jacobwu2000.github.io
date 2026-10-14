// Wraps each "[PLACEHOLDER: …]" in Markdown/MDX content in
// <span class="placeholder">, so unfinished work is visibly marked on the
// page while the source keeps the greppable "[PLACEHOLDER:" prefix.
// A placeholder may run across inline elements (e.g. *italics*); it ends at
// the "]" that balances its opening "[".

const OPEN = '[PLACEHOLDER:';

const isPlaceholderSpan = (node) =>
  node.type === 'element' && (node.properties?.className || []).includes('placeholder');

function wrap(parent) {
  const kids = parent.children;
  const out = [];
  let i = 0;
  while (i < kids.length) {
    const kid = kids[i];
    const start = kid.type === 'text' ? kid.value.indexOf(OPEN) : -1;
    if (start < 0) {
      out.push(kid);
      i += 1;
      continue;
    }
    if (start > 0) out.push({ type: 'text', value: kid.value.slice(0, start) });

    const inner = [];
    let depth = 0;
    let node = { type: 'text', value: kid.value.slice(start) };
    let j = i;
    let rest = null;
    while (node) {
      if (node.type === 'text') {
        let end = -1;
        for (let p = 0; p < node.value.length; p += 1) {
          if (node.value[p] === '[') depth += 1;
          else if (node.value[p] === ']' && --depth === 0) { end = p; break; }
        }
        if (end >= 0) {
          inner.push({ type: 'text', value: node.value.slice(0, end + 1) });
          const after = node.value.slice(end + 1);
          if (after) rest = { type: 'text', value: after };
          break;
        }
      }
      inner.push(node);
      j += 1;
      node = kids[j];
    }
    out.push({
      type: 'element',
      tagName: 'span',
      properties: { className: ['placeholder'] },
      children: inner,
    });
    if (rest) {
      // Keep scanning the remainder of this text node for another placeholder.
      kids[j] = rest;
      i = j;
    } else {
      i = j + 1;
    }
  }
  parent.children = out;
}

function walk(node) {
  if (!node.children || isPlaceholderSpan(node)) return;
  wrap(node);
  node.children.forEach(walk);
}

export default function rehypePlaceholders() {
  return (tree) => walk(tree);
}
