/*! For license information please see custom-panel.ce0590c0.js.LICENSE.txt */
(()=>{var e,t,r={87466:(e,t,r)=>{"use strict";r.d(t,{Mo:()=>o,Cb:()=>i,sz:()=>a,IO:()=>s,GC:()=>l,hO:()=>p});const o=e=>t=>"function"==typeof t?((e,t)=>(window.customElements.define(e,t),t))(e,t):((e,t)=>{const{kind:r,elements:o}=t;return{kind:r,elements:o,finisher(t){window.customElements.define(e,t)}}})(e,t),n=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?Object.assign(Object.assign({},t),{finisher(r){r.createProperty(t.key,e)}}):{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(r){r.createProperty(t.key,e)}};function i(e){return(t,r)=>void 0!==r?((e,t,r)=>{t.constructor.createProperty(r,e)})(e,t,r):n(e,t)}function a(e){return i({attribute:!1,hasChanged:null==e?void 0:e.hasChanged})}function s(e,t){return(r,o)=>{const n={get(){return this.renderRoot.querySelector(e)},enumerable:!0,configurable:!0};if(t){const t="symbol"==typeof o?Symbol():`__${o}`;n.get=function(){return void 0===this[t]&&(this[t]=this.renderRoot.querySelector(e)),this[t]}}return void 0!==o?c(n,r,o):d(n,r)}}function l(e){return(t,r)=>{const o={async get(){return await this.updateComplete,this.renderRoot.querySelector(e)},enumerable:!0,configurable:!0};return void 0!==r?c(o,t,r):d(o,t)}}const c=(e,t,r)=>{Object.defineProperty(t,r,e)},d=(e,t)=>({kind:"method",placement:"prototype",key:t.key,descriptor:e});function p(e){return(t,r)=>void 0!==r?((e,t,r)=>{Object.assign(t[r],e)})(e,t,r):((e,t)=>Object.assign(Object.assign({},t),{finisher(r){Object.assign(r.prototype[t.key],e)}}))(e,t)}const h=Element.prototype;h.msMatchesSelector||h.webkitMatchesSelector},15652:(e,t,r)=>{"use strict";r.d(t,{oi:()=>A,iv:()=>E,Mo:()=>S.Mo,hO:()=>S.hO,dy:()=>p.dy,sz:()=>S.sz,Cb:()=>S.Cb,IO:()=>S.IO,GC:()=>S.GC,YP:()=>p.YP});var o=r(50115),n=r(27283);function i(e,t){const{element:{content:r},parts:o}=e,n=document.createTreeWalker(r,133,null,!1);let i=s(o),a=o[i],l=-1,c=0;const d=[];let p=null;for(;n.nextNode();){l++;const e=n.currentNode;for(e.previousSibling===p&&(p=null),t.has(e)&&(d.push(e),null===p&&(p=e)),null!==p&&c++;void 0!==a&&a.index===l;)a.index=null!==p?-1:a.index-c,i=s(o,i),a=o[i]}d.forEach((e=>e.parentNode.removeChild(e)))}const a=e=>{let t=11===e.nodeType?0:1;const r=document.createTreeWalker(e,133,null,!1);for(;r.nextNode();)t++;return t},s=(e,t=-1)=>{for(let r=t+1;r<e.length;r++){const t=e[r];if((0,n.pC)(t))return r}return-1};var l=r(84677),c=r(92530),d=r(37581),p=r(94707);const h=(e,t)=>`${e}--${t}`;let u=!0;void 0===window.ShadyCSS?u=!1:void 0===window.ShadyCSS.prepareTemplateDom&&(console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."),u=!1);const m=e=>t=>{const r=h(t.type,e);let o=c.r.get(r);void 0===o&&(o={stringsArray:new WeakMap,keyString:new Map},c.r.set(r,o));let i=o.stringsArray.get(t.strings);if(void 0!==i)return i;const a=t.strings.join(n.Jw);if(i=o.keyString.get(a),void 0===i){const r=t.getTemplateElement();u&&window.ShadyCSS.prepareTemplateDom(r,e),i=new n.YS(t,r),o.keyString.set(a,i)}return o.stringsArray.set(t.strings,i),i},f=["html","svg"],g=new Set,v=(e,t,r)=>{g.add(e);const o=r?r.element:document.createElement("template"),n=t.querySelectorAll("style"),{length:l}=n;if(0===l)return void window.ShadyCSS.prepareTemplateStyles(o,e);const d=document.createElement("style");for(let e=0;e<l;e++){const t=n[e];t.parentNode.removeChild(t),d.textContent+=t.textContent}(e=>{f.forEach((t=>{const r=c.r.get(h(t,e));void 0!==r&&r.keyString.forEach((e=>{const{element:{content:t}}=e,r=new Set;Array.from(t.querySelectorAll("style")).forEach((e=>{r.add(e)})),i(e,r)}))}))})(e);const p=o.content;r?function(e,t,r=null){const{element:{content:o},parts:n}=e;if(null==r)return void o.appendChild(t);const i=document.createTreeWalker(o,133,null,!1);let l=s(n),c=0,d=-1;for(;i.nextNode();)for(d++,i.currentNode===r&&(c=a(t),r.parentNode.insertBefore(t,r));-1!==l&&n[l].index===d;){if(c>0){for(;-1!==l;)n[l].index+=c,l=s(n,l);return}l=s(n,l)}}(r,d,p.firstChild):p.insertBefore(d,p.firstChild),window.ShadyCSS.prepareTemplateStyles(o,e);const u=p.querySelector("style");if(window.ShadyCSS.nativeShadow&&null!==u)t.insertBefore(u.cloneNode(!0),t.firstChild);else if(r){p.insertBefore(d,p.firstChild);const e=new Set;e.add(d),i(r,e)}};window.JSCompiler_renameProperty=(e,t)=>e;const y={toAttribute(e,t){switch(t){case Boolean:return e?"":null;case Object:case Array:return null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){switch(t){case Boolean:return null!==e;case Number:return null===e?null:Number(e);case Object:case Array:return JSON.parse(e)}return e}},b=(e,t)=>t!==e&&(t==t||e==e),_={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:b},w="finalized";class x extends HTMLElement{constructor(){super(),this.initialize()}static get observedAttributes(){this.finalize();const e=[];return this._classProperties.forEach(((t,r)=>{const o=this._attributeNameForProperty(r,t);void 0!==o&&(this._attributeToPropertyMap.set(o,r),e.push(o))})),e}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const e=Object.getPrototypeOf(this)._classProperties;void 0!==e&&e.forEach(((e,t)=>this._classProperties.set(t,e)))}}static createProperty(e,t=_){if(this._ensureClassProperties(),this._classProperties.set(e,t),t.noAccessor||this.prototype.hasOwnProperty(e))return;const r="symbol"==typeof e?Symbol():`__${e}`,o=this.getPropertyDescriptor(e,r,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}static getPropertyDescriptor(e,t,r){return{get(){return this[t]},set(o){const n=this[e];this[t]=o,this.requestUpdateInternal(e,n,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this._classProperties&&this._classProperties.get(e)||_}static finalize(){const e=Object.getPrototypeOf(this);if(e.hasOwnProperty(w)||e.finalize(),this.finalized=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const e=this.properties,t=[...Object.getOwnPropertyNames(e),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(e):[]];for(const r of t)this.createProperty(r,e[r])}}static _attributeNameForProperty(e,t){const r=t.attribute;return!1===r?void 0:"string"==typeof r?r:"string"==typeof e?e.toLowerCase():void 0}static _valueHasChanged(e,t,r=b){return r(e,t)}static _propertyValueFromAttribute(e,t){const r=t.type,o=t.converter||y,n="function"==typeof o?o:o.fromAttribute;return n?n(e,r):e}static _propertyValueToAttribute(e,t){if(void 0===t.reflect)return;const r=t.type,o=t.converter;return(o&&o.toAttribute||y.toAttribute)(e,r)}initialize(){this._updateState=0,this._updatePromise=new Promise((e=>this._enableUpdatingResolver=e)),this._changedProperties=new Map,this._saveInstanceProperties(),this.requestUpdateInternal()}_saveInstanceProperties(){this.constructor._classProperties.forEach(((e,t)=>{if(this.hasOwnProperty(t)){const e=this[t];delete this[t],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(t,e)}}))}_applyInstanceProperties(){this._instanceProperties.forEach(((e,t)=>this[t]=e)),this._instanceProperties=void 0}connectedCallback(){this.enableUpdating()}enableUpdating(){void 0!==this._enableUpdatingResolver&&(this._enableUpdatingResolver(),this._enableUpdatingResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(e,t,r){t!==r&&this._attributeToProperty(e,r)}_propertyToAttribute(e,t,r=_){const o=this.constructor,n=o._attributeNameForProperty(e,r);if(void 0!==n){const e=o._propertyValueToAttribute(t,r);if(void 0===e)return;this._updateState=8|this._updateState,null==e?this.removeAttribute(n):this.setAttribute(n,e),this._updateState=-9&this._updateState}}_attributeToProperty(e,t){if(8&this._updateState)return;const r=this.constructor,o=r._attributeToPropertyMap.get(e);if(void 0!==o){const e=r.getPropertyOptions(o);this._updateState=16|this._updateState,this[o]=r._propertyValueFromAttribute(t,e),this._updateState=-17&this._updateState}}requestUpdateInternal(e,t,r){let o=!0;if(void 0!==e){const n=this.constructor;r=r||n.getPropertyOptions(e),n._valueHasChanged(this[e],t,r.hasChanged)?(this._changedProperties.has(e)||this._changedProperties.set(e,t),!0!==r.reflect||16&this._updateState||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(e,r))):o=!1}!this._hasRequestedUpdate&&o&&(this._updatePromise=this._enqueueUpdate())}requestUpdate(e,t){return this.requestUpdateInternal(e,t),this.updateComplete}async _enqueueUpdate(){this._updateState=4|this._updateState;try{await this._updatePromise}catch(e){}const e=this.performUpdate();return null!=e&&await e,!this._hasRequestedUpdate}get _hasRequestedUpdate(){return 4&this._updateState}get hasUpdated(){return 1&this._updateState}performUpdate(){if(!this._hasRequestedUpdate)return;this._instanceProperties&&this._applyInstanceProperties();let e=!1;const t=this._changedProperties;try{e=this.shouldUpdate(t),e?this.update(t):this._markUpdated()}catch(t){throw e=!1,this._markUpdated(),t}e&&(1&this._updateState||(this._updateState=1|this._updateState,this.firstUpdated(t)),this.updated(t))}_markUpdated(){this._changedProperties=new Map,this._updateState=-5&this._updateState}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(e){return!0}update(e){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach(((e,t)=>this._propertyToAttribute(t,this[t],e))),this._reflectingProperties=void 0),this._markUpdated()}updated(e){}firstUpdated(e){}}x.finalized=!0;var S=r(87466);const k=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,C=Symbol();class P{constructor(e,t){if(t!==C)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return void 0===this._styleSheet&&(k?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}const E=(e,...t)=>{const r=t.reduce(((t,r,o)=>t+(e=>{if(e instanceof P)return e.cssText;if("number"==typeof e)return e;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${e}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(r)+e[o+1]),e[0]);return new P(r,C)};(window.litElementVersions||(window.litElementVersions=[])).push("2.4.0");const N={};class A extends x{static getStyles(){return this.styles}static _getUniqueStyles(){if(this.hasOwnProperty(JSCompiler_renameProperty("_styles",this)))return;const e=this.getStyles();if(Array.isArray(e)){const t=(e,r)=>e.reduceRight(((e,r)=>Array.isArray(r)?t(r,e):(e.add(r),e)),r),r=t(e,new Set),o=[];r.forEach((e=>o.unshift(e))),this._styles=o}else this._styles=void 0===e?[]:[e];this._styles=this._styles.map((e=>{if(e instanceof CSSStyleSheet&&!k){const t=Array.prototype.slice.call(e.cssRules).reduce(((e,t)=>e+t.cssText),"");return new P(String(t),C)}return e}))}initialize(){super.initialize(),this.constructor._getUniqueStyles(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const e=this.constructor._styles;0!==e.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?k?this.renderRoot.adoptedStyleSheets=e.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(e.map((e=>e.cssText)),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(e){const t=this.render();super.update(e),t!==N&&this.constructor.render(t,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach((e=>{const t=document.createElement("style");t.textContent=e.cssText,this.renderRoot.appendChild(t)})))}render(){return N}}A.finalized=!0,A.render=(e,t,r)=>{if(!r||"object"!=typeof r||!r.scopeName)throw new Error("The `scopeName` option is required.");const n=r.scopeName,i=l.L.has(t),a=u&&11===t.nodeType&&!!t.host,s=a&&!g.has(n),c=s?document.createDocumentFragment():t;if((0,l.s)(e,c,Object.assign({templateFactory:m(n)},r)),s){const e=l.L.get(c);l.L.delete(c);const r=e.value instanceof d.R?e.value.template:void 0;v(n,c,r),(0,o.r4)(t,t.firstChild),t.appendChild(c),l.L.set(t,e)}!i&&a&&window.ShadyCSS.styleElement(t.host)}},76747:(e,t,r)=>{"use strict";r.d(t,{X:()=>n,w:()=>i});const o=new WeakMap,n=e=>(...t)=>{const r=e(...t);return o.set(r,!0),r},i=e=>"function"==typeof e&&o.has(e)},50115:(e,t,r)=>{"use strict";r.d(t,{eC:()=>o,V:()=>n,r4:()=>i});const o="undefined"!=typeof window&&null!=window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,n=(e,t,r=null,o=null)=>{for(;t!==r;){const r=t.nextSibling;e.insertBefore(t,o),t=r}},i=(e,t,r=null)=>{for(;t!==r;){const r=t.nextSibling;e.removeChild(t),t=r}}},43401:(e,t,r)=>{"use strict";r.d(t,{J:()=>o,L:()=>n});const o={},n={}},28823:(e,t,r)=>{"use strict";r.d(t,{QG:()=>p,_l:()=>h,nt:()=>u,JG:()=>m,m:()=>f,sL:()=>g,K1:()=>y});var o=r(76747),n=r(50115),i=r(43401),a=r(37581),s=r(87842),l=r(27283);const c=e=>null===e||!("object"==typeof e||"function"==typeof e),d=e=>Array.isArray(e)||!(!e||!e[Symbol.iterator]);class p{constructor(e,t,r){this.dirty=!0,this.element=e,this.name=t,this.strings=r,this.parts=[];for(let e=0;e<r.length-1;e++)this.parts[e]=this._createPart()}_createPart(){return new h(this)}_getValue(){const e=this.strings,t=e.length-1,r=this.parts;if(1===t&&""===e[0]&&""===e[1]){const e=r[0].value;if("symbol"==typeof e)return String(e);if("string"==typeof e||!d(e))return e}let o="";for(let n=0;n<t;n++){o+=e[n];const t=r[n];if(void 0!==t){const e=t.value;if(c(e)||!d(e))o+="string"==typeof e?e:String(e);else for(const t of e)o+="string"==typeof t?t:String(t)}}return o+=e[t],o}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class h{constructor(e){this.value=void 0,this.committer=e}setValue(e){e===i.J||c(e)&&e===this.value||(this.value=e,(0,o.w)(e)||(this.committer.dirty=!0))}commit(){for(;(0,o.w)(this.value);){const e=this.value;this.value=i.J,e(this)}this.value!==i.J&&this.committer.commit()}}class u{constructor(e){this.value=void 0,this.__pendingValue=void 0,this.options=e}appendInto(e){this.startNode=e.appendChild((0,l.IW)()),this.endNode=e.appendChild((0,l.IW)())}insertAfterNode(e){this.startNode=e,this.endNode=e.nextSibling}appendIntoPart(e){e.__insert(this.startNode=(0,l.IW)()),e.__insert(this.endNode=(0,l.IW)())}insertAfterPart(e){e.__insert(this.startNode=(0,l.IW)()),this.endNode=e.endNode,e.endNode=this.startNode}setValue(e){this.__pendingValue=e}commit(){if(null===this.startNode.parentNode)return;for(;(0,o.w)(this.__pendingValue);){const e=this.__pendingValue;this.__pendingValue=i.J,e(this)}const e=this.__pendingValue;e!==i.J&&(c(e)?e!==this.value&&this.__commitText(e):e instanceof s.j?this.__commitTemplateResult(e):e instanceof Node?this.__commitNode(e):d(e)?this.__commitIterable(e):e===i.L?(this.value=i.L,this.clear()):this.__commitText(e))}__insert(e){this.endNode.parentNode.insertBefore(e,this.endNode)}__commitNode(e){this.value!==e&&(this.clear(),this.__insert(e),this.value=e)}__commitText(e){const t=this.startNode.nextSibling,r="string"==typeof(e=null==e?"":e)?e:String(e);t===this.endNode.previousSibling&&3===t.nodeType?t.data=r:this.__commitNode(document.createTextNode(r)),this.value=e}__commitTemplateResult(e){const t=this.options.templateFactory(e);if(this.value instanceof a.R&&this.value.template===t)this.value.update(e.values);else{const r=new a.R(t,e.processor,this.options),o=r._clone();r.update(e.values),this.__commitNode(o),this.value=r}}__commitIterable(e){Array.isArray(this.value)||(this.value=[],this.clear());const t=this.value;let r,o=0;for(const n of e)r=t[o],void 0===r&&(r=new u(this.options),t.push(r),0===o?r.appendIntoPart(this):r.insertAfterPart(t[o-1])),r.setValue(n),r.commit(),o++;o<t.length&&(t.length=o,this.clear(r&&r.endNode))}clear(e=this.startNode){(0,n.r4)(this.startNode.parentNode,e.nextSibling,this.endNode)}}class m{constructor(e,t,r){if(this.value=void 0,this.__pendingValue=void 0,2!==r.length||""!==r[0]||""!==r[1])throw new Error("Boolean attributes can only contain a single expression");this.element=e,this.name=t,this.strings=r}setValue(e){this.__pendingValue=e}commit(){for(;(0,o.w)(this.__pendingValue);){const e=this.__pendingValue;this.__pendingValue=i.J,e(this)}if(this.__pendingValue===i.J)return;const e=!!this.__pendingValue;this.value!==e&&(e?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name),this.value=e),this.__pendingValue=i.J}}class f extends p{constructor(e,t,r){super(e,t,r),this.single=2===r.length&&""===r[0]&&""===r[1]}_createPart(){return new g(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class g extends h{}let v=!1;(()=>{try{const e={get capture(){return v=!0,!1}};window.addEventListener("test",e,e),window.removeEventListener("test",e,e)}catch(e){}})();class y{constructor(e,t,r){this.value=void 0,this.__pendingValue=void 0,this.element=e,this.eventName=t,this.eventContext=r,this.__boundHandleEvent=e=>this.handleEvent(e)}setValue(e){this.__pendingValue=e}commit(){for(;(0,o.w)(this.__pendingValue);){const e=this.__pendingValue;this.__pendingValue=i.J,e(this)}if(this.__pendingValue===i.J)return;const e=this.__pendingValue,t=this.value,r=null==e||null!=t&&(e.capture!==t.capture||e.once!==t.once||e.passive!==t.passive),n=null!=e&&(null==t||r);r&&this.element.removeEventListener(this.eventName,this.__boundHandleEvent,this.__options),n&&(this.__options=b(e),this.element.addEventListener(this.eventName,this.__boundHandleEvent,this.__options)),this.value=e,this.__pendingValue=i.J}handleEvent(e){"function"==typeof this.value?this.value.call(this.eventContext||this.element,e):this.value.handleEvent(e)}}const b=e=>e&&(v?{capture:e.capture,passive:e.passive,once:e.once}:e.capture)},84677:(e,t,r)=>{"use strict";r.d(t,{L:()=>a,s:()=>s});var o=r(50115),n=r(28823),i=r(92530);const a=new WeakMap,s=(e,t,r)=>{let s=a.get(t);void 0===s&&((0,o.r4)(t,t.firstChild),a.set(t,s=new n.nt(Object.assign({templateFactory:i.t},r))),s.appendInto(t)),s.setValue(e),s.commit()}},92530:(e,t,r)=>{"use strict";r.d(t,{t:()=>n,r:()=>i});var o=r(27283);function n(e){let t=i.get(e.type);void 0===t&&(t={stringsArray:new WeakMap,keyString:new Map},i.set(e.type,t));let r=t.stringsArray.get(e.strings);if(void 0!==r)return r;const n=e.strings.join(o.Jw);return r=t.keyString.get(n),void 0===r&&(r=new o.YS(e,e.getTemplateElement()),t.keyString.set(n,r)),t.stringsArray.set(e.strings,r),r}const i=new Map},37581:(e,t,r)=>{"use strict";r.d(t,{R:()=>i});var o=r(50115),n=r(27283);class i{constructor(e,t,r){this.__parts=[],this.template=e,this.processor=t,this.options=r}update(e){let t=0;for(const r of this.__parts)void 0!==r&&r.setValue(e[t]),t++;for(const e of this.__parts)void 0!==e&&e.commit()}_clone(){const e=o.eC?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),t=[],r=this.template.parts,i=document.createTreeWalker(e,133,null,!1);let a,s=0,l=0,c=i.nextNode();for(;s<r.length;)if(a=r[s],(0,n.pC)(a)){for(;l<a.index;)l++,"TEMPLATE"===c.nodeName&&(t.push(c),i.currentNode=c.content),null===(c=i.nextNode())&&(i.currentNode=t.pop(),c=i.nextNode());if("node"===a.type){const e=this.processor.handleTextExpression(this.options);e.insertAfterNode(c.previousSibling),this.__parts.push(e)}else this.__parts.push(...this.processor.handleAttributeExpressions(c,a.name,a.strings,this.options));s++}else this.__parts.push(void 0),s++;return o.eC&&(document.adoptNode(e),customElements.upgrade(e)),e}}},87842:(e,t,r)=>{"use strict";r.d(t,{j:()=>s,C:()=>l});var o=r(50115),n=r(27283);const i=window.trustedTypes&&trustedTypes.createPolicy("lit-html",{createHTML:e=>e}),a=` ${n.Jw} `;class s{constructor(e,t,r,o){this.strings=e,this.values=t,this.type=r,this.processor=o}getHTML(){const e=this.strings.length-1;let t="",r=!1;for(let o=0;o<e;o++){const e=this.strings[o],i=e.lastIndexOf("\x3c!--");r=(i>-1||r)&&-1===e.indexOf("--\x3e",i+1);const s=n.W5.exec(e);t+=null===s?e+(r?a:n.N):e.substr(0,s.index)+s[1]+s[2]+n.$E+s[3]+n.Jw}return t+=this.strings[e],t}getTemplateElement(){const e=document.createElement("template");let t=this.getHTML();return void 0!==i&&(t=i.createHTML(t)),e.innerHTML=t,e}}class l extends s{getHTML(){return`<svg>${super.getHTML()}</svg>`}getTemplateElement(){const e=super.getTemplateElement(),t=e.content,r=t.firstChild;return t.removeChild(r),(0,o.V)(t,r.firstChild),e}}},27283:(e,t,r)=>{"use strict";r.d(t,{Jw:()=>o,N:()=>n,$E:()=>a,YS:()=>s,pC:()=>c,IW:()=>d,W5:()=>p});const o=`{{lit-${String(Math.random()).slice(2)}}}`,n=`\x3c!--${o}--\x3e`,i=new RegExp(`${o}|${n}`),a="$lit$";class s{constructor(e,t){this.parts=[],this.element=t;const r=[],n=[],s=document.createTreeWalker(t.content,133,null,!1);let c=0,h=-1,u=0;const{strings:m,values:{length:f}}=e;for(;u<f;){const e=s.nextNode();if(null!==e){if(h++,1===e.nodeType){if(e.hasAttributes()){const t=e.attributes,{length:r}=t;let o=0;for(let e=0;e<r;e++)l(t[e].name,a)&&o++;for(;o-- >0;){const t=m[u],r=p.exec(t)[2],o=r.toLowerCase()+a,n=e.getAttribute(o);e.removeAttribute(o);const s=n.split(i);this.parts.push({type:"attribute",index:h,name:r,strings:s}),u+=s.length-1}}"TEMPLATE"===e.tagName&&(n.push(e),s.currentNode=e.content)}else if(3===e.nodeType){const t=e.data;if(t.indexOf(o)>=0){const o=e.parentNode,n=t.split(i),s=n.length-1;for(let t=0;t<s;t++){let r,i=n[t];if(""===i)r=d();else{const e=p.exec(i);null!==e&&l(e[2],a)&&(i=i.slice(0,e.index)+e[1]+e[2].slice(0,-a.length)+e[3]),r=document.createTextNode(i)}o.insertBefore(r,e),this.parts.push({type:"node",index:++h})}""===n[s]?(o.insertBefore(d(),e),r.push(e)):e.data=n[s],u+=s}}else if(8===e.nodeType)if(e.data===o){const t=e.parentNode;null!==e.previousSibling&&h!==c||(h++,t.insertBefore(d(),e)),c=h,this.parts.push({type:"node",index:h}),null===e.nextSibling?e.data="":(r.push(e),h--),u++}else{let t=-1;for(;-1!==(t=e.data.indexOf(o,t+1));)this.parts.push({type:"node",index:-1}),u++}}else s.currentNode=n.pop()}for(const e of r)e.parentNode.removeChild(e)}}const l=(e,t)=>{const r=e.length-t.length;return r>=0&&e.slice(r)===t},c=e=>-1!==e.index,d=()=>document.createComment(""),p=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/},94707:(e,t,r)=>{"use strict";r.d(t,{_l:()=>o._l,sL:()=>o.sL,XM:()=>a.X,dy:()=>s,YP:()=>l});var o=r(28823);const n=new class{handleAttributeExpressions(e,t,r,n){const i=t[0];if("."===i){return new o.m(e,t.slice(1),r).parts}if("@"===i)return[new o.K1(e,t.slice(1),n.eventContext)];if("?"===i)return[new o.JG(e,t.slice(1),r)];return new o.QG(e,t,r).parts}handleTextExpression(e){return new o.nt(e)}};var i=r(87842),a=r(76747);r(50115),r(43401),r(84677),r(92530),r(37581),r(27283);"undefined"!=typeof window&&(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.3.0");const s=(e,...t)=>new i.j(e,t,"html",n),l=(e,...t)=>new i.C(e,t,"svg",n)},47181:(e,t,r)=>{"use strict";r.d(t,{B:()=>o});const o=(e,t,r,o)=>{o=o||{},r=null==r?{}:r;const n=new Event(t,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return n.detail=r,e.dispatchEvent(n),n}},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},11654:(e,t,r)=>{"use strict";r.d(t,{_l:()=>n,q0:()=>i,Qx:()=>s,e$:()=>l});var o=r(15652);const n={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B"},i={"error-state-color":"var(--error-color)","state-icon-unavailable-color":"var(--disabled-text-color)","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-bar-color":"var(--disabled-text-color)","label-badge-grey":"var(--paper-grey-500)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-bar-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)"},a=o.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,s=o.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${a}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,l=(o.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,o.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`,o.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`)}},o={};function n(e){if(o[e])return o[e].exports;var t=o[e]={exports:{}};return r[e](t,t.exports,n),t.exports}n.m=r,n.d=(e,t)=>{for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},n.f={},n.e=e=>Promise.all(Object.keys(n.f).reduce(((t,r)=>(n.f[r](e,t),t)),[])),n.u=e=>"chunk."+{613:"127fda46df363236e6e4",1479:"25bf1069f7b4dcacd602",1672:"c010d4b9431ab6840991",2678:"0c5ca4645f825bbfac39",2983:"fa93755451f3f3ed20fa",6134:"47c6b8ff1317c44118de",9286:"6641b6a171a28a2c7062"}[e]+".js",n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",n.l=(r,o,i,a)=>{if(e[r])e[r].push(o);else{var s,l;if(void 0!==i)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var p=c[d];if(p.getAttribute("src")==r||p.getAttribute("data-webpack")==t+i){s=p;break}}s||(l=!0,(s=document.createElement("script")).charset="utf-8",s.timeout=120,n.nc&&s.setAttribute("nonce",n.nc),s.setAttribute("data-webpack",t+i),s.src=r),e[r]=[o];var h=(t,o)=>{s.onerror=s.onload=null,clearTimeout(u);var n=e[r];if(delete e[r],s.parentNode&&s.parentNode.removeChild(s),n&&n.forEach((e=>e(o))),t)return t(o)},u=setTimeout(h.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=h.bind(null,s.onerror),s.onload=h.bind(null,s.onload),l&&document.head.appendChild(s)}},n.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.p="/frontend_latest/",(()=>{var e={8017:0};n.f.j=(t,r)=>{var o=n.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var i=new Promise(((r,n)=>{o=e[t]=[r,n]}));r.push(o[2]=i);var a=n.p+n.u(t),s=new Error;n.l(a,(r=>{if(n.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var i=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\n("+i+": "+a+")",s.name="ChunkLoadError",s.type=i,s.request=a,o[1](s)}}),"chunk-"+t,t)}};var t=(t,r)=>{for(var o,i,[a,s,l]=r,c=0,d=[];c<a.length;c++)i=a[c],n.o(e,i)&&e[i]&&d.push(e[i][0]),e[i]=0;for(o in s)n.o(s,o)&&(n.m[o]=s[o]);for(l&&l(n),t&&t(r);d.length;)d.shift()()},r=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})(),(()=>{"use strict";var e=n(47181);const t=(e,t,r)=>new Promise(((o,n)=>{const i=document.createElement(e);let a="src",s="body";switch(i.onload=()=>o(t),i.onerror=()=>n(t),e){case"script":i.async=!0,r&&(i.type=r);break;case"link":i.type="text/css",i.rel="stylesheet",a="href",s="head"}i[a]=t,document[s].appendChild(i)})),r=e=>t("script",e),o="customElements"in window&&"content"in document.createElement("template");n(37846);const i={},a=e=>{const o=(e=>e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url||e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url})(e);return"js"===o.type?(o.url in i||(i[o.url]=r(o.url)),i[o.url]):"module"===o.type?(n=o.url,t("script",n,"module")):Promise.reject("No valid url found in panel config.");var n};var s=n(11654);let l,c;function d(e){c&&((e,t)=>{"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((r=>{e[r]=t[r]}))})(c,e)}function p(t,i){const p=document.createElement("style");p.innerHTML="body{margin:0}",document.head.appendChild(p);const h=t.config._panel_custom;let u=Promise.resolve();o||(u=u.then((()=>r("/static/polyfills/webcomponents-bundle.js")))),u.then((()=>a(h))).then((()=>l||Promise.resolve())).then((()=>{c=(e=>{const t="html_url"in e?`ha-panel-${e.name}`:e.name;return document.createElement(t)})(h);c.addEventListener("hass-toggle-menu",(t=>{window.parent.customPanel&&(0,e.B)(window.parent.customPanel,t.type,t.detail)})),window.addEventListener("location-changed",(e=>{window.parent.customPanel&&window.parent.customPanel.navigate(window.location.pathname,!!e.detail&&e.detail.replace)})),d({panel:t,...i}),document.body.appendChild(c)}),(e=>{let r;console.error(e,t),"hassio"===t.url_path?(Promise.all([n.e(1672),n.e(613),n.e(2983),n.e(1479),n.e(6134),n.e(2678)]).then(n.bind(n,82678)),r=document.createElement("supervisor-error-screen")):(Promise.all([n.e(613),n.e(2983),n.e(6134),n.e(9286)]).then(n.bind(n,48811)),r=document.createElement("hass-error-screen"),r.error=`Unable to load the panel source: ${e}.`);const o=document.createElement("style");o.innerHTML=s.e$.cssText,document.body.appendChild(o),r.hass=i.hass,document.body.appendChild(r)}))}window.loadES5Adapter=()=>(l||(l=r("/static/polyfills/custom-elements-es5-adapter.js").catch()),l),document.addEventListener("DOMContentLoaded",(()=>window.parent.customPanel.registerIframe(p,d)),{once:!0})})()})();
//# sourceMappingURL=custom-panel.ce0590c0.js.map