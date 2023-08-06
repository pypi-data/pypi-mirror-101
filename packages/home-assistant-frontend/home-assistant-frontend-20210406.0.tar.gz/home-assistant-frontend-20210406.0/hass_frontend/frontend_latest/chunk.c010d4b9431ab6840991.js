/*! For license information please see chunk.c010d4b9431ab6840991.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1672],{72774:(t,e,s)=>{"use strict";s.d(e,{K:()=>i});var i=function(){function t(t){void 0===t&&(t={}),this.adapter=t}return Object.defineProperty(t,"cssClasses",{get:function(){return{}},enumerable:!0,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return{}},enumerable:!0,configurable:!0}),Object.defineProperty(t,"numbers",{get:function(){return{}},enumerable:!0,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{}},enumerable:!0,configurable:!0}),t.prototype.init=function(){},t.prototype.destroy=function(){},t}()},65660:(t,e,s)=>{"use strict";s(65233);const i=s(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content);var n=document.createElement("style");n.textContent="[hidden] { display: none !important; }",document.head.appendChild(n)},54242:(t,e,s)=>{"use strict";s(65233);const i=s(50856).d`
<custom-style>
  <style is="custom-style">
    html {

      --shadow-transition: {
        transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
      };

      --shadow-none: {
        box-shadow: none;
      };

      /* from http://codepen.io/shyndman/pen/c5394ddf2e8b2a5c9185904b57421cdb */

      --shadow-elevation-2dp: {
        box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),
                    0 1px 5px 0 rgba(0, 0, 0, 0.12),
                    0 3px 1px -2px rgba(0, 0, 0, 0.2);
      };

      --shadow-elevation-3dp: {
        box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.14),
                    0 1px 8px 0 rgba(0, 0, 0, 0.12),
                    0 3px 3px -2px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-4dp: {
        box-shadow: 0 4px 5px 0 rgba(0, 0, 0, 0.14),
                    0 1px 10px 0 rgba(0, 0, 0, 0.12),
                    0 2px 4px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-6dp: {
        box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14),
                    0 1px 18px 0 rgba(0, 0, 0, 0.12),
                    0 3px 5px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-8dp: {
        box-shadow: 0 8px 10px 1px rgba(0, 0, 0, 0.14),
                    0 3px 14px 2px rgba(0, 0, 0, 0.12),
                    0 5px 5px -3px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-12dp: {
        box-shadow: 0 12px 16px 1px rgba(0, 0, 0, 0.14),
                    0 4px 22px 3px rgba(0, 0, 0, 0.12),
                    0 6px 7px -4px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-16dp: {
        box-shadow: 0 16px 24px 2px rgba(0, 0, 0, 0.14),
                    0  6px 30px 5px rgba(0, 0, 0, 0.12),
                    0  8px 10px -5px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-24dp: {
        box-shadow: 0 24px 38px 3px rgba(0, 0, 0, 0.14),
                    0 9px 46px 8px rgba(0, 0, 0, 0.12),
                    0 11px 15px -7px rgba(0, 0, 0, 0.4);
      };
    }
  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},70019:(t,e,s)=>{"use strict";s(65233);const i=s(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},37961:(t,e,s)=>{"use strict";var i=s(28426),n=s(76389),r=s(4507),o=s(36608);let a=(0,n.o)((t=>{let e=(0,o.SH)(t);return class extends e{static get properties(){return{items:{type:Array},multi:{type:Boolean,value:!1},selected:{type:Object,notify:!0},selectedItem:{type:Object,notify:!0},toggle:{type:Boolean,value:!1}}}static get observers(){return["__updateSelection(multi, items.*)"]}constructor(){super(),this.__lastItems=null,this.__lastMulti=null,this.__selectedMap=null}__updateSelection(t,e){let s=e.path;if("items"==s){let s=e.base||[],i=this.__lastItems;if(t!==this.__lastMulti&&this.clearSelection(),i){let t=(0,r.c)(s,i);this.__applySplices(t)}this.__lastItems=s,this.__lastMulti=t}else if("items.splices"==e.path)this.__applySplices(e.value.indexSplices);else{let t=s.slice("items.".length),e=parseInt(t,10);t.indexOf(".")<0&&t==e&&this.__deselectChangedIdx(e)}}__applySplices(t){let e=this.__selectedMap;for(let s=0;s<t.length;s++){let i=t[s];e.forEach(((t,s)=>{t<i.index||(t>=i.index+i.removed.length?e.set(s,t+i.addedCount-i.removed.length):e.set(s,-1))}));for(let t=0;t<i.addedCount;t++){let s=i.index+t;e.has(this.items[s])&&e.set(this.items[s],s)}}this.__updateLinks();let s=0;e.forEach(((t,i)=>{t<0?(this.multi?this.splice("selected",s,1):this.selected=this.selectedItem=null,e.delete(i)):s++}))}__updateLinks(){if(this.__dataLinkedPaths={},this.multi){let t=0;this.__selectedMap.forEach((e=>{e>=0&&this.linkPaths("items."+e,"selected."+t++)}))}else this.__selectedMap.forEach((t=>{this.linkPaths("selected","items."+t),this.linkPaths("selectedItem","items."+t)}))}clearSelection(){this.__dataLinkedPaths={},this.__selectedMap=new Map,this.selected=this.multi?[]:null,this.selectedItem=null}isSelected(t){return this.__selectedMap.has(t)}isIndexSelected(t){return this.isSelected(this.items[t])}__deselectChangedIdx(t){let e=this.__selectedIndexForItemIndex(t);if(e>=0){let t=0;this.__selectedMap.forEach(((s,i)=>{e==t++&&this.deselect(i)}))}}__selectedIndexForItemIndex(t){let e=this.__dataLinkedPaths["items."+t];if(e)return parseInt(e.slice("selected.".length),10)}deselect(t){let e=this.__selectedMap.get(t);if(e>=0){let s;this.__selectedMap.delete(t),this.multi&&(s=this.__selectedIndexForItemIndex(e)),this.__updateLinks(),this.multi?this.splice("selected",s,1):this.selected=this.selectedItem=null}}deselectIndex(t){this.deselect(this.items[t])}select(t){this.selectIndex(this.items.indexOf(t))}selectIndex(t){let e=this.items[t];this.isSelected(e)?this.toggle&&this.deselectIndex(t):(this.multi||this.__selectedMap.clear(),this.__selectedMap.set(e,t),this.__updateLinks(),this.multi?this.push("selected",e):this.selected=this.selectedItem=e)}}}))(i.H3);class l extends a{static get is(){return"array-selector"}}customElements.define(l.is,l)},5618:(t,e,s)=>{"use strict";var i=s(34816),n=s(10868),r=s(26539);const o=new i.ZP;window.ShadyCSS||(window.ShadyCSS={prepareTemplate(t,e,s){},prepareTemplateDom(t,e){},prepareTemplateStyles(t,e,s){},styleSubtree(t,e){o.processStyles(),(0,n.wW)(t,e)},styleElement(t){o.processStyles()},styleDocument(t){o.processStyles(),(0,n.wW)(document.body,t)},getComputedStyleValue:(t,e)=>(0,n.B7)(t,e),flushCustomStyles(){},nativeCss:r.rd,nativeShadow:r.WA,cssBuild:r.Cp,disableRuntime:r.jF}),window.ShadyCSS.CustomStyleInterface=o;var a=s(15392);const l="include",h=window.ShadyCSS.CustomStyleInterface;class d extends HTMLElement{constructor(){super(),this._style=null,h.addCustomStyle(this)}getStyle(){if(this._style)return this._style;const t=this.querySelector("style");if(!t)return null;this._style=t;const e=t.getAttribute(l);return e&&(t.removeAttribute(l),t.textContent=(0,a.jv)(e)+t.textContent),this.ownerDocument!==window.document&&window.document.head.appendChild(this),this._style}}window.customElements.define("custom-style",d)},9024:(t,e,s)=>{"use strict";s(56646);var i=s(40729),n=s(18691),r=s(60995),o=s(74460);const a=(0,r._)((0,n.w)((0,i.q)(HTMLElement)));customElements.define("dom-bind",class extends a{static get observedAttributes(){return["mutable-data"]}constructor(){if(super(),o.XN)throw new Error("strictTemplatePolicy: dom-bind not allowed");this.root=null,this.$=null,this.__children=null}attributeChangedCallback(){this.mutableData=!0}connectedCallback(){this.style.display="none",this.render()}disconnectedCallback(){this.__removeChildren()}__insertChildren(){this.parentNode.insertBefore(this.root,this)}__removeChildren(){if(this.__children)for(let t=0;t<this.__children.length;t++)this.root.appendChild(this.__children[t])}render(){let t;if(!this.__children){if(t=t||this.querySelector("template"),!t){let e=new MutationObserver((()=>{if(t=this.querySelector("template"),!t)throw new Error("dom-bind requires a <template> child");e.disconnect(),this.render()}));return void e.observe(this,{childList:!0})}this.root=this._stampTemplate(t),this.$=this.root.$,this.__children=[];for(let t=this.root.firstChild;t;t=t.nextSibling)this.__children[this.__children.length]=t;this._enableProperties()}this.__insertChildren(),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}})},26047:(t,e,s)=>{"use strict";var i=s(28426),n=s(52521),r=s(78956),o=s(93252),a=s(21683),l=s(4059);class h extends i.H3{static get is(){return"dom-if"}static get template(){return null}static get properties(){return{if:{type:Boolean,observer:"__debounceRender"},restamp:{type:Boolean,observer:"__debounceRender"}}}constructor(){super(),this.__renderDebouncer=null,this.__invalidProps=null,this.__instance=null,this._lastIf=!1,this.__ctor=null,this.__hideTemplateChildren__=!1}__debounceRender(){this.__renderDebouncer=r.d.debounce(this.__renderDebouncer,a.YA,(()=>this.__render())),(0,o.E)(this.__renderDebouncer)}disconnectedCallback(){super.disconnectedCallback(),this.parentNode&&(this.parentNode.nodeType!=Node.DOCUMENT_FRAGMENT_NODE||this.parentNode.host)||this.__teardownInstance()}connectedCallback(){super.connectedCallback(),this.style.display="none",this.if&&this.__debounceRender()}render(){(0,o.y)()}__render(){if(this.if){if(!this.__ensureInstance())return;this._showHideChildren()}else this.restamp&&this.__teardownInstance();!this.restamp&&this.__instance&&this._showHideChildren(),this.if!=this._lastIf&&(this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this._lastIf=this.if)}__ensureInstance(){let t=this.parentNode;if(t){if(!this.__ctor){let t=this.querySelector("template");if(!t){let t=new MutationObserver((()=>{if(!this.querySelector("template"))throw new Error("dom-if requires a <template> child");t.disconnect(),this.__render()}));return t.observe(this,{childList:!0}),!1}this.__ctor=(0,n.Uv)(t,this,{mutableData:!0,forwardHostProp:function(t,e){this.__instance&&(this.if?this.__instance.forwardHostProp(t,e):(this.__invalidProps=this.__invalidProps||Object.create(null),this.__invalidProps[(0,l.Jz)(t)]=!0))}})}if(this.__instance){this.__syncHostProperties();let e=this.__instance.children;if(e&&e.length){if(this.previousSibling!==e[e.length-1])for(let s,i=0;i<e.length&&(s=e[i]);i++)t.insertBefore(s,this)}}else this.__instance=new this.__ctor,t.insertBefore(this.__instance.root,this)}return!0}__syncHostProperties(){let t=this.__invalidProps;if(t){for(let e in t)this.__instance._setPendingProperty(e,this.__dataHost[e]);this.__invalidProps=null,this.__instance._flushProperties()}}__teardownInstance(){if(this.__instance){let t=this.__instance.children;if(t&&t.length){let e=t[0].parentNode;if(e)for(let s,i=0;i<t.length&&(s=t[i]);i++)e.removeChild(s)}this.__instance=null,this.__invalidProps=null}}_showHideChildren(){let t=this.__hideTemplateChildren__||!this.if;this.__instance&&this.__instance._showHideChildren(t)}}customElements.define(h.is,h)},42173:(t,e,s)=>{"use strict";var i=s(28426),n=s(52521),r=s(78956),o=s(93252),a=s(18691),l=s(4059),h=s(21683);const d=(0,a.w)(i.H3);class c extends d{static get is(){return"dom-repeat"}static get template(){return null}static get properties(){return{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},itemsIndexAs:{type:String,value:"itemsIndex"},sort:{type:Function,observer:"__sortChanged"},filter:{type:Function,observer:"__filterChanged"},observe:{type:String,observer:"__observeChanged"},delay:Number,renderedItemCount:{type:Number,notify:!0,readOnly:!0},initialCount:{type:Number,observer:"__initializeChunking"},targetFramerate:{type:Number,value:20},_targetFrameTime:{type:Number,computed:"__computeFrameTime(targetFramerate)"}}}static get observers(){return["__itemsChanged(items.*)"]}constructor(){super(),this.__instances=[],this.__limit=1/0,this.__pool=[],this.__renderDebouncer=null,this.__itemsIdxToInstIdx={},this.__chunkCount=null,this.__lastChunkTime=null,this.__sortFn=null,this.__filterFn=null,this.__observePaths=null,this.__ctor=null,this.__isDetached=!0,this.template=null}disconnectedCallback(){super.disconnectedCallback(),this.__isDetached=!0;for(let t=0;t<this.__instances.length;t++)this.__detachInstance(t)}connectedCallback(){if(super.connectedCallback(),this.style.display="none",this.__isDetached){this.__isDetached=!1;let t=this.parentNode;for(let e=0;e<this.__instances.length;e++)this.__attachInstance(e,t)}}__ensureTemplatized(){if(!this.__ctor){let t=this.template=this.querySelector("template");if(!t){let t=new MutationObserver((()=>{if(!this.querySelector("template"))throw new Error("dom-repeat requires a <template> child");t.disconnect(),this.__render()}));return t.observe(this,{childList:!0}),!1}let e={};e[this.as]=!0,e[this.indexAs]=!0,e[this.itemsIndexAs]=!0,this.__ctor=(0,n.Uv)(t,this,{mutableData:this.mutableData,parentModel:!0,instanceProps:e,forwardHostProp:function(t,e){let s=this.__instances;for(let i,n=0;n<s.length&&(i=s[n]);n++)i.forwardHostProp(t,e)},notifyInstanceProp:function(t,e,s){if((0,l.wB)(this.as,e)){let i=t[this.itemsIndexAs];e==this.as&&(this.items[i]=s);let n=(0,l.Iu)(this.as,"items."+i,e);this.notifyPath(n,s)}}})}return!0}__getMethodHost(){return this.__dataHost._methodHost||this.__dataHost}__functionFromPropertyValue(t){if("string"==typeof t){let e=t,s=this.__getMethodHost();return function(){return s[e].apply(s,arguments)}}return t}__sortChanged(t){this.__sortFn=this.__functionFromPropertyValue(t),this.items&&this.__debounceRender(this.__render)}__filterChanged(t){this.__filterFn=this.__functionFromPropertyValue(t),this.items&&this.__debounceRender(this.__render)}__computeFrameTime(t){return Math.ceil(1e3/t)}__initializeChunking(){this.initialCount&&(this.__limit=this.initialCount,this.__chunkCount=this.initialCount,this.__lastChunkTime=performance.now())}__tryRenderChunk(){this.items&&this.__limit<this.items.length&&this.__debounceRender(this.__requestRenderChunk)}__requestRenderChunk(){requestAnimationFrame((()=>this.__renderChunk()))}__renderChunk(){let t=performance.now(),e=this._targetFrameTime/(t-this.__lastChunkTime);this.__chunkCount=Math.round(this.__chunkCount*e)||1,this.__limit+=this.__chunkCount,this.__lastChunkTime=t,this.__debounceRender(this.__render)}__observeChanged(){this.__observePaths=this.observe&&this.observe.replace(".*",".").split(" ")}__itemsChanged(t){this.items&&!Array.isArray(this.items)&&console.warn("dom-repeat expected array for `items`, found",this.items),this.__handleItemPath(t.path,t.value)||(this.__initializeChunking(),this.__debounceRender(this.__render))}__handleObservedPaths(t){if(this.__sortFn||this.__filterFn)if(t){if(this.__observePaths){let e=this.__observePaths;for(let s=0;s<e.length;s++)0===t.indexOf(e[s])&&this.__debounceRender(this.__render,this.delay)}}else this.__debounceRender(this.__render,this.delay)}__debounceRender(t,e=0){this.__renderDebouncer=r.d.debounce(this.__renderDebouncer,e>0?h.Wc.after(e):h.YA,t.bind(this)),(0,o.E)(this.__renderDebouncer)}render(){this.__debounceRender(this.__render),(0,o.y)()}__render(){this.__ensureTemplatized()&&(this.__applyFullRefresh(),this.__pool.length=0,this._setRenderedItemCount(this.__instances.length),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this.__tryRenderChunk())}__applyFullRefresh(){let t=this.items||[],e=new Array(t.length);for(let s=0;s<t.length;s++)e[s]=s;this.__filterFn&&(e=e.filter(((e,s,i)=>this.__filterFn(t[e],s,i)))),this.__sortFn&&e.sort(((e,s)=>this.__sortFn(t[e],t[s])));const s=this.__itemsIdxToInstIdx={};let i=0;const n=Math.min(e.length,this.__limit);for(;i<n;i++){let n=this.__instances[i],r=e[i],o=t[r];s[r]=i,n?(n._setPendingProperty(this.as,o),n._setPendingProperty(this.indexAs,i),n._setPendingProperty(this.itemsIndexAs,r),n._flushProperties()):this.__insertInstance(o,i,r)}for(let t=this.__instances.length-1;t>=i;t--)this.__detachAndRemoveInstance(t)}__detachInstance(t){let e=this.__instances[t];for(let t=0;t<e.children.length;t++){let s=e.children[t];e.root.appendChild(s)}return e}__attachInstance(t,e){let s=this.__instances[t];e.insertBefore(s.root,this)}__detachAndRemoveInstance(t){let e=this.__detachInstance(t);e&&this.__pool.push(e),this.__instances.splice(t,1)}__stampInstance(t,e,s){let i={};return i[this.as]=t,i[this.indexAs]=e,i[this.itemsIndexAs]=s,new this.__ctor(i)}__insertInstance(t,e,s){let i=this.__pool.pop();i?(i._setPendingProperty(this.as,t),i._setPendingProperty(this.indexAs,e),i._setPendingProperty(this.itemsIndexAs,s),i._flushProperties()):i=this.__stampInstance(t,e,s);let n=this.__instances[e+1],r=n?n.children[0]:this;return this.parentNode.insertBefore(i.root,r),this.__instances[e]=i,i}_showHideChildren(t){for(let e=0;e<this.__instances.length;e++)this.__instances[e]._showHideChildren(t)}__handleItemPath(t,e){let s=t.slice(6),i=s.indexOf("."),n=i<0?s:s.substring(0,i);if(n==parseInt(n,10)){let t=i<0?"":s.substring(i+1);this.__handleObservedPaths(t);let r=this.__itemsIdxToInstIdx[n],o=this.__instances[r];if(o){let s=this.as+(t?"."+t:"");o._setPendingPropertyOrPath(s,e,!1,!0),o._flushProperties()}return!0}}itemForElement(t){let e=this.modelForElement(t);return e&&e[this.as]}indexForElement(t){let e=this.modelForElement(t);return e&&e[this.indexAs]}modelForElement(t){return(0,n.GJ)(this.template,t)}}customElements.define(c.is,c)},81850:(t,e,s)=>{"use strict";s.d(e,{x:()=>pt});var i=s(26539);class n{constructor(){this.start=0,this.end=0,this.previous=null,this.parent=null,this.rules=null,this.parsedCssText="",this.cssText="",this.atRule=!1,this.type=0,this.keyframesName="",this.selector="",this.parsedSelector=""}}function r(t){return o(function(t){let e=new n;e.start=0,e.end=t.length;let s=e;for(let i=0,r=t.length;i<r;i++)if(t[i]===h){s.rules||(s.rules=[]);let t=s,e=t.rules[t.rules.length-1]||null;s=new n,s.start=i+1,s.parent=t,s.previous=e,t.rules.push(s)}else t[i]===d&&(s.end=i+1,s=s.parent||e);return e}(t=t.replace(c.comments,"").replace(c.port,"")),t)}function o(t,e){let s=e.substring(t.start,t.end-1);if(t.parsedCssText=t.cssText=s.trim(),t.parent){let i=t.previous?t.previous.end:t.parent.start;s=e.substring(i,t.start-1),s=function(t){return t.replace(/\\([0-9a-f]{1,6})\s/gi,(function(){let t=arguments[1],e=6-t.length;for(;e--;)t="0"+t;return"\\"+t}))}(s),s=s.replace(c.multipleSpaces," "),s=s.substring(s.lastIndexOf(";")+1);let n=t.parsedSelector=t.selector=s.trim();t.atRule=0===n.indexOf(_),t.atRule?0===n.indexOf(p)?t.type=l.MEDIA_RULE:n.match(c.keyframesRule)&&(t.type=l.KEYFRAMES_RULE,t.keyframesName=t.selector.split(c.multipleSpaces).pop()):0===n.indexOf(u)?t.type=l.MIXIN_RULE:t.type=l.STYLE_RULE}let i=t.rules;if(i)for(let t,s=0,n=i.length;s<n&&(t=i[s]);s++)o(t,e);return t}function a(t,e,s=""){let i="";if(t.cssText||t.rules){let s=t.rules;if(s&&!function(t){let e=t[0];return Boolean(e)&&Boolean(e.selector)&&0===e.selector.indexOf(u)}(s))for(let t,n=0,r=s.length;n<r&&(t=s[n]);n++)i=a(t,e,i);else i=e?t.cssText:function(t){return function(t){return t.replace(c.mixinApply,"").replace(c.varApply,"")}(t=function(t){return t.replace(c.customProp,"").replace(c.mixinProp,"")}(t))}(t.cssText),i=i.trim(),i&&(i="  "+i+"\n")}return i&&(t.selector&&(s+=t.selector+" "+h+"\n"),s+=i,t.selector&&(s+=d+"\n\n")),s}const l={STYLE_RULE:1,KEYFRAMES_RULE:7,MEDIA_RULE:4,MIXIN_RULE:1e3},h="{",d="}",c={comments:/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,port:/@import[^;]*;/gim,customProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?(?:[;\n]|$)/gim,mixinProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?{[^}]*?}(?:[;\n]|$)?/gim,mixinApply:/@apply\s*\(?[^);]*\)?\s*(?:[;\n]|$)?/gim,varApply:/[^;:]*?:[^;]*?var\([^;]*\)(?:[;\n]|$)?/gim,keyframesRule:/^@[^\s]*keyframes/,multipleSpaces:/\s+/g},u="--",p="@media",_="@";var f=s(60309);const m=new Set;function y(t){const e=t.textContent;if(!m.has(e)){m.add(e);const s=t.cloneNode(!0);document.head.appendChild(s)}}function g(t){return t.hasAttribute("shady-unscoped")}function b(t,e){return t?("string"==typeof t&&(t=r(t)),e&&C(t,e),a(t,i.rd)):""}function x(t){return!t.__cssRules&&t.textContent&&(t.__cssRules=r(t.textContent)),t.__cssRules||null}function C(t,e,s,i){if(!t)return;let n=!1,r=t.type;if(i&&r===l.MEDIA_RULE){let e=t.selector.match(f.mA);e&&(window.matchMedia(e[1]).matches||(n=!0))}r===l.STYLE_RULE?e(t):s&&r===l.KEYFRAMES_RULE?s(t):r===l.MIXIN_RULE&&(n=!0);let o=t.rules;if(o&&!n)for(let t,n=0,r=o.length;n<r&&(t=o[n]);n++)C(t,e,s,i)}function P(t,e){let s=0;for(let i=e,n=t.length;i<n;i++)if("("===t[i])s++;else if(")"===t[i]&&0==--s)return i;return-1}function w(t,e){let s=t.indexOf("var(");if(-1===s)return e(t,"","","");let i=P(t,s+3),n=t.substring(s+4,i),r=t.substring(0,s),o=w(t.substring(i+1),e),a=n.indexOf(",");return-1===a?e(r,n.trim(),"",o):e(r,n.substring(0,a).trim(),n.substring(a+1).trim(),o)}window.ShadyDOM&&window.ShadyDOM.wrap;const v="css-build";function S(t){if(void 0!==i.Cp)return i.Cp;if(void 0===t.__cssBuild){const e=t.getAttribute(v);if(e)t.__cssBuild=e;else{const e=function(t){const e="template"===t.localName?t.content.firstChild:t.firstChild;if(e instanceof Comment){const t=e.textContent.trim().split(":");if(t[0]===v)return t[1]}return""}(t);""!==e&&function(t){const e="template"===t.localName?t.content.firstChild:t.firstChild;e.parentNode.removeChild(e)}(t),t.__cssBuild=e}}return t.__cssBuild||""}function E(t){return""!==S(t)}var O=s(10868);const T=/;\s*/m,A=/^\s*(initial)|(inherit)\s*$/,N=/\s*!important/,I="_-_";class k{constructor(){this._map={}}set(t,e){t=t.trim(),this._map[t]={properties:e,dependants:{}}}get(t){return t=t.trim(),this._map[t]||null}}let R=null;class M{constructor(){this._currentElement=null,this._measureElement=null,this._map=new k}detectMixin(t){return(0,O.OH)(t)}gatherStyles(t){const e=function(t){const e=[],s=t.querySelectorAll("style");for(let t=0;t<s.length;t++){const n=s[t];g(n)?i.WA||(y(n),n.parentNode.removeChild(n)):(e.push(n.textContent),n.parentNode.removeChild(n))}return e.join("").trim()}(t.content);if(e){const s=document.createElement("style");return s.textContent=e,t.content.insertBefore(s,t.content.firstChild),s}return null}transformTemplate(t,e){void 0===t._gatheredStyle&&(t._gatheredStyle=this.gatherStyles(t));const s=t._gatheredStyle;return s?this.transformStyle(s,e):null}transformStyle(t,e=""){let s=x(t);return this.transformRules(s,e),t.textContent=b(s),s}transformCustomStyle(t){let e=x(t);return C(e,(t=>{":root"===t.selector&&(t.selector="html"),this.transformRule(t)})),t.textContent=b(e),e}transformRules(t,e){this._currentElement=e,C(t,(t=>{this.transformRule(t)})),this._currentElement=null}transformRule(t){t.cssText=this.transformCssText(t.parsedCssText,t),":root"===t.selector&&(t.selector=":host > *")}transformCssText(t,e){return t=t.replace(f.CN,((t,s,i,n)=>this._produceCssProperties(t,s,i,n,e))),this._consumeCssProperties(t,e)}_getInitialValueForProperty(t){return this._measureElement||(this._measureElement=document.createElement("meta"),this._measureElement.setAttribute("apply-shim-measure",""),this._measureElement.style.all="initial",document.head.appendChild(this._measureElement)),window.getComputedStyle(this._measureElement).getPropertyValue(t)}_fallbacksFromPreviousRules(t){let e=t;for(;e.parent;)e=e.parent;const s={};let i=!1;return C(e,(e=>{i=i||e===t,i||e.selector===t.selector&&Object.assign(s,this._cssTextToMap(e.parsedCssText))})),s}_consumeCssProperties(t,e){let s=null;for(;s=f.$T.exec(t);){let i=s[0],n=s[1],r=s.index,o=r+i.indexOf("@apply"),a=r+i.length,l=t.slice(0,o),h=t.slice(a),d=e?this._fallbacksFromPreviousRules(e):{};Object.assign(d,this._cssTextToMap(l));let c=this._atApplyToCssProperties(n,d);t=`${l}${c}${h}`,f.$T.lastIndex=r+c.length}return t}_atApplyToCssProperties(t,e){t=t.replace(T,"");let s=[],i=this._map.get(t);if(i||(this._map.set(t,{}),i=this._map.get(t)),i){let n,r,o;this._currentElement&&(i.dependants[this._currentElement]=!0);const a=i.properties;for(n in a)o=e&&e[n],r=[n,": var(",t,I,n],o&&r.push(",",o.replace(N,"")),r.push(")"),N.test(a[n])&&r.push(" !important"),s.push(r.join(""))}return s.join("; ")}_replaceInitialOrInherit(t,e){let s=A.exec(e);return s&&(e=s[1]?this._getInitialValueForProperty(t):"apply-shim-inherit"),e}_cssTextToMap(t,e=!1){let s,i,n=t.split(";"),r={};for(let t,o,a=0;a<n.length;a++)t=n[a],t&&(o=t.split(":"),o.length>1&&(s=o[0].trim(),i=o.slice(1).join(":"),e&&(i=this._replaceInitialOrInherit(s,i)),r[s]=i));return r}_invalidateMixinEntry(t){if(R)for(let e in t.dependants)e!==this._currentElement&&R(e)}_produceCssProperties(t,e,s,i,n){if(s&&w(s,((t,e)=>{e&&this._map.get(e)&&(i=`@apply ${e};`)})),!i)return t;let r=this._consumeCssProperties(""+i,n),o=t.slice(0,t.indexOf("--")),a=this._cssTextToMap(r,!0),l=a,h=this._map.get(e),d=h&&h.properties;d?l=Object.assign(Object.create(d),a):this._map.set(e,l);let c,u,p=[],_=!1;for(c in l)u=a[c],void 0===u&&(u="initial"),d&&!(c in d)&&(_=!0),p.push(`${e}_-_${c}: ${u}`);return _&&this._invalidateMixinEntry(h),h&&(h.properties=l),s&&(o=`${t};${o}`),`${o}${p.join("; ")};`}}M.prototype.detectMixin=M.prototype.detectMixin,M.prototype.transformStyle=M.prototype.transformStyle,M.prototype.transformCustomStyle=M.prototype.transformCustomStyle,M.prototype.transformRules=M.prototype.transformRules,M.prototype.transformRule=M.prototype.transformRule,M.prototype.transformTemplate=M.prototype.transformTemplate,M.prototype._separator=I,Object.defineProperty(M.prototype,"invalidCallback",{get:()=>R,set(t){R=t}});const L=M,D={},F="_applyShimCurrentVersion",z="_applyShimNextVersion",j="_applyShimValidatingVersion",H=Promise.resolve();function B(t){let e=D[t];e&&function(t){t[F]=t[F]||0,t[j]=t[j]||0,t[z]=(t[z]||0)+1}(e)}function q(t){return t[F]===t[z]}function $(t){return!q(t)&&t[j]===t[z]}function U(t){t[j]=t[z],t._validating||(t._validating=!0,H.then((function(){t[F]=t[z],t._validating=!1})))}s(34816);const Y=new L;class V{constructor(){this.customStyleInterface=null,Y.invalidCallback=B}ensure(){this.customStyleInterface||window.ShadyCSS.CustomStyleInterface&&(this.customStyleInterface=window.ShadyCSS.CustomStyleInterface,this.customStyleInterface.transformCallback=t=>{Y.transformCustomStyle(t)},this.customStyleInterface.validateCallback=()=>{requestAnimationFrame((()=>{this.customStyleInterface.enqueued&&this.flushCustomStyles()}))})}prepareTemplate(t,e){if(this.ensure(),E(t))return;D[e]=t;let s=Y.transformTemplate(t,e);t._styleAst=s}flushCustomStyles(){if(this.ensure(),!this.customStyleInterface)return;let t=this.customStyleInterface.processStyles();if(this.customStyleInterface.enqueued){for(let e=0;e<t.length;e++){let s=t[e],i=this.customStyleInterface.getStyleForCustomStyle(s);i&&Y.transformCustomStyle(i)}this.customStyleInterface.enqueued=!1}}styleSubtree(t,e){if(this.ensure(),e&&(0,O.wW)(t,e),t.shadowRoot){this.styleElement(t);let e=t.shadowRoot.children||t.shadowRoot.childNodes;for(let t=0;t<e.length;t++)this.styleSubtree(e[t])}else{let e=t.children||t.childNodes;for(let t=0;t<e.length;t++)this.styleSubtree(e[t])}}styleElement(t){this.ensure();let{is:e}=function(t){let e=t.localName,s="",i="";return e?e.indexOf("-")>-1?s=e:(i=e,s=t.getAttribute&&t.getAttribute("is")||""):(s=t.is,i=t.extends),{is:s,typeExtension:i}}(t),s=D[e];if((!s||!E(s))&&s&&!q(s)){$(s)||(this.prepareTemplate(s,e),U(s));let i=t.shadowRoot;if(i){let t=i.querySelector("style");t&&(t.__cssRules=s._styleAst,t.textContent=b(s._styleAst))}}}styleDocument(t){this.ensure(),this.styleSubtree(document.body,t)}}if(!window.ShadyCSS||!window.ShadyCSS.ScopingShim){const t=new V;let e=window.ShadyCSS&&window.ShadyCSS.CustomStyleInterface;window.ShadyCSS={prepareTemplate(e,s,i){t.flushCustomStyles(),t.prepareTemplate(e,s)},prepareTemplateStyles(t,e,s){window.ShadyCSS.prepareTemplate(t,e,s)},prepareTemplateDom(t,e){},styleSubtree(e,s){t.flushCustomStyles(),t.styleSubtree(e,s)},styleElement(e){t.flushCustomStyles(),t.styleElement(e)},styleDocument(e){t.flushCustomStyles(),t.styleDocument(e)},getComputedStyleValue:(t,e)=>(0,O.B7)(t,e),flushCustomStyles(){t.flushCustomStyles()},nativeCss:i.rd,nativeShadow:i.WA,cssBuild:i.Cp,disableRuntime:i.jF},e&&(window.ShadyCSS.CustomStyleInterface=e)}window.ShadyCSS.ApplyShim=Y;var J=s(36608),W=s(60995),Z=s(63933),K=s(76389);const X=/:host\(:dir\((ltr|rtl)\)\)/g,G=/([\s\w-#\.\[\]\*]*):dir\((ltr|rtl)\)/g,Q=[];let tt=null,et="";function st(){et=document.documentElement.getAttribute("dir")}function it(t){if(!t.__autoDirOptOut){t.setAttribute("dir",et)}}function nt(){st(),et=document.documentElement.getAttribute("dir");for(let t=0;t<Q.length;t++)it(Q[t])}const rt=(0,K.o)((t=>{tt||(st(),tt=new MutationObserver(nt),tt.observe(document.documentElement,{attributes:!0,attributeFilter:["dir"]}));const e=(0,Z.Q)(t);class s extends e{static _processStyleText(t,e){return t=super._processStyleText(t,e),t=this._replaceDirInCssText(t)}static _replaceDirInCssText(t){let e=t;return e=e.replace(X,':host([dir="$1"])'),e=e.replace(G,':host([dir="$2"]) $1'),t!==e&&(this.__activateDir=!0),e}constructor(){super(),this.__autoDirOptOut=!1}ready(){super.ready(),this.__autoDirOptOut=this.hasAttribute("dir")}connectedCallback(){e.prototype.connectedCallback&&super.connectedCallback(),this.constructor.__activateDir&&(tt&&tt.takeRecords().length&&nt(),Q.push(this),it(this))}disconnectedCallback(){if(e.prototype.disconnectedCallback&&super.disconnectedCallback(),this.constructor.__activateDir){const t=Q.indexOf(this);t>-1&&Q.splice(t,1)}}}return s.__activateDir=!1,s}));s(87529);function ot(){document.body.removeAttribute("unresolved")}"interactive"===document.readyState||"complete"===document.readyState?ot():window.addEventListener("DOMContentLoaded",ot);var at=s(87156),lt=s(81668),ht=s(78956),dt=s(21683),ct=s(4059);let ut=window.ShadyCSS;const pt=(0,K.o)((t=>{const e=rt((0,W._)((0,J.SH)(t))),s={x:"pan-x",y:"pan-y",none:"none",all:"auto"};class i extends e{constructor(){super(),this.isAttached,this.__boundListeners,this._debouncers,this._applyListeners()}static get importMeta(){return this.prototype.importMeta}created(){}connectedCallback(){super.connectedCallback(),this.isAttached=!0,this.attached()}attached(){}disconnectedCallback(){super.disconnectedCallback(),this.isAttached=!1,this.detached()}detached(){}attributeChangedCallback(t,e,s,i){e!==s&&(super.attributeChangedCallback(t,e,s,i),this.attributeChanged(t,e,s))}attributeChanged(t,e,s){}_initializeProperties(){let t=Object.getPrototypeOf(this);t.hasOwnProperty("__hasRegisterFinished")||(t.__hasRegisterFinished=!0,this._registered()),super._initializeProperties(),this.root=this,this.created()}_registered(){}ready(){this._ensureAttributes(),super.ready()}_ensureAttributes(){}_applyListeners(){}serialize(t){return this._serializeValue(t)}deserialize(t,e){return this._deserializeValue(t,e)}reflectPropertyToAttribute(t,e,s){this._propertyToAttribute(t,e,s)}serializeValueToAttribute(t,e,s){this._valueToNodeAttribute(s||this,t,e)}extend(t,e){if(!t||!e)return t||e;let s=Object.getOwnPropertyNames(e);for(let i,n=0;n<s.length&&(i=s[n]);n++){let s=Object.getOwnPropertyDescriptor(e,i);s&&Object.defineProperty(t,i,s)}return t}mixin(t,e){for(let s in e)t[s]=e[s];return t}chainObject(t,e){return t&&e&&t!==e&&(t.__proto__=e),t}instanceTemplate(t){let e=this.constructor._contentForTemplate(t);return document.importNode(e,!0)}fire(t,e,s){s=s||{},e=null==e?{}:e;let i=new Event(t,{bubbles:void 0===s.bubbles||s.bubbles,cancelable:Boolean(s.cancelable),composed:void 0===s.composed||s.composed});return i.detail=e,(s.node||this).dispatchEvent(i),i}listen(t,e,s){t=t||this;let i=this.__boundListeners||(this.__boundListeners=new WeakMap),n=i.get(t);n||(n={},i.set(t,n));let r=e+s;n[r]||(n[r]=this._addMethodEventListenerToNode(t,e,s,this))}unlisten(t,e,s){t=t||this;let i=this.__boundListeners&&this.__boundListeners.get(t),n=e+s,r=i&&i[n];r&&(this._removeEventListenerFromNode(t,e,r),i[n]=null)}setScrollDirection(t,e){(0,lt.BP)(e||this,s[t]||"auto")}$$(t){return this.root.querySelector(t)}get domHost(){let t=this.getRootNode();return t instanceof DocumentFragment?t.host:t}distributeContent(){window.ShadyDOM&&this.shadowRoot&&ShadyDOM.flush()}getEffectiveChildNodes(){return(0,at.vz)(this).getEffectiveChildNodes()}queryDistributedElements(t){return(0,at.vz)(this).queryDistributedElements(t)}getEffectiveChildren(){return this.getEffectiveChildNodes().filter((function(t){return t.nodeType===Node.ELEMENT_NODE}))}getEffectiveTextContent(){let t=this.getEffectiveChildNodes(),e=[];for(let s,i=0;s=t[i];i++)s.nodeType!==Node.COMMENT_NODE&&e.push(s.textContent);return e.join("")}queryEffectiveChildren(t){let e=this.queryDistributedElements(t);return e&&e[0]}queryAllEffectiveChildren(t){return this.queryDistributedElements(t)}getContentChildNodes(t){let e=this.root.querySelector(t||"slot");return e?(0,at.vz)(e).getDistributedNodes():[]}getContentChildren(t){return this.getContentChildNodes(t).filter((function(t){return t.nodeType===Node.ELEMENT_NODE}))}isLightDescendant(t){const e=this;return e!==t&&e.contains(t)&&e.getRootNode()===t.getRootNode()}isLocalDescendant(t){return this.root===t.getRootNode()}scopeSubtree(t,e){}getComputedStyleValue(t){return ut.getComputedStyleValue(this,t)}debounce(t,e,s){return this._debouncers=this._debouncers||{},this._debouncers[t]=ht.d.debounce(this._debouncers[t],s>0?dt.Wc.after(s):dt.YA,e.bind(this))}isDebouncerActive(t){this._debouncers=this._debouncers||{};let e=this._debouncers[t];return!(!e||!e.isActive())}flushDebouncer(t){this._debouncers=this._debouncers||{};let e=this._debouncers[t];e&&e.flush()}cancelDebouncer(t){this._debouncers=this._debouncers||{};let e=this._debouncers[t];e&&e.cancel()}async(t,e){return e>0?dt.Wc.run(t.bind(this),e):~dt.YA.run(t.bind(this))}cancelAsync(t){t<0?dt.YA.cancel(~t):dt.Wc.cancel(t)}create(t,e){let s=document.createElement(t);if(e)if(s.setProperties)s.setProperties(e);else for(let t in e)s[t]=e[t];return s}elementMatches(t,e){return(0,at.Ku)(e||this,t)}toggleAttribute(t,e){let s=this;return 3===arguments.length&&(s=arguments[2]),1==arguments.length&&(e=!s.hasAttribute(t)),e?(s.setAttribute(t,""),!0):(s.removeAttribute(t),!1)}toggleClass(t,e,s){s=s||this,1==arguments.length&&(e=!s.classList.contains(t)),e?s.classList.add(t):s.classList.remove(t)}transform(t,e){(e=e||this).style.webkitTransform=t,e.style.transform=t}translate3d(t,e,s,i){i=i||this,this.transform("translate3d("+t+","+e+","+s+")",i)}arrayDelete(t,e){let s;if(Array.isArray(t)){if(s=t.indexOf(e),s>=0)return t.splice(s,1)}else{if(s=(0,ct.U2)(this,t).indexOf(e),s>=0)return this.splice(t,s,1)}return null}_logger(t,e){switch(Array.isArray(e)&&1===e.length&&Array.isArray(e[0])&&(e=e[0]),t){case"log":case"warn":case"error":console[t](...e)}}_log(...t){this._logger("log",t)}_warn(...t){this._logger("warn",t)}_error(...t){this._logger("error",t)}_logf(t,...e){return["[%s::%s]",this.is,t,...e]}}return i.prototype.is="",i}))},36608:(t,e,s)=>{"use strict";s.d(e,{SH:()=>c});s(56646);var i=s(74460),n=s(76389),r=s(15392),o=s(42687),a=s(21384),l=s(40729),h=s(24072);const d=(0,n.o)((t=>{const e=(0,h.e)(t);function s(t){const e=Object.getPrototypeOf(t);return e.prototype instanceof n?e:null}function i(t){if(!t.hasOwnProperty(JSCompiler_renameProperty("__ownProperties",t))){let e=null;if(t.hasOwnProperty(JSCompiler_renameProperty("properties",t))){const s=t.properties;s&&(e=function(t){const e={};for(let s in t){const i=t[s];e[s]="function"==typeof i?{type:i}:i}return e}(s))}t.__ownProperties=e}return t.__ownProperties}class n extends e{static get observedAttributes(){const t=this._properties;return t?Object.keys(t).map((t=>this.attributeNameForProperty(t))):[]}static finalize(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__finalized",this))){const t=s(this);t&&t.finalize(),this.__finalized=!0,this._finalizeClass()}}static _finalizeClass(){const t=i(this);t&&this.createProperties(t)}static get _properties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__properties",this))){const t=s(this);this.__properties=Object.assign({},t&&t._properties,i(this))}return this.__properties}static typeForProperty(t){const e=this._properties[t];return e&&e.type}_initializeProperties(){this.constructor.finalize(),super._initializeProperties()}connectedCallback(){super.connectedCallback&&super.connectedCallback(),this._enableProperties()}disconnectedCallback(){super.disconnectedCallback&&super.disconnectedCallback()}}return n})),c=(0,n.o)((t=>{const e=d((0,l.q)(t));return class extends e{static get polymerElementVersion(){return"3.0.5"}static _finalizeClass(){var t;super._finalizeClass(),this.hasOwnProperty(JSCompiler_renameProperty("is",this))&&this.is&&(t=this.prototype,u.push(t));const e=((s=this).hasOwnProperty(JSCompiler_renameProperty("__ownObservers",s))||(s.__ownObservers=s.hasOwnProperty(JSCompiler_renameProperty("observers",s))?s.observers:null),s.__ownObservers);var s;e&&this.createObservers(e,this._properties);let i=this.template;i&&("string"==typeof i?(console.error("template getter must return HTMLTemplateElement"),i=null):i=i.cloneNode(!0)),this.prototype._template=i}static createProperties(t){for(let r in t)e=this.prototype,s=r,i=t[r],n=t,i.computed&&(i.readOnly=!0),i.computed&&!e._hasReadOnlyEffect(s)&&e._createComputedProperty(s,i.computed,n),i.readOnly&&!e._hasReadOnlyEffect(s)&&e._createReadOnlyProperty(s,!i.computed),i.reflectToAttribute&&!e._hasReflectEffect(s)&&e._createReflectedProperty(s),i.notify&&!e._hasNotifyEffect(s)&&e._createNotifyingProperty(s),i.observer&&e._createPropertyObserver(s,i.observer,n[i.observer]),e._addPropertyToAttributeMap(s);var e,s,i,n}static createObservers(t,e){const s=this.prototype;for(let i=0;i<t.length;i++)s._createMethodObserver(t[i],e)}static get template(){return this.hasOwnProperty(JSCompiler_renameProperty("_template",this))||(this._template=this.prototype.hasOwnProperty(JSCompiler_renameProperty("_template",this.prototype))?this.prototype._template:function(t){let e=null;if(t&&(!i.XN||i.ZN)&&(e=a.t.import(t,"template"),i.XN&&!e))throw new Error(`strictTemplatePolicy: expecting dom-module or null template for ${t}`);return e}(this.is)||Object.getPrototypeOf(this.prototype).constructor.template),this._template}static set template(t){this._template=t}static get importPath(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_importPath",this))){const t=this.importMeta;if(t)this._importPath=(0,o.iY)(t.url);else{const t=a.t.import(this.is);this._importPath=t&&t.assetpath||Object.getPrototypeOf(this.prototype).constructor.importPath}}return this._importPath}constructor(){super(),this._template,this._importPath,this.rootPath,this.importPath,this.root,this.$}_initializeProperties(){this.constructor.finalize(),this.constructor._finalizeTemplate(this.localName),super._initializeProperties(),this.rootPath=i.sM,this.importPath=this.constructor.importPath;let t=function(t){if(!t.hasOwnProperty(JSCompiler_renameProperty("__propertyDefaults",t))){t.__propertyDefaults=null;let e=t._properties;for(let s in e){let i=e[s];"value"in i&&(t.__propertyDefaults=t.__propertyDefaults||{},t.__propertyDefaults[s]=i)}}return t.__propertyDefaults}(this.constructor);if(t)for(let e in t){let s=t[e];if(!this.hasOwnProperty(e)){let t="function"==typeof s.value?s.value.call(this):s.value;this._hasAccessor(e)?this._setPendingProperty(e,t,!0):this[e]=t}}}static _processStyleText(t,e){return(0,o.Rq)(t,e)}static _finalizeTemplate(t){const e=this.prototype._template;if(e&&!e.__polymerFinalized){e.__polymerFinalized=!0;const s=this.importPath;!function(t,e,s,i){const n=e.content.querySelectorAll("style"),o=(0,r.uT)(e),a=(0,r.lx)(s),l=e.content.firstElementChild;for(let s=0;s<a.length;s++){let n=a[s];n.textContent=t._processStyleText(n.textContent,i),e.content.insertBefore(n,l)}let h=0;for(let e=0;e<o.length;e++){let s=o[e],r=n[h];r!==s?(s=s.cloneNode(!0),r.parentNode.insertBefore(s,r)):h++,s.textContent=t._processStyleText(s.textContent,i)}window.ShadyCSS&&window.ShadyCSS.prepareTemplate(e,s)}(this,e,t,s?(0,o.Kk)(s):""),this.prototype._bindTemplate(e)}}connectedCallback(){window.ShadyCSS&&this._template&&window.ShadyCSS.styleElement(this),super.connectedCallback()}ready(){this._template&&(this.root=this._stampTemplate(this._template),this.$=this.root.$),super.ready()}_readyClients(){this._template&&(this.root=this._attachDom(this.root)),super._readyClients()}_attachDom(t){if(this.attachShadow)return t?(this.shadowRoot||this.attachShadow({mode:"open"}),this.shadowRoot.appendChild(t),this.shadowRoot):null;throw new Error("ShadowDOM not available. PolymerElement can create dom as children instead of in ShadowDOM by setting `this.root = this;` before `ready`.")}updateStyles(t){window.ShadyCSS&&window.ShadyCSS.styleSubtree(this,t)}resolveUrl(t,e){return!e&&this.importPath&&(e=(0,o.Kk)(this.importPath)),(0,o.Kk)(t,e)}static _parseTemplateContent(t,e,s){return e.dynamicFns=e.dynamicFns||this._properties,super._parseTemplateContent(t,e,s)}}}));const u=[]},60995:(t,e,s)=>{"use strict";s.d(e,{_:()=>r});s(56646);var i=s(76389),n=s(81668);const r=(0,i.o)((t=>class extends t{_addEventListenerToNode(t,e,s){(0,n.NH)(t,e,s)||super._addEventListenerToNode(t,e,s)}_removeEventListenerFromNode(t,e,s){(0,n.ys)(t,e,s)||super._removeEventListenerFromNode(t,e,s)}}))},18691:(t,e,s)=>{"use strict";s.d(e,{E:()=>r,w:()=>o});var i=s(76389);function n(t,e,s,i,n){let r;n&&(r="object"==typeof s&&null!==s,r&&(i=t.__dataTemp[e]));let o=i!==s&&(i==i||s==s);return r&&o&&(t.__dataTemp[e]=s),o}const r=(0,i.o)((t=>class extends t{_shouldPropertyChange(t,e,s){return n(this,t,e,s,!0)}})),o=(0,i.o)((t=>class extends t{static get properties(){return{mutableData:Boolean}}_shouldPropertyChange(t,e,s){return n(this,t,e,s,this.mutableData)}}));r._mutablePropertyChange=n},24072:(t,e,s)=>{"use strict";s.d(e,{e:()=>r});s(56646);var i=s(76389);const n=s(21683).YA,r=(0,i.o)((t=>class extends t{static createProperties(t){const e=this.prototype;for(let s in t)s in e||e._createPropertyAccessor(s)}static attributeNameForProperty(t){return t.toLowerCase()}static typeForProperty(t){}_createPropertyAccessor(t,e){this._addPropertyToAttributeMap(t),this.hasOwnProperty("__dataHasAccessor")||(this.__dataHasAccessor=Object.assign({},this.__dataHasAccessor)),this.__dataHasAccessor[t]||(this.__dataHasAccessor[t]=!0,this._definePropertyAccessor(t,e))}_addPropertyToAttributeMap(t){if(this.hasOwnProperty("__dataAttributes")||(this.__dataAttributes=Object.assign({},this.__dataAttributes)),!this.__dataAttributes[t]){const e=this.constructor.attributeNameForProperty(t);this.__dataAttributes[e]=t}}_definePropertyAccessor(t,e){Object.defineProperty(this,t,{get(){return this._getProperty(t)},set:e?function(){}:function(e){this._setProperty(t,e)}})}constructor(){super(),this.__dataEnabled=!1,this.__dataReady=!1,this.__dataInvalid=!1,this.__data={},this.__dataPending=null,this.__dataOld=null,this.__dataInstanceProps=null,this.__serializing=!1,this._initializeProperties()}ready(){this.__dataReady=!0,this._flushProperties()}_initializeProperties(){for(let t in this.__dataHasAccessor)this.hasOwnProperty(t)&&(this.__dataInstanceProps=this.__dataInstanceProps||{},this.__dataInstanceProps[t]=this[t],delete this[t])}_initializeInstanceProperties(t){Object.assign(this,t)}_setProperty(t,e){this._setPendingProperty(t,e)&&this._invalidateProperties()}_getProperty(t){return this.__data[t]}_setPendingProperty(t,e,s){let i=this.__data[t],n=this._shouldPropertyChange(t,e,i);return n&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),this.__dataOld&&!(t in this.__dataOld)&&(this.__dataOld[t]=i),this.__data[t]=e,this.__dataPending[t]=e),n}_invalidateProperties(){!this.__dataInvalid&&this.__dataReady&&(this.__dataInvalid=!0,n.run((()=>{this.__dataInvalid&&(this.__dataInvalid=!1,this._flushProperties())})))}_enableProperties(){this.__dataEnabled||(this.__dataEnabled=!0,this.__dataInstanceProps&&(this._initializeInstanceProperties(this.__dataInstanceProps),this.__dataInstanceProps=null),this.ready())}_flushProperties(){const t=this.__data,e=this.__dataPending,s=this.__dataOld;this._shouldPropertiesChange(t,e,s)&&(this.__dataPending=null,this.__dataOld=null,this._propertiesChanged(t,e,s))}_shouldPropertiesChange(t,e,s){return Boolean(e)}_propertiesChanged(t,e,s){}_shouldPropertyChange(t,e,s){return s!==e&&(s==s||e==e)}attributeChangedCallback(t,e,s,i){e!==s&&this._attributeToProperty(t,s),super.attributeChangedCallback&&super.attributeChangedCallback(t,e,s,i)}_attributeToProperty(t,e,s){if(!this.__serializing){const i=this.__dataAttributes,n=i&&i[t]||t;this[n]=this._deserializeValue(e,s||this.constructor.typeForProperty(n))}}_propertyToAttribute(t,e,s){this.__serializing=!0,s=arguments.length<3?this[t]:s,this._valueToNodeAttribute(this,s,e||this.constructor.attributeNameForProperty(t)),this.__serializing=!1}_valueToNodeAttribute(t,e,s){const i=this._serializeValue(e);void 0===i?t.removeAttribute(s):t.setAttribute(s,i)}_serializeValue(t){switch(typeof t){case"boolean":return t?"":void 0;default:return null!=t?t.toString():void 0}}_deserializeValue(t,e){switch(e){case Boolean:return null!==t;case Number:return Number(t);default:return t}}}))},63933:(t,e,s)=>{"use strict";s.d(e,{Q:()=>l});s(56646);var i=s(76389),n=s(67130),r=s(24072);const o={};let a=HTMLElement.prototype;for(;a;){let t=Object.getOwnPropertyNames(a);for(let e=0;e<t.length;e++)o[t[e]]=!0;a=Object.getPrototypeOf(a)}const l=(0,i.o)((t=>{const e=(0,r.e)(t);return class extends e{static createPropertiesForAttributes(){let t=this.observedAttributes;for(let e=0;e<t.length;e++)this.prototype._createPropertyAccessor((0,n.z)(t[e]))}static attributeNameForProperty(t){return(0,n.n)(t)}_initializeProperties(){this.__dataProto&&(this._initializeProtoProperties(this.__dataProto),this.__dataProto=null),super._initializeProperties()}_initializeProtoProperties(t){for(let e in t)this._setProperty(e,t[e])}_ensureAttribute(t,e){const s=this;s.hasAttribute(t)||this._valueToNodeAttribute(s,e,t)}_serializeValue(t){switch(typeof t){case"object":if(t instanceof Date)return t.toString();if(t)try{return JSON.stringify(t)}catch(t){return""}default:return super._serializeValue(t)}}_deserializeValue(t,e){let s;switch(e){case Object:try{s=JSON.parse(t)}catch(e){s=t}break;case Array:try{s=JSON.parse(t)}catch(e){s=null,console.warn(`Polymer::Attributes: couldn't decode Array as JSON: ${t}`)}break;case Date:s=isNaN(t)?String(t):Number(t),s=new Date(s);break;default:s=super._deserializeValue(t,e)}return s}_definePropertyAccessor(t,e){!function(t,e){if(!o[e]){let s=t[e];void 0!==s&&(t.__data?t._setPendingProperty(e,s):(t.__dataProto?t.hasOwnProperty(JSCompiler_renameProperty("__dataProto",t))||(t.__dataProto=Object.create(t.__dataProto)):t.__dataProto={},t.__dataProto[e]=s))}}(this,t),super._definePropertyAccessor(t,e)}_hasAccessor(t){return this.__dataHasAccessor&&this.__dataHasAccessor[t]}_isPropertyPending(t){return Boolean(this.__dataPending&&t in this.__dataPending)}}}))},40729:(t,e,s)=>{"use strict";s.d(e,{q:()=>$});s(56646);var i=s(76389),n=s(4059),r=s(67130),o=s(63933);const a={"dom-if":!0,"dom-repeat":!0};function l(t){let e=t.getAttribute("is");if(e&&a[e]){let s=t;for(s.removeAttribute("is"),t=s.ownerDocument.createElement(e),s.parentNode.replaceChild(t,s),t.appendChild(s);s.attributes.length;)t.setAttribute(s.attributes[0].name,s.attributes[0].value),s.removeAttribute(s.attributes[0].name)}return t}function h(t,e){let s=e.parentInfo&&h(t,e.parentInfo);if(!s)return t;for(let t=s.firstChild,i=0;t;t=t.nextSibling)if(e.parentIndex===i++)return t}function d(t,e,s,i){i.id&&(e[i.id]=s)}function c(t,e,s){if(s.events&&s.events.length)for(let i,n=0,r=s.events;n<r.length&&(i=r[n]);n++)t._addMethodEventListenerToNode(e,i.name,i.value,t)}function u(t,e,s){s.templateInfo&&(e._templateInfo=s.templateInfo)}const p=(0,i.o)((t=>class extends t{static _parseTemplate(t,e){if(!t._templateInfo){let s=t._templateInfo={};s.nodeInfoList=[],s.stripWhiteSpace=e&&e.stripWhiteSpace||t.hasAttribute("strip-whitespace"),this._parseTemplateContent(t,s,{parent:null})}return t._templateInfo}static _parseTemplateContent(t,e,s){return this._parseTemplateNode(t.content,e,s)}static _parseTemplateNode(t,e,s){let i,n=t;return"template"!=n.localName||n.hasAttribute("preserve-content")?"slot"===n.localName&&(e.hasInsertionPoint=!0):i=this._parseTemplateNestedTemplate(n,e,s)||i,n.firstChild&&(i=this._parseTemplateChildNodes(n,e,s)||i),n.hasAttributes&&n.hasAttributes()&&(i=this._parseTemplateNodeAttributes(n,e,s)||i),i}static _parseTemplateChildNodes(t,e,s){if("script"!==t.localName&&"style"!==t.localName)for(let i,n=t.firstChild,r=0;n;n=i){if("template"==n.localName&&(n=l(n)),i=n.nextSibling,n.nodeType===Node.TEXT_NODE){let s=i;for(;s&&s.nodeType===Node.TEXT_NODE;)n.textContent+=s.textContent,i=s.nextSibling,t.removeChild(s),s=i;if(e.stripWhiteSpace&&!n.textContent.trim()){t.removeChild(n);continue}}let o={parentIndex:r,parentInfo:s};this._parseTemplateNode(n,e,o)&&(o.infoIndex=e.nodeInfoList.push(o)-1),n.parentNode&&r++}}static _parseTemplateNestedTemplate(t,e,s){let i=this._parseTemplate(t,e);return(i.content=t.content.ownerDocument.createDocumentFragment()).appendChild(t.content),s.templateInfo=i,!0}static _parseTemplateNodeAttributes(t,e,s){let i=!1,n=Array.from(t.attributes);for(let r,o=n.length-1;r=n[o];o--)i=this._parseTemplateNodeAttribute(t,e,s,r.name,r.value)||i;return i}static _parseTemplateNodeAttribute(t,e,s,i,n){return"on-"===i.slice(0,3)?(t.removeAttribute(i),s.events=s.events||[],s.events.push({name:i.slice(3),value:n}),!0):"id"===i&&(s.id=n,!0)}static _contentForTemplate(t){let e=t._templateInfo;return e&&e.content||t.content}_stampTemplate(t){t&&!t.content&&window.HTMLTemplateElement&&HTMLTemplateElement.decorate&&HTMLTemplateElement.decorate(t);let e=this.constructor._parseTemplate(t),s=e.nodeInfoList,i=e.content||t.content,n=document.importNode(i,!0);n.__noInsertionPoint=!e.hasInsertionPoint;let r=n.nodeList=new Array(s.length);n.$={};for(let t,e=0,i=s.length;e<i&&(t=s[e]);e++){let s=r[e]=h(n,t);d(0,n.$,s,t),u(0,s,t),c(this,s,t)}return n=n,n}_addMethodEventListenerToNode(t,e,s,i){let n=function(t,e,s){return t=t._methodHost||t,function(e){t[s]?t[s](e,e.detail):console.warn("listener method `"+s+"` not defined")}}(i=i||t,0,s);return this._addEventListenerToNode(t,e,n),n}_addEventListenerToNode(t,e,s){t.addEventListener(e,s)}_removeEventListenerFromNode(t,e,s){t.removeEventListener(e,s)}}));var _=s(74460);let f=0;const m={COMPUTE:"__computeEffects",REFLECT:"__reflectEffects",NOTIFY:"__notifyEffects",PROPAGATE:"__propagateEffects",OBSERVE:"__observeEffects",READ_ONLY:"__readOnly"},y=/[A-Z]/;let g;function b(t,e){let s=t[e];if(s){if(!t.hasOwnProperty(e)){s=t[e]=Object.create(t[e]);for(let t in s){let e=s[t],i=s[t]=Array(e.length);for(let t=0;t<e.length;t++)i[t]=e[t]}}}else s=t[e]={};return s}function x(t,e,s,i,n,r){if(e){let o=!1,a=f++;for(let l in s)C(t,e,a,l,s,i,n,r)&&(o=!0);return o}return!1}function C(t,e,s,i,r,o,a,l){let h=!1,d=e[a?(0,n.Jz)(i):i];if(d)for(let e,n=0,c=d.length;n<c&&(e=d[n]);n++)e.info&&e.info.lastRun===s||a&&!P(i,e.trigger)||(e.info&&(e.info.lastRun=s),e.fn(t,i,r,o,e.info,a,l),h=!0);return h}function P(t,e){if(e){let s=e.name;return s==t||e.structured&&(0,n.jg)(s,t)||e.wildcard&&(0,n.SG)(s,t)}return!0}function w(t,e,s,i,n){let r="string"==typeof n.method?t[n.method]:n.method,o=n.property;r?r.call(t,t.__data[o],i[o]):n.dynamicFn||console.warn("observer method `"+n.method+"` not defined")}function v(t,e,s){let i=(0,n.Jz)(e);if(i!==e){return S(t,(0,r.n)(i)+"-changed",s[e],e),!0}return!1}function S(t,e,s,i){let n={value:s,queueProperty:!0};i&&(n.path=i),t.dispatchEvent(new CustomEvent(e,{detail:n}))}function E(t,e,s,i,r,o){let a=(o?(0,n.Jz)(e):e)!=e?e:null,l=a?(0,n.U2)(t,a):t.__data[e];a&&void 0===l&&(l=s[e]),S(t,r.eventName,l,a)}function O(t,e,s,i,n){let r=t.__data[e];_.v1&&(r=(0,_.v1)(r,n.attrName,"attribute",t)),t._propertyToAttribute(e,n.attrName,r)}function T(t,e,s,i,n){let r=L(t,e,s,i,n),o=n.methodInfo;t.__dataHasAccessor&&t.__dataHasAccessor[o]?t._setPendingProperty(o,r,!0):t[o]=r}function A(t,e,s,i,n,o,a){s.bindings=s.bindings||[];let l={kind:i,target:n,parts:o,literal:a,isCompound:1!==o.length};if(s.bindings.push(l),function(t){return Boolean(t.target)&&"attribute"!=t.kind&&"text"!=t.kind&&!t.isCompound&&"{"===t.parts[0].mode}(l)){let{event:t,negate:e}=l.parts[0];l.listenerEvent=t||(0,r.n)(n)+"-changed",l.listenerNegate=e}let h=e.nodeInfoList.length;for(let s=0;s<l.parts.length;s++){let i=l.parts[s];i.compoundIndex=s,N(t,e,l,i,h)}}function N(t,e,s,i,n){if(!i.literal)if("attribute"===s.kind&&"-"===s.target[0])console.warn("Cannot set attribute "+s.target+' because "-" is not a valid attribute starting character');else{let r=i.dependencies,o={index:n,binding:s,part:i,evaluator:t};for(let s=0;s<r.length;s++){let i=r[s];"string"==typeof i&&(i=H(i),i.wildcard=!0),t._addTemplatePropertyEffect(e,i.rootProperty,{fn:I,info:o,trigger:i})}}}function I(t,e,s,i,r,o,a){let l=a[r.index],h=r.binding,d=r.part;if(o&&d.source&&e.length>d.source.length&&"property"==h.kind&&!h.isCompound&&l.__isPropertyEffectsClient&&l.__dataHasAccessor&&l.__dataHasAccessor[h.target]){let i=s[e];e=(0,n.Iu)(d.source,h.target,e),l._setPendingPropertyOrPath(e,i,!1,!0)&&t._enqueueClient(l)}else{!function(t,e,s,i,n){n=function(t,e,s,i){if(s.isCompound){let n=t.__dataCompoundStorage[s.target];n[i.compoundIndex]=e,e=n.join("")}"attribute"!==s.kind&&("textContent"!==s.target&&("value"!==s.target||"input"!==t.localName&&"textarea"!==t.localName)||(e=null==e?"":e));return e}(e,n,s,i),_.v1&&(n=(0,_.v1)(n,s.target,s.kind,e));if("attribute"==s.kind)t._valueToNodeAttribute(e,n,s.target);else{let i=s.target;e.__isPropertyEffectsClient&&e.__dataHasAccessor&&e.__dataHasAccessor[i]?e[m.READ_ONLY]&&e[m.READ_ONLY][i]||e._setPendingProperty(i,n)&&t._enqueueClient(e):t._setUnmanagedPropertyToNode(e,i,n)}}(t,l,h,d,r.evaluator._evaluateBinding(t,d,e,s,i,o))}}function k(t,e){if(e.isCompound){let s=t.__dataCompoundStorage||(t.__dataCompoundStorage={}),i=e.parts,n=new Array(i.length);for(let t=0;t<i.length;t++)n[t]=i[t].literal;let r=e.target;s[r]=n,e.literal&&"property"==e.kind&&(t[r]=e.literal)}}function R(t,e,s){if(s.listenerEvent){let i=s.parts[0];t.addEventListener(s.listenerEvent,(function(t){!function(t,e,s,i,r){let o,a=t.detail,l=a&&a.path;l?(i=(0,n.Iu)(s,i,l),o=a&&a.value):o=t.currentTarget[s],o=r?!o:o,e[m.READ_ONLY]&&e[m.READ_ONLY][i]||!e._setPendingPropertyOrPath(i,o,!0,Boolean(l))||a&&a.queueProperty||e._invalidateProperties()}(t,e,s.target,i.source,i.negate)}))}}function M(t,e,s,i,n,r){r=e.static||r&&("object"!=typeof r||r[e.methodName]);let o={methodName:e.methodName,args:e.args,methodInfo:n,dynamicFn:r};for(let n,r=0;r<e.args.length&&(n=e.args[r]);r++)n.literal||t._addPropertyEffect(n.rootProperty,s,{fn:i,info:o,trigger:n});r&&t._addPropertyEffect(e.methodName,s,{fn:i,info:o})}function L(t,e,s,i,n){let r=t._methodHost||t,o=r[n.methodName];if(o){let i=t._marshalArgs(n.args,e,s);return o.apply(r,i)}n.dynamicFn||console.warn("method `"+n.methodName+"` not defined")}const D=[],F=new RegExp("(\\[\\[|{{)\\s*(?:(!)\\s*)?((?:[a-zA-Z_$][\\w.:$\\-*]*)\\s*(?:\\(\\s*(?:(?:(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*)(?:,\\s*(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*))*)?)\\)\\s*)?)(?:]]|}})","g");function z(t){let e="";for(let s=0;s<t.length;s++){e+=t[s].literal||""}return e}function j(t){let e=t.match(/([^\s]+?)\(([\s\S]*)\)/);if(e){let t={methodName:e[1],static:!0,args:D};if(e[2].trim()){return function(t,e){return e.args=t.map((function(t){let s=H(t);return s.literal||(e.static=!1),s}),this),e}(e[2].replace(/\\,/g,"&comma;").split(","),t)}return t}return null}function H(t){let e=t.trim().replace(/&comma;/g,",").replace(/\\(.)/g,"$1"),s={name:e,value:"",literal:!1},i=e[0];switch("-"===i&&(i=e[1]),i>="0"&&i<="9"&&(i="#"),i){case"'":case'"':s.value=e.slice(1,-1),s.literal=!0;break;case"#":s.value=Number(e),s.literal=!0}return s.literal||(s.rootProperty=(0,n.Jz)(e),s.structured=(0,n.AZ)(e),s.structured&&(s.wildcard=".*"==e.slice(-2),s.wildcard&&(s.name=e.slice(0,-2)))),s}function B(t,e,s,i){let n=s+".splices";t.notifyPath(n,{indexSplices:i}),t.notifyPath(s+".length",e.length),t.__data[n]={indexSplices:null}}function q(t,e,s,i,n,r){B(t,e,s,[{index:i,addedCount:n,removed:r,object:e,type:"splice"}])}const $=(0,i.o)((t=>{const e=p((0,o.Q)(t));class s extends e{constructor(){super(),this.__isPropertyEffectsClient=!0,this.__dataCounter=0,this.__dataClientsReady,this.__dataPendingClients,this.__dataToNotify,this.__dataLinkedPaths,this.__dataHasPaths,this.__dataCompoundStorage,this.__dataHost,this.__dataTemp,this.__dataClientsInitialized,this.__data,this.__dataPending,this.__dataOld,this.__computeEffects,this.__reflectEffects,this.__notifyEffects,this.__propagateEffects,this.__observeEffects,this.__readOnly,this.__templateInfo}get PROPERTY_EFFECT_TYPES(){return m}_initializeProperties(){super._initializeProperties(),U.registerHost(this),this.__dataClientsReady=!1,this.__dataPendingClients=null,this.__dataToNotify=null,this.__dataLinkedPaths=null,this.__dataHasPaths=!1,this.__dataCompoundStorage=this.__dataCompoundStorage||null,this.__dataHost=this.__dataHost||null,this.__dataTemp={},this.__dataClientsInitialized=!1}_initializeProtoProperties(t){this.__data=Object.create(t),this.__dataPending=Object.create(t),this.__dataOld={}}_initializeInstanceProperties(t){let e=this[m.READ_ONLY];for(let s in t)e&&e[s]||(this.__dataPending=this.__dataPending||{},this.__dataOld=this.__dataOld||{},this.__data[s]=this.__dataPending[s]=t[s])}_addPropertyEffect(t,e,s){this._createPropertyAccessor(t,e==m.READ_ONLY);let i=b(this,e)[t];i||(i=this[e][t]=[]),i.push(s)}_removePropertyEffect(t,e,s){let i=b(this,e)[t],n=i.indexOf(s);n>=0&&i.splice(n,1)}_hasPropertyEffect(t,e){let s=this[e];return Boolean(s&&s[t])}_hasReadOnlyEffect(t){return this._hasPropertyEffect(t,m.READ_ONLY)}_hasNotifyEffect(t){return this._hasPropertyEffect(t,m.NOTIFY)}_hasReflectEffect(t){return this._hasPropertyEffect(t,m.REFLECT)}_hasComputedEffect(t){return this._hasPropertyEffect(t,m.COMPUTE)}_setPendingPropertyOrPath(t,e,s,i){if(i||(0,n.Jz)(Array.isArray(t)?t[0]:t)!==t){if(!i){let s=(0,n.U2)(this,t);if(!(t=(0,n.t8)(this,t,e))||!super._shouldPropertyChange(t,e,s))return!1}if(this.__dataHasPaths=!0,this._setPendingProperty(t,e,s))return function(t,e,s){let i=t.__dataLinkedPaths;if(i){let r;for(let o in i){let a=i[o];(0,n.SG)(o,e)?(r=(0,n.Iu)(o,a,e),t._setPendingPropertyOrPath(r,s,!0,!0)):(0,n.SG)(a,e)&&(r=(0,n.Iu)(a,o,e),t._setPendingPropertyOrPath(r,s,!0,!0))}}}(this,t,e),!0}else{if(this.__dataHasAccessor&&this.__dataHasAccessor[t])return this._setPendingProperty(t,e,s);this[t]=e}return!1}_setUnmanagedPropertyToNode(t,e,s){s===t[e]&&"object"!=typeof s||(t[e]=s)}_setPendingProperty(t,e,s){let i=this.__dataHasPaths&&(0,n.AZ)(t),r=i?this.__dataTemp:this.__data;return!!this._shouldPropertyChange(t,e,r[t])&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),t in this.__dataOld||(this.__dataOld[t]=this.__data[t]),i?this.__dataTemp[t]=e:this.__data[t]=e,this.__dataPending[t]=e,(i||this[m.NOTIFY]&&this[m.NOTIFY][t])&&(this.__dataToNotify=this.__dataToNotify||{},this.__dataToNotify[t]=s),!0)}_setProperty(t,e){this._setPendingProperty(t,e,!0)&&this._invalidateProperties()}_invalidateProperties(){this.__dataReady&&this._flushProperties()}_enqueueClient(t){this.__dataPendingClients=this.__dataPendingClients||[],t!==this&&this.__dataPendingClients.push(t)}_flushProperties(){this.__dataCounter++,super._flushProperties(),this.__dataCounter--}_flushClients(){this.__dataClientsReady?this.__enableOrFlushClients():(this.__dataClientsReady=!0,this._readyClients(),this.__dataReady=!0)}__enableOrFlushClients(){let t=this.__dataPendingClients;if(t){this.__dataPendingClients=null;for(let e=0;e<t.length;e++){let s=t[e];s.__dataEnabled?s.__dataPending&&s._flushProperties():s._enableProperties()}}}_readyClients(){this.__enableOrFlushClients()}setProperties(t,e){for(let s in t)!e&&this[m.READ_ONLY]&&this[m.READ_ONLY][s]||this._setPendingPropertyOrPath(s,t[s],!0);this._invalidateProperties()}ready(){this._flushProperties(),this.__dataClientsReady||this._flushClients(),this.__dataPending&&this._flushProperties()}_propertiesChanged(t,e,s){let i=this.__dataHasPaths;this.__dataHasPaths=!1,function(t,e,s,i){let n=t[m.COMPUTE];if(n){let r=e;for(;x(t,n,r,s,i);)Object.assign(s,t.__dataOld),Object.assign(e,t.__dataPending),r=t.__dataPending,t.__dataPending=null}}(this,e,s,i);let n=this.__dataToNotify;this.__dataToNotify=null,this._propagatePropertyChanges(e,s,i),this._flushClients(),x(this,this[m.REFLECT],e,s,i),x(this,this[m.OBSERVE],e,s,i),n&&function(t,e,s,i,n){let r,o,a=t[m.NOTIFY],l=f++;for(let o in e)e[o]&&(a&&C(t,a,l,o,s,i,n)||n&&v(t,o,s))&&(r=!0);r&&(o=t.__dataHost)&&o._invalidateProperties&&o._invalidateProperties()}(this,n,e,s,i),1==this.__dataCounter&&(this.__dataTemp={})}_propagatePropertyChanges(t,e,s){this[m.PROPAGATE]&&x(this,this[m.PROPAGATE],t,e,s);let i=this.__templateInfo;for(;i;)x(this,i.propertyEffects,t,e,s,i.nodeList),i=i.nextTemplateInfo}linkPaths(t,e){t=(0,n.Fv)(t),e=(0,n.Fv)(e),this.__dataLinkedPaths=this.__dataLinkedPaths||{},this.__dataLinkedPaths[t]=e}unlinkPaths(t){t=(0,n.Fv)(t),this.__dataLinkedPaths&&delete this.__dataLinkedPaths[t]}notifySplices(t,e){let s={path:""};B(this,(0,n.U2)(this,t,s),s.path,e)}get(t,e){return(0,n.U2)(e||this,t)}set(t,e,s){s?(0,n.t8)(s,t,e):this[m.READ_ONLY]&&this[m.READ_ONLY][t]||this._setPendingPropertyOrPath(t,e,!0)&&this._invalidateProperties()}push(t,...e){let s={path:""},i=(0,n.U2)(this,t,s),r=i.length,o=i.push(...e);return e.length&&q(this,i,s.path,r,e.length,[]),o}pop(t){let e={path:""},s=(0,n.U2)(this,t,e),i=Boolean(s.length),r=s.pop();return i&&q(this,s,e.path,s.length,0,[r]),r}splice(t,e,s,...i){let r,o={path:""},a=(0,n.U2)(this,t,o);return e<0?e=a.length-Math.floor(-e):e&&(e=Math.floor(e)),r=2===arguments.length?a.splice(e):a.splice(e,s,...i),(i.length||r.length)&&q(this,a,o.path,e,i.length,r),r}shift(t){let e={path:""},s=(0,n.U2)(this,t,e),i=Boolean(s.length),r=s.shift();return i&&q(this,s,e.path,0,0,[r]),r}unshift(t,...e){let s={path:""},i=(0,n.U2)(this,t,s),r=i.unshift(...e);return e.length&&q(this,i,s.path,0,e.length,[]),r}notifyPath(t,e){let s;if(1==arguments.length){let i={path:""};e=(0,n.U2)(this,t,i),s=i.path}else s=Array.isArray(t)?(0,n.Fv)(t):t;this._setPendingPropertyOrPath(s,e,!0,!0)&&this._invalidateProperties()}_createReadOnlyProperty(t,e){var s;this._addPropertyEffect(t,m.READ_ONLY),e&&(this["_set"+(s=t,s[0].toUpperCase()+s.substring(1))]=function(e){this._setProperty(t,e)})}_createPropertyObserver(t,e,s){let i={property:t,method:e,dynamicFn:Boolean(s)};this._addPropertyEffect(t,m.OBSERVE,{fn:w,info:i,trigger:{name:t}}),s&&this._addPropertyEffect(e,m.OBSERVE,{fn:w,info:i,trigger:{name:e}})}_createMethodObserver(t,e){let s=j(t);if(!s)throw new Error("Malformed observer expression '"+t+"'");M(this,s,m.OBSERVE,L,null,e)}_createNotifyingProperty(t){this._addPropertyEffect(t,m.NOTIFY,{fn:E,info:{eventName:(0,r.n)(t)+"-changed",property:t}})}_createReflectedProperty(t){let e=this.constructor.attributeNameForProperty(t);"-"===e[0]?console.warn("Property "+t+" cannot be reflected to attribute "+e+' because "-" is not a valid starting attribute name. Use a lowercase first letter for the property instead.'):this._addPropertyEffect(t,m.REFLECT,{fn:O,info:{attrName:e}})}_createComputedProperty(t,e,s){let i=j(e);if(!i)throw new Error("Malformed computed expression '"+e+"'");M(this,i,m.COMPUTE,T,t,s)}_marshalArgs(t,e,s){const i=this.__data;let r=[];for(let o=0,a=t.length;o<a;o++){let a,l=t[o],h=l.name;if(l.literal?a=l.value:l.structured?(a=(0,n.U2)(i,h),void 0===a&&(a=s[h])):a=i[h],l.wildcard){let t=0===h.indexOf(e+"."),i=0===e.indexOf(h)&&!t;r[o]={path:i?e:h,value:i?s[e]:a,base:a}}else r[o]=a}return r}static addPropertyEffect(t,e,s){this.prototype._addPropertyEffect(t,e,s)}static createPropertyObserver(t,e,s){this.prototype._createPropertyObserver(t,e,s)}static createMethodObserver(t,e){this.prototype._createMethodObserver(t,e)}static createNotifyingProperty(t){this.prototype._createNotifyingProperty(t)}static createReadOnlyProperty(t,e){this.prototype._createReadOnlyProperty(t,e)}static createReflectedProperty(t){this.prototype._createReflectedProperty(t)}static createComputedProperty(t,e,s){this.prototype._createComputedProperty(t,e,s)}static bindTemplate(t){return this.prototype._bindTemplate(t)}_bindTemplate(t,e){let s=this.constructor._parseTemplate(t),i=this.__templateInfo==s;if(!i)for(let t in s.propertyEffects)this._createPropertyAccessor(t);if(e&&(s=Object.create(s),s.wasPreBound=i,!i&&this.__templateInfo)){let t=this.__templateInfoLast||this.__templateInfo;return this.__templateInfoLast=t.nextTemplateInfo=s,s.previousTemplateInfo=t,s}return this.__templateInfo=s}static _addTemplatePropertyEffect(t,e,s){(t.hostProps=t.hostProps||{})[e]=!0;let i=t.propertyEffects=t.propertyEffects||{};(i[e]=i[e]||[]).push(s)}_stampTemplate(t){U.beginHosting(this);let e=super._stampTemplate(t);U.endHosting(this);let s=this._bindTemplate(t,!0);if(s.nodeList=e.nodeList,!s.wasPreBound){let t=s.childNodes=[];for(let s=e.firstChild;s;s=s.nextSibling)t.push(s)}return e.templateInfo=s,function(t,e){let{nodeList:s,nodeInfoList:i}=e;if(i.length)for(let e=0;e<i.length;e++){let n=i[e],r=s[e],o=n.bindings;if(o)for(let e=0;e<o.length;e++){let s=o[e];k(r,s),R(r,t,s)}r.__dataHost=t}}(this,s),this.__dataReady&&x(this,s.propertyEffects,this.__data,null,!1,s.nodeList),e}_removeBoundDom(t){let e=t.templateInfo;e.previousTemplateInfo&&(e.previousTemplateInfo.nextTemplateInfo=e.nextTemplateInfo),e.nextTemplateInfo&&(e.nextTemplateInfo.previousTemplateInfo=e.previousTemplateInfo),this.__templateInfoLast==e&&(this.__templateInfoLast=e.previousTemplateInfo),e.previousTemplateInfo=e.nextTemplateInfo=null;let s=e.childNodes;for(let t=0;t<s.length;t++){let e=s[t];e.parentNode.removeChild(e)}}static _parseTemplateNode(t,e,s){let i=super._parseTemplateNode(t,e,s);if(t.nodeType===Node.TEXT_NODE){let n=this._parseBindings(t.textContent,e);n&&(t.textContent=z(n)||" ",A(this,e,s,"text","textContent",n),i=!0)}return i}static _parseTemplateNodeAttribute(t,e,s,i,n){let o=this._parseBindings(n,e);if(o){let n=i,a="property";y.test(i)?a="attribute":"$"==i[i.length-1]&&(i=i.slice(0,-1),a="attribute");let l=z(o);return l&&"attribute"==a&&t.setAttribute(i,l),"input"===t.localName&&"value"===n&&t.setAttribute(n,""),t.removeAttribute(n),"property"===a&&(i=(0,r.z)(i)),A(this,e,s,a,i,o,l),!0}return super._parseTemplateNodeAttribute(t,e,s,i,n)}static _parseTemplateNestedTemplate(t,e,s){let i=super._parseTemplateNestedTemplate(t,e,s),n=s.templateInfo.hostProps;for(let t in n){A(this,e,s,"property","_host_"+t,[{mode:"{",source:t,dependencies:[t]}])}return i}static _parseBindings(t,e){let s,i=[],n=0;for(;null!==(s=F.exec(t));){s.index>n&&i.push({literal:t.slice(n,s.index)});let r=s[1][0],o=Boolean(s[2]),a=s[3].trim(),l=!1,h="",d=-1;"{"==r&&(d=a.indexOf("::"))>0&&(h=a.substring(d+2),a=a.substring(0,d),l=!0);let c=j(a),u=[];if(c){let{args:t,methodName:s}=c;for(let e=0;e<t.length;e++){let s=t[e];s.literal||u.push(s)}let i=e.dynamicFns;(i&&i[s]||c.static)&&(u.push(s),c.dynamicFn=!0)}else u.push(a);i.push({source:a,mode:r,negate:o,customEvent:l,signature:c,dependencies:u,event:h}),n=F.lastIndex}if(n&&n<t.length){let e=t.substring(n);e&&i.push({literal:e})}return i.length?i:null}static _evaluateBinding(t,e,s,i,r,o){let a;return a=e.signature?L(t,s,i,0,e.signature):s!=e.source?(0,n.U2)(t,e.source):o&&(0,n.AZ)(s)?(0,n.U2)(t,s):t.__data[s],e.negate&&(a=!a),a}}return g=s,s}));const U=new class{constructor(){this.stack=[]}registerHost(t){if(this.stack.length){this.stack[this.stack.length-1]._enqueueClient(t)}}beginHosting(t){this.stack.push(t)}endHosting(t){let e=this.stack.length;e&&this.stack[e-1]==t&&this.stack.pop()}}},4507:(t,e,s)=>{"use strict";s.d(e,{c:()=>r});s(56646);function i(t,e,s){return{index:t,removed:e,addedCount:s}}function n(t,e,s,n,r,a){let l,h=0,d=0,c=Math.min(s-e,a-r);if(0==e&&0==r&&(h=function(t,e,s){for(let i=0;i<s;i++)if(!o(t[i],e[i]))return i;return s}(t,n,c)),s==t.length&&a==n.length&&(d=function(t,e,s){let i=t.length,n=e.length,r=0;for(;r<s&&o(t[--i],e[--n]);)r++;return r}(t,n,c-h)),r+=h,a-=d,(s-=d)-(e+=h)==0&&a-r==0)return[];if(e==s){for(l=i(e,[],0);r<a;)l.removed.push(n[r++]);return[l]}if(r==a)return[i(e,[],s-e)];let u=function(t){let e=t.length-1,s=t[0].length-1,i=t[e][s],n=[];for(;e>0||s>0;){if(0==e){n.push(2),s--;continue}if(0==s){n.push(3),e--;continue}let r,o=t[e-1][s-1],a=t[e-1][s],l=t[e][s-1];r=a<l?a<o?a:o:l<o?l:o,r==o?(o==i?n.push(0):(n.push(1),i=o),e--,s--):r==a?(n.push(3),e--,i=a):(n.push(2),s--,i=l)}return n.reverse(),n}(function(t,e,s,i,n,r){let a=r-n+1,l=s-e+1,h=new Array(a);for(let t=0;t<a;t++)h[t]=new Array(l),h[t][0]=t;for(let t=0;t<l;t++)h[0][t]=t;for(let s=1;s<a;s++)for(let r=1;r<l;r++)if(o(t[e+r-1],i[n+s-1]))h[s][r]=h[s-1][r-1];else{let t=h[s-1][r]+1,e=h[s][r-1]+1;h[s][r]=t<e?t:e}return h}(t,e,s,n,r,a));l=void 0;let p=[],_=e,f=r;for(let t=0;t<u.length;t++)switch(u[t]){case 0:l&&(p.push(l),l=void 0),_++,f++;break;case 1:l||(l=i(_,[],0)),l.addedCount++,_++,l.removed.push(n[f]),f++;break;case 2:l||(l=i(_,[],0)),l.addedCount++,_++;break;case 3:l||(l=i(_,[],0)),l.removed.push(n[f]),f++}return l&&p.push(l),p}function r(t,e){return n(t,0,t.length,e,0,e.length)}function o(t,e){return t===e}},56646:()=>{"use strict";window.JSCompiler_renameProperty=function(t,e){return t}},67130:(t,e,s)=>{"use strict";s.d(e,{z:()=>o,n:()=>a});s(56646);const i={},n=/-[a-z]/g,r=/([A-Z])/g;function o(t){return i[t]||(i[t]=t.indexOf("-")<0?t:t.replace(n,(t=>t[1].toUpperCase())))}function a(t){return i[t]||(i[t]=t.replace(r,"-$1").toLowerCase())}},78956:(t,e,s)=>{"use strict";s.d(e,{d:()=>i});s(56646),s(76389),s(21683);class i{constructor(){this._asyncModule=null,this._callback=null,this._timer=null}setConfig(t,e){this._asyncModule=t,this._callback=e,this._timer=this._asyncModule.run((()=>{this._timer=null,this._callback()}))}cancel(){this.isActive()&&(this._asyncModule.cancel(this._timer),this._timer=null)}flush(){this.isActive()&&(this.cancel(),this._callback())}isActive(){return null!=this._timer}static debounce(t,e,s){return t instanceof i?t.cancel():t=new i,t.setConfig(e,s),t}}},20723:(t,e,s)=>{"use strict";s.d(e,{o:()=>o});s(56646);var i=s(4507),n=s(21683);function r(t){return"slot"===t.localName}class o{static getFlattenedNodes(t){return r(t)?(t=t).assignedNodes({flatten:!0}):Array.from(t.childNodes).map((t=>r(t)?(t=t).assignedNodes({flatten:!0}):[t])).reduce(((t,e)=>t.concat(e)),[])}constructor(t,e){this._shadyChildrenObserver=null,this._nativeChildrenObserver=null,this._connected=!1,this._target=t,this.callback=e,this._effectiveNodes=[],this._observer=null,this._scheduled=!1,this._boundSchedule=()=>{this._schedule()},this.connect(),this._schedule()}connect(){r(this._target)?this._listenSlots([this._target]):this._target.children&&(this._listenSlots(this._target.children),window.ShadyDOM?this._shadyChildrenObserver=ShadyDOM.observeChildren(this._target,(t=>{this._processMutations(t)})):(this._nativeChildrenObserver=new MutationObserver((t=>{this._processMutations(t)})),this._nativeChildrenObserver.observe(this._target,{childList:!0}))),this._connected=!0}disconnect(){r(this._target)?this._unlistenSlots([this._target]):this._target.children&&(this._unlistenSlots(this._target.children),window.ShadyDOM&&this._shadyChildrenObserver?(ShadyDOM.unobserveChildren(this._shadyChildrenObserver),this._shadyChildrenObserver=null):this._nativeChildrenObserver&&(this._nativeChildrenObserver.disconnect(),this._nativeChildrenObserver=null)),this._connected=!1}_schedule(){this._scheduled||(this._scheduled=!0,n.YA.run((()=>this.flush())))}_processMutations(t){this._processSlotMutations(t),this.flush()}_processSlotMutations(t){if(t)for(let e=0;e<t.length;e++){let s=t[e];s.addedNodes&&this._listenSlots(s.addedNodes),s.removedNodes&&this._unlistenSlots(s.removedNodes)}}flush(){if(!this._connected)return!1;window.ShadyDOM&&ShadyDOM.flush(),this._nativeChildrenObserver?this._processSlotMutations(this._nativeChildrenObserver.takeRecords()):this._shadyChildrenObserver&&this._processSlotMutations(this._shadyChildrenObserver.takeRecords()),this._scheduled=!1;let t={target:this._target,addedNodes:[],removedNodes:[]},e=this.constructor.getFlattenedNodes(this._target),s=(0,i.c)(e,this._effectiveNodes);for(let e,i=0;i<s.length&&(e=s[i]);i++)for(let s,i=0;i<e.removed.length&&(s=e.removed[i]);i++)t.removedNodes.push(s);for(let i,n=0;n<s.length&&(i=s[n]);n++)for(let s=i.index;s<i.index+i.addedCount;s++)t.addedNodes.push(e[s]);this._effectiveNodes=e;let n=!1;return(t.addedNodes.length||t.removedNodes.length)&&(n=!0,this.callback.call(this._target,t)),n}_listenSlots(t){for(let e=0;e<t.length;e++){let s=t[e];r(s)&&s.addEventListener("slotchange",this._boundSchedule)}}_unlistenSlots(t){for(let e=0;e<t.length;e++){let s=t[e];r(s)&&s.removeEventListener("slotchange",this._boundSchedule)}}}},93252:(t,e,s)=>{"use strict";s.d(e,{E:()=>n,y:()=>o});s(56646),s(78956);let i=[];const n=function(t){i.push(t)};function r(){const t=Boolean(i.length);for(;i.length;)try{i.shift().flush()}catch(t){setTimeout((()=>{throw t}))}return t}const o=function(){let t,e;do{t=window.ShadyDOM&&ShadyDOM.flush(),window.ShadyCSS&&window.ShadyCSS.ScopingShim&&window.ShadyCSS.ScopingShim.flush(),e=r()}while(t||e)}},50856:(t,e,s)=>{"use strict";s.d(e,{d:()=>r});s(56646);class i{constructor(t){this.value=t.toString()}toString(){return this.value}}function n(t){if(t instanceof i)return t.value;throw new Error(`non-literal value passed to Polymer's htmlLiteral function: ${t}`)}const r=function(t,...e){const s=document.createElement("template");return s.innerHTML=e.reduce(((e,s,r)=>e+function(t){if(t instanceof HTMLTemplateElement)return t.innerHTML;if(t instanceof i)return n(t);throw new Error(`non-template value passed to Polymer's html function: ${t}`)}(s)+t[r+1]),t[0]),s}},76389:(t,e,s)=>{"use strict";s.d(e,{o:()=>r});s(56646);let i=0;function n(){}n.prototype.__mixinApplications,n.prototype.__mixinSet;const r=function(t){let e=t.__mixinApplications;e||(e=new WeakMap,t.__mixinApplications=e);let s=i++;return function(i){let n=i.__mixinSet;if(n&&n[s])return i;let r=e,o=r.get(i);o||(o=t(i),r.set(i,o));let a=Object.create(o.__mixinSet||n||null);return a[s]=!0,o.__mixinSet=a,o}}},4059:(t,e,s)=>{"use strict";s.d(e,{AZ:()=>i,Jz:()=>n,jg:()=>r,SG:()=>o,Iu:()=>a,wB:()=>l,Fv:()=>h,U2:()=>c,t8:()=>u});s(56646);function i(t){return t.indexOf(".")>=0}function n(t){let e=t.indexOf(".");return-1===e?t:t.slice(0,e)}function r(t,e){return 0===t.indexOf(e+".")}function o(t,e){return 0===e.indexOf(t+".")}function a(t,e,s){return e+s.slice(t.length)}function l(t,e){return t===e||r(t,e)||o(t,e)}function h(t){if(Array.isArray(t)){let e=[];for(let s=0;s<t.length;s++){let i=t[s].toString().split(".");for(let t=0;t<i.length;t++)e.push(i[t])}return e.join(".")}return t}function d(t){return Array.isArray(t)?h(t).split("."):t.toString().split(".")}function c(t,e,s){let i=t,n=d(e);for(let t=0;t<n.length;t++){if(!i)return;i=i[n[t]]}return s&&(s.path=n.join(".")),i}function u(t,e,s){let i=t,n=d(e),r=n[n.length-1];if(n.length>1){for(let t=0;t<n.length-1;t++){if(i=i[n[t]],!i)return}i[r]=s}else i[e]=s;return n.join(".")}},42687:(t,e,s)=>{"use strict";s.d(e,{Kk:()=>a,Rq:()=>l,iY:()=>h});s(56646);let i,n,r=/(url\()([^)]*)(\))/g,o=/(^\/)|(^#)|(^[\w-\d]*:)/;function a(t,e){if(t&&o.test(t))return t;if(void 0===i){i=!1;try{const t=new URL("b","http://a");t.pathname="c%20d",i="http://a/c%20d"===t.href}catch(t){}}return e||(e=document.baseURI||window.location.href),i?new URL(t,e).href:(n||(n=document.implementation.createHTMLDocument("temp"),n.base=n.createElement("base"),n.head.appendChild(n.base),n.anchor=n.createElement("a"),n.body.appendChild(n.anchor)),n.base.href=e,n.anchor.href=t,n.anchor.href||t)}function l(t,e){return t.replace(r,(function(t,s,i,n){return s+"'"+a(i.replace(/["']/g,""),e)+"'"+n}))}function h(t){return t.substring(0,t.lastIndexOf("/")+1)}},15392:(t,e,s)=>{"use strict";s.d(e,{uT:()=>d,lx:()=>c,jv:()=>p});var i=s(21384),n=s(42687);const r="shady-unscoped";function o(t){return i.t.import(t)}function a(t){let e=t.body?t.body:t;const s=(0,n.Rq)(e.textContent,t.baseURI),i=document.createElement("style");return i.textContent=s,i}function l(t){const e=t.trim().split(/\s+/),s=[];for(let t=0;t<e.length;t++)s.push(...h(e[t]));return s}function h(t){const e=o(t);if(!e)return console.warn("Could not find style data in module named",t),[];if(void 0===e._styles){const t=[];t.push(...u(e));const s=e.querySelector("template");s&&t.push(...d(s,e.assetpath)),e._styles=t}return e._styles}function d(t,e){if(!t._styles){const s=[],i=t.content.querySelectorAll("style");for(let t=0;t<i.length;t++){let r=i[t],o=r.getAttribute("include");o&&s.push(...l(o).filter((function(t,e,s){return s.indexOf(t)===e}))),e&&(r.textContent=(0,n.Rq)(r.textContent,e)),s.push(r)}t._styles=s}return t._styles}function c(t){let e=o(t);return e?u(e):[]}function u(t){const e=[],s=t.querySelectorAll("link[rel=import][type~=css]");for(let t=0;t<s.length;t++){let i=s[t];if(i.import){const t=i.import,s=i.hasAttribute(r);if(s&&!t._unscopedStyle){const e=a(t);e.setAttribute(r,""),t._unscopedStyle=e}else t._style||(t._style=a(t));e.push(s?t._unscopedStyle:t._style)}}return e}function p(t){let e=t.trim().split(/\s+/),s="";for(let t=0;t<e.length;t++)s+=_(e[t]);return s}function _(t){let e=o(t);if(e&&void 0===e._cssText){let t=f(e),s=e.querySelector("template");s&&(t+=function(t,e){let s="";const i=d(t,e);for(let t=0;t<i.length;t++){let e=i[t];e.parentNode&&e.parentNode.removeChild(e),s+=e.textContent}return s}(s,e.assetpath)),e._cssText=t||null}return e||console.warn("Could not find style data in module named",t),e&&e._cssText||""}function f(t){let e="",s=u(t);for(let t=0;t<s.length;t++)e+=s[t].textContent;return e}},60309:(t,e,s)=>{"use strict";s.d(e,{CN:()=>i,$T:()=>n,mA:()=>r});const i=/(?:^|[;\s{]\s*)(--[\w-]*?)\s*:\s*(?:((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^)]*?\)|[^};{])+)|\{([^}]*)\}(?:(?=[;\s}])|$))/gi,n=/(?:^|\W+)@apply\s*\(?([^);\n]*)\)?/gi,r=/@media\s(.*)/},10868:(t,e,s)=>{"use strict";s.d(e,{wW:()=>n,B7:()=>r,OH:()=>o});var i=s(60309);function n(t,e){for(let s in e)null===s?t.style.removeProperty(s):t.style.setProperty(s,e[s])}function r(t,e){const s=window.getComputedStyle(t).getPropertyValue(e);return s?s.trim():""}function o(t){const e=i.$T.test(t)||i.CN.test(t);return i.$T.lastIndex=0,i.CN.lastIndex=0,e}},34816:(t,e,s)=>{"use strict";s.d(e,{ZP:()=>c});let i,n=null,r=window.HTMLImports&&window.HTMLImports.whenReady||null;function o(t){requestAnimationFrame((function(){r?r(t):(n||(n=new Promise((t=>{i=t})),"complete"===document.readyState?i():document.addEventListener("readystatechange",(()=>{"complete"===document.readyState&&i()}))),n.then((function(){t&&t()})))}))}const a="__seenByShadyCSS",l="__shadyCSSCachedStyle";let h=null,d=null;class c{constructor(){this.customStyles=[],this.enqueued=!1,o((()=>{window.ShadyCSS.flushCustomStyles&&window.ShadyCSS.flushCustomStyles()}))}enqueueDocumentValidation(){!this.enqueued&&d&&(this.enqueued=!0,o(d))}addCustomStyle(t){t[a]||(t[a]=!0,this.customStyles.push(t),this.enqueueDocumentValidation())}getStyleForCustomStyle(t){if(t[l])return t[l];let e;return e=t.getStyle?t.getStyle():t,e}processStyles(){const t=this.customStyles;for(let e=0;e<t.length;e++){const s=t[e];if(s[l])continue;const i=this.getStyleForCustomStyle(s);if(i){const t=i.__appliedElement||i;h&&h(t),s[l]=t}}return t}}c.prototype.addCustomStyle=c.prototype.addCustomStyle,c.prototype.getStyleForCustomStyle=c.prototype.getStyleForCustomStyle,c.prototype.processStyles=c.prototype.processStyles,Object.defineProperties(c.prototype,{transformCallback:{get:()=>h,set(t){h=t}},validateCallback:{get:()=>d,set(t){let e=!1;d||(e=!0),d=t,e&&this.enqueueDocumentValidation()}}})},26539:(t,e,s)=>{"use strict";s.d(e,{WA:()=>i,Cp:()=>r,jF:()=>a,rd:()=>l});const i=!(window.ShadyDOM&&window.ShadyDOM.inUse);let n,r;function o(t){n=(!t||!t.shimcssproperties)&&(i||Boolean(!navigator.userAgent.match(/AppleWebKit\/601|Edge\/15/)&&window.CSS&&CSS.supports&&CSS.supports("box-shadow","0 0 0 var(--foo)")))}window.ShadyCSS&&void 0!==window.ShadyCSS.cssBuild&&(r=window.ShadyCSS.cssBuild);const a=Boolean(window.ShadyCSS&&window.ShadyCSS.disableRuntime);window.ShadyCSS&&void 0!==window.ShadyCSS.nativeCss?n=window.ShadyCSS.nativeCss:window.ShadyCSS?(o(window.ShadyCSS),window.ShadyCSS=void 0):o(window.WebComponents&&window.WebComponents.flags);const l=n},81471:(t,e,s)=>{"use strict";s.d(e,{$:()=>o});var i=s(94707);class n{constructor(t){this.classes=new Set,this.changed=!1,this.element=t;const e=(t.getAttribute("class")||"").split(/\s+/);for(const t of e)this.classes.add(t)}add(t){this.classes.add(t),this.changed=!0}remove(t){this.classes.delete(t),this.changed=!0}commit(){if(this.changed){let t="";this.classes.forEach((e=>t+=e+" ")),this.element.setAttribute("class",t)}}}const r=new WeakMap,o=(0,i.XM)((t=>e=>{if(!(e instanceof i._l)||e instanceof i.sL||"class"!==e.committer.name||e.committer.parts.length>1)throw new Error("The `classMap` directive must be used in the `class` attribute and must be the only part in the attribute.");const{committer:s}=e,{element:o}=s;let a=r.get(e);void 0===a&&(o.setAttribute("class",s.strings.join(" ")),r.set(e,a=new Set));const l=o.classList||new n(o);a.forEach((e=>{e in t||(l.remove(e),a.delete(e))}));for(const e in t){const s=t[e];s!=a.has(e)&&(s?(l.add(e),a.add(e)):(l.remove(e),a.delete(e)))}"function"==typeof l.commit&&l.commit()}))}}]);
//# sourceMappingURL=chunk.c010d4b9431ab6840991.js.map