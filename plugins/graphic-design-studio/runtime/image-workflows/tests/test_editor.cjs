/* Small DOM harness for the editor's real event handlers; no browser process. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

class Node {
  constructor(tag = 'fragment') { this.tagName = tag; this.children = []; this.listeners = {}; this.attributes = {}; this.hidden = false; this.value = ''; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  addEventListener(type, handler) { this.listeners[type] = handler; }
  dispatch(type) { this.listeners[type]?.({target: this}); }
  setAttribute(name, value) { this.attributes[name] = value; }
  removeAttribute(name) { delete this.attributes[name]; }
  focus() { Node.focused = this; }
  querySelectorAll(selector) { const result = []; const visit = node => { if (selector === 'input:checked' && node.tagName === 'input' && node.checked) result.push(node); for (const child of node.children) visit(child); }; visit(this); return result; }
}
const document = {createElement: tag => new Node(tag), createDocumentFragment: () => new Node()};
const window = {};
const context = {document, window, Option: class extends Node { constructor(label, value) { super('option'); this.textContent = label; this.value = value; } }};
const source = fs.readFileSync(path.join(__dirname, '..', 'ui', 'editor.js'), 'utf8');
vm.runInNewContext(source, context);
const editor = window.ImageWorkflowEditor;
const host = new Node('div');
const poster = {id:'poster', name:'Poster', revision:'2026-10-06.1', ratio:'2:3', detail:'Balanced', reference:'optional', exampleSubject:'A night-sky event', prompt:'Make a clear poster.', checks:['Readable hierarchy']};
const portrait = {id:'portrait', name:'Portrait edit', revision:'2026-10-06.1', ratio:'4:5', detail:'Detailed', reference:'required', exampleSubject:'A headshot', prompt:'Preserve likeness.', checks:[]};
function byId(id) { let found; const walk = n => { if (n.id === id) found = n; for (const child of n.children) walk(child); }; walk(host); return found; }
let changes = 0;
editor.mount({item:poster, host, onChange:() => changes++});
assert.equal(byId('image-subject').value, '');
assert.equal(byId('image-subject').placeholder, 'For example: A night-sky event');
assert.equal(editor.hasMissing(), true);
assert.equal(editor.validate(), false);
assert.equal(Node.focused, byId('image-subject'));
byId('image-subject').value = 'Moon festival'; byId('image-subject').dispatch('input');
byId('image-prompt').value = 'Draw a large moon and small observatory.'; byId('image-prompt').dispatch('input');
byId('image-background').value = 'Transparent'; byId('image-background').dispatch('change');
assert.equal(editor.validate(), true);
let prompt = editor.compose(poster, 'No invented date.');
assert.match(prompt, /Moon festival/);
assert.match(prompt, /Draw a large moon/);
assert.match(prompt, /transparent_background=true/);
assert.match(prompt, /No invented date/);
assert.ok(changes >= 3);
editor.mount({item:portrait, host, onChange:() => changes++});
assert.equal(byId('image-subject').value, '');
assert.match(editor.compose(portrait, ''), /If missing, ask the user to attach it and stop/);
editor.mount({item:poster, host, onChange:() => changes++});
assert.equal(byId('image-subject').value, 'Moon festival');
assert.equal(byId('image-prompt').value, 'Draw a large moon and small observatory.');
assert.equal(byId('image-background').value, 'Transparent');
assert.equal(editor.validate(), true);
assert.throws(() => editor.compose(poster, 'x'.repeat(2001)), /too long/);
console.log('Editor DOM harness: required subject, editable prompt, reference guard, per-item draft, ratio/background and bounds OK');
