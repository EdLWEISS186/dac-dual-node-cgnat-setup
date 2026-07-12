(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,567549,r=>{"use strict";var o="[big.js] ",i=o+"Invalid ",e=i+"decimal places",t=i+"rounding mode",a=o+"Division by zero",s={},c=void 0,l=/^-?(\d+(\.\d*)?|\.\d+)(e[+-]?\d+)?$/i;function n(r,o,i,e){var a=r.c;if(i===c&&(i=r.constructor.RM),0!==i&&1!==i&&2!==i&&3!==i)throw Error(t);if(o<1)e=3===i&&(e||!!a[0])||0===o&&(1===i&&a[0]>=5||2===i&&(a[0]>5||5===a[0]&&(e||a[1]!==c))),a.length=1,e?(r.e=r.e-o+1,a[0]=1):a[0]=r.e=0;else if(o<a.length){if(e=1===i&&a[o]>=5||2===i&&(a[o]>5||5===a[o]&&(e||a[o+1]!==c||1&a[o-1]))||3===i&&(e||!!a[0]),a.length=o,e){for(;++a[--o]>9;)if(a[o]=0,0===o){++r.e,a.unshift(1);break}}for(o=a.length;!a[--o];)a.pop()}return r}function u(r,o,i){var e=r.e,t=r.c.join(""),a=t.length;if(o)t=t.charAt(0)+(a>1?"."+t.slice(1):"")+(e<0?"e":"e+")+e;else if(e<0){for(;++e;)t="0"+t;t="0."+t}else if(e>0)if(++e>a)for(e-=a;e--;)t+="0";else e<a&&(t=t.slice(0,e)+"."+t.slice(e));else a>1&&(t=t.charAt(0)+"."+t.slice(1));return r.s<0&&i?"-"+t:t}s.abs=function(){var r=new this.constructor(this);return r.s=1,r},s.cmp=function(r){var o,i=this.c,e=(r=new this.constructor(r)).c,t=this.s,a=r.s,s=this.e,c=r.e;if(!i[0]||!e[0])return i[0]?t:e[0]?-a:0;if(t!=a)return t;if(o=t<0,s!=c)return s>c^o?1:-1;for(t=-1,a=(s=i.length)<(c=e.length)?s:c;++t<a;)if(i[t]!=e[t])return i[t]>e[t]^o?1:-1;return s==c?0:s>c^o?1:-1},s.div=function(r){var o=this.constructor,i=this.c,t=(r=new o(r)).c,s=this.s==r.s?1:-1,l=o.DP;if(l!==~~l||l<0||l>1e6)throw Error(e);if(!t[0])throw Error(a);if(!i[0])return r.s=s,r.c=[r.e=0],r;var u,w,g,b,m,f=t.slice(),h=u=t.length,v=i.length,p=i.slice(0,u),d=p.length,x=r,y=x.c=[],S=0,A=l+(x.e=this.e-r.e)+1;for(x.s=s,s=A<0?0:A,f.unshift(0);d++<u;)p.push(0);do{for(g=0;g<10;g++){if(u!=(d=p.length))b=u>d?1:-1;else for(m=-1,b=0;++m<u;)if(t[m]!=p[m]){b=t[m]>p[m]?1:-1;break}if(b<0){for(w=d==u?t:f;d;){if(p[--d]<w[d]){for(m=d;m&&!p[--m];)p[m]=9;--p[m],p[d]+=10}p[d]-=w[d]}for(;!p[0];)p.shift()}else break}y[S++]=b?g:++g,p[0]&&b?p[d]=i[h]||0:p=[i[h]]}while((h++<v||p[0]!==c)&&s--)return!y[0]&&1!=S&&(y.shift(),x.e--,A--),S>A&&n(x,A,o.RM,p[0]!==c),x},s.eq=function(r){return 0===this.cmp(r)},s.gt=function(r){return this.cmp(r)>0},s.gte=function(r){return this.cmp(r)>-1},s.lt=function(r){return 0>this.cmp(r)},s.lte=function(r){return 1>this.cmp(r)},s.minus=s.sub=function(r){var o,i,e,t,a=this.constructor,s=this.s,c=(r=new a(r)).s;if(s!=c)return r.s=-c,this.plus(r);var l=this.c.slice(),n=this.e,u=r.c,w=r.e;if(!l[0]||!u[0])return u[0]?r.s=-c:l[0]?r=new a(this):r.s=1,r;if(s=n-w){for((t=s<0)?(s=-s,e=l):(w=n,e=u),e.reverse(),c=s;c--;)e.push(0);e.reverse()}else for(i=((t=l.length<u.length)?l:u).length,s=c=0;c<i;c++)if(l[c]!=u[c]){t=l[c]<u[c];break}if(t&&(e=l,l=u,u=e,r.s=-r.s),(c=(i=u.length)-(o=l.length))>0)for(;c--;)l[o++]=0;for(c=o;i>s;){if(l[--i]<u[i]){for(o=i;o&&!l[--o];)l[o]=9;--l[o],l[i]+=10}l[i]-=u[i]}for(;0===l[--c];)l.pop();for(;0===l[0];)l.shift(),--w;return l[0]||(r.s=1,l=[w=0]),r.c=l,r.e=w,r},s.mod=function(r){var o,i=this,e=i.constructor,t=i.s,s=(r=new e(r)).s;if(!r.c[0])throw Error(a);return(i.s=r.s=1,o=1==r.cmp(i),i.s=t,r.s=s,o)?new e(i):(t=e.DP,s=e.RM,e.DP=e.RM=0,i=i.div(r),e.DP=t,e.RM=s,this.minus(i.times(r)))},s.neg=function(){var r=new this.constructor(this);return r.s=-r.s,r},s.plus=s.add=function(r){var o,i,e,t=this.constructor;if(r=new t(r),this.s!=r.s)return r.s=-r.s,this.minus(r);var a=this.e,s=this.c,c=r.e,l=r.c;if(!s[0]||!l[0])return l[0]||(s[0]?r=new t(this):r.s=this.s),r;if(s=s.slice(),o=a-c){for(o>0?(c=a,e=l):(o=-o,e=s),e.reverse();o--;)e.push(0);e.reverse()}for(s.length-l.length<0&&(e=l,l=s,s=e),o=l.length,i=0;o;s[o]%=10)i=(s[--o]=s[o]+l[o]+i)/10|0;for(i&&(s.unshift(i),++c),o=s.length;0===s[--o];)s.pop();return r.c=s,r.e=c,r},s.pow=function(r){var o=this,e=new o.constructor("1"),t=e,a=r<0;if(r!==~~r||r<-1e6||r>1e6)throw Error(i+"exponent");for(a&&(r=-r);1&r&&(t=t.times(o)),r>>=1;)o=o.times(o);return a?e.div(t):t},s.prec=function(r,o){if(r!==~~r||r<1||r>1e6)throw Error(i+"precision");return n(new this.constructor(this),r,o)},s.round=function(r,o){if(r===c)r=0;else if(r!==~~r||r<-1e6||r>1e6)throw Error(e);return n(new this.constructor(this),r+this.e+1,o)},s.sqrt=function(){var r,i,e,t=this.constructor,a=this.s,s=this.e,c=new t("0.5");if(!this.c[0])return new t(this);if(a<0)throw Error(o+"No square root");0===(a=Math.sqrt(+u(this,!0,!0)))||a===1/0?((i=this.c.join("")).length+s&1||(i+="0"),s=((s+1)/2|0)-(s<0||1&s),r=new t(((a=Math.sqrt(i))==1/0?"5e":(a=a.toExponential()).slice(0,a.indexOf("e")+1))+s)):r=new t(a+""),s=r.e+(t.DP+=4);do e=r,r=c.times(e.plus(this.div(e)));while(e.c.slice(0,s).join("")!==r.c.slice(0,s).join(""))return n(r,(t.DP-=4)+r.e+1,t.RM)},s.times=s.mul=function(r){var o,i=this.constructor,e=this.c,t=(r=new i(r)).c,a=e.length,s=t.length,c=this.e,l=r.e;if(r.s=this.s==r.s?1:-1,!e[0]||!t[0])return r.c=[r.e=0],r;for(r.e=c+l,a<s&&(o=e,e=t,t=o,l=a,a=s,s=l),o=Array(l=a+s);l--;)o[l]=0;for(c=s;c--;){for(s=0,l=a+c;l>c;)s=o[l]+t[c]*e[l-c-1]+s,o[l--]=s%10,s=s/10|0;o[l]=s}for(s?++r.e:o.shift(),c=o.length;!o[--c];)o.pop();return r.c=o,r},s.toExponential=function(r,o){var i=this,t=i.c[0];if(r!==c){if(r!==~~r||r<0||r>1e6)throw Error(e);for(i=n(new i.constructor(i),++r,o);i.c.length<r;)i.c.push(0)}return u(i,!0,!!t)},s.toFixed=function(r,o){var i=this,t=i.c[0];if(r!==c){if(r!==~~r||r<0||r>1e6)throw Error(e);for(i=n(new i.constructor(i),r+i.e+1,o),r=r+i.e+1;i.c.length<r;)i.c.push(0)}return u(i,!1,!!t)},s[Symbol.for("nodejs.util.inspect.custom")]=s.toJSON=s.toString=function(){var r=this.constructor;return u(this,this.e<=r.NE||this.e>=r.PE,!!this.c[0])},s.toNumber=function(){var r=+u(this,!0,!0);if(!0===this.constructor.strict&&!this.eq(r.toString()))throw Error(o+"Imprecise conversion");return r},s.toPrecision=function(r,o){var e=this,t=e.constructor,a=e.c[0];if(r!==c){if(r!==~~r||r<1||r>1e6)throw Error(i+"precision");for(e=n(new t(e),r,o);e.c.length<r;)e.c.push(0)}return u(e,r<=e.e||e.e<=t.NE||e.e>=t.PE,!!a)},s.valueOf=function(){var r=this.constructor;if(!0===r.strict)throw Error(o+"valueOf disallowed");return u(this,this.e<=r.NE||this.e>=r.PE,!0)};var w=function r(){function o(e){if(!(this instanceof o))return e===c?r():new o(e);if(e instanceof o)this.s=e.s,this.e=e.e,this.c=e.c.slice();else{if("string"!=typeof e){if(!0===o.strict&&"bigint"!=typeof e)throw TypeError(i+"value");e=0===e&&1/e<0?"-0":String(e)}!function(r,o){var e,t,a;if(!l.test(o))throw Error(i+"number");for(r.s="-"==o.charAt(0)?(o=o.slice(1),-1):1,(e=o.indexOf("."))>-1&&(o=o.replace(".","")),(t=o.search(/e/i))>0?(e<0&&(e=t),e+=+o.slice(t+1),o=o.substring(0,t)):e<0&&(e=o.length),a=o.length,t=0;t<a&&"0"==o.charAt(t);)++t;if(t==a)r.c=[r.e=0];else{for(;a>0&&"0"==o.charAt(--a););for(r.e=e-t-1,r.c=[],e=0;t<=a;)r.c[e++]=+o.charAt(t++)}}(this,e)}this.constructor=o}return o.prototype=s,o.DP=20,o.RM=1,o.NE=-7,o.PE=21,o.strict=!1,o.roundDown=0,o.roundHalfUp=1,o.roundHalfEven=2,o.roundUp=3,o}();r.s(["default",0,w])},759703,392074,698797,r=>{"use strict";var o=r.i(535178);let i={attribute:!0,type:String,converter:o.defaultConverter,reflect:!1,hasChanged:o.notEqual};function e(r){return(o,e)=>{let t;return"object"==typeof e?((r=i,o,e)=>{let{kind:t,metadata:a}=e,s=globalThis.litPropertyMetadata.get(a);if(void 0===s&&globalThis.litPropertyMetadata.set(a,s=new Map),"setter"===t&&((r=Object.create(r)).wrapped=!0),s.set(e.name,r),"accessor"===t){let{name:i}=e;return{set(e){let t=o.get.call(this);o.set.call(this,e),this.requestUpdate(i,t,r,!0,e)},init(o){return void 0!==o&&this.C(i,void 0,r,o),o}}}if("setter"===t){let{name:i}=e;return function(e){let t=this[i];o.call(this,e),this.requestUpdate(i,t,r,!0,e)}}throw Error("Unsupported decorator location: "+t)})(r,o,e):(t=o.hasOwnProperty(e),o.constructor.createProperty(e,r),t?Object.getOwnPropertyDescriptor(o,e):void 0)}}r.s(["property",0,e],392074),r.s(["state",0,function(r){return e({...r,state:!0,attribute:!1})}],698797),r.s([],759703)},781840,86988,r=>{"use strict";var o=r.i(872857);r.s(["ifDefined",0,r=>r??o.nothing],86988),r.s([],781840)},364521,r=>{"use strict";r.s(["Directive",0,class{constructor(r){}get _$AU(){return this._$AM._$AU}_$AT(r,o,i){this._$Ct=r,this._$AM=o,this._$Ci=i}_$AS(r,o){return this.update(r,o)}update(r,o){return this.render(...o)}},"PartType",0,{ATTRIBUTE:1,CHILD:2,PROPERTY:3,BOOLEAN_ATTRIBUTE:4,EVENT:5,ELEMENT:6},"directive",0,r=>(...o)=>({_$litDirective$:r,values:o})])},865793,513002,r=>{"use strict";var o=r.i(872857),i=r.i(364521);let e=(0,i.directive)(class extends i.Directive{constructor(r){if(super(r),r.type!==i.PartType.ATTRIBUTE||"class"!==r.name||r.strings?.length>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(r){return" "+Object.keys(r).filter(o=>r[o]).join(" ")+" "}update(r,[i]){if(void 0===this.st){for(let o in this.st=new Set,void 0!==r.strings&&(this.nt=new Set(r.strings.join(" ").split(/\s/).filter(r=>""!==r))),i)i[o]&&!this.nt?.has(o)&&this.st.add(o);return this.render(i)}let e=r.element.classList;for(let r of this.st)r in i||(e.remove(r),this.st.delete(r));for(let r in i){let o=!!i[r];o===this.st.has(r)||this.nt?.has(r)||(o?(e.add(r),this.st.add(r)):(e.remove(r),this.st.delete(r)))}return o.noChange}});r.s(["classMap",0,e],513002),r.s([],865793)},891237,941528,412088,r=>{"use strict";var o=r.i(872857);let{I:i}=o._$LH;var e=r.i(364521);let t=(r,o)=>{let i=r._$AN;if(void 0===i)return!1;for(let r of i)r._$AO?.(o,!1),t(r,o);return!0},a=r=>{let o,i;do{if(void 0===(o=r._$AM))break;(i=o._$AN).delete(r),r=o}while(0===i?.size)},s=r=>{for(let o;o=r._$AM;r=o){let i=o._$AN;if(void 0===i)o._$AN=i=new Set;else if(i.has(r))break;i.add(r),n(o)}};function c(r){void 0!==this._$AN?(a(this),this._$AM=r,s(this)):this._$AM=r}function l(r,o=!1,i=0){let e=this._$AH,s=this._$AN;if(void 0!==s&&0!==s.size)if(o)if(Array.isArray(e))for(let r=i;r<e.length;r++)t(e[r],!1),a(e[r]);else null!=e&&(t(e,!1),a(e));else t(this,r)}let n=r=>{r.type==e.PartType.CHILD&&(r._$AP??=l,r._$AQ??=c)};class u extends e.Directive{constructor(){super(...arguments),this._$AN=void 0}_$AT(r,o,i){super._$AT(r,o,i),s(this),this.isConnected=r._$AU}_$AO(r,o=!0){r!==this.isConnected&&(this.isConnected=r,r?this.reconnected?.():this.disconnected?.()),o&&(t(this,r),a(this))}setValue(r){if(void 0===this._$Ct.strings)this._$Ct._$AI(r,this);else{let o=[...this._$Ct._$AH];o[this._$Ci]=r,this._$Ct._$AI(o,this,0)}}disconnected(){}reconnected(){}}r.s(["AsyncDirective",0,u],941528);class w{constructor(r){this.G=r}disconnect(){this.G=void 0}reconnect(r){this.G=r}deref(){return this.G}}class g{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){this.Y??=new Promise(r=>this.Z=r)}resume(){this.Z?.(),this.Y=this.Z=void 0}}let b=r=>null!==r&&("object"==typeof r||"function"==typeof r)&&"function"==typeof r.then,m=(0,e.directive)(class extends u{constructor(){super(...arguments),this._$Cwt=0x3fffffff,this._$Cbt=[],this._$CK=new w(this),this._$CX=new g}render(...r){return r.find(r=>!b(r))??o.noChange}update(r,i){let e=this._$Cbt,t=e.length;this._$Cbt=i;let a=this._$CK,s=this._$CX;this.isConnected||this.disconnected();for(let r=0;r<i.length&&!(r>this._$Cwt);r++){let o=i[r];if(!b(o))return this._$Cwt=r,o;r<t&&o===e[r]||(this._$Cwt=0x3fffffff,t=0,Promise.resolve(o).then(async r=>{for(;s.get();)await s.get();let i=a.deref();if(void 0!==i){let e=i._$Cbt.indexOf(o);e>-1&&e<i._$Cwt&&(i._$Cwt=e,i.setValue(r))}}))}return o.noChange}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}});r.s(["until",0,m],412088),r.s([],891237)},742560,758901,r=>{"use strict";let o,i,e;r.i(588984);var t=r.i(334736),a=r.i(678125);function s(r){i&&e&&("light"===r?(i.removeAttribute("media"),e.media="enabled"):(e.removeAttribute("media"),i.media="enabled"))}function c(r){return{core:t.css`
      ${r?.["--w3m-font-family"]?t.css``:t.css`
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
          `}
      @keyframes w3m-shake {
        0% {
          transform: scale(1) rotate(0deg);
        }
        20% {
          transform: scale(1) rotate(-1deg);
        }
        40% {
          transform: scale(1) rotate(1.5deg);
        }
        60% {
          transform: scale(1) rotate(-1.5deg);
        }
        80% {
          transform: scale(1) rotate(1deg);
        }
        100% {
          transform: scale(1) rotate(0deg);
        }
      }
      @keyframes w3m-iframe-fade-out {
        0% {
          opacity: 1;
        }
        100% {
          opacity: 0;
        }
      }
      @keyframes w3m-iframe-zoom-in {
        0% {
          transform: translateY(50px);
          opacity: 0;
        }
        100% {
          transform: translateY(0px);
          opacity: 1;
        }
      }
      @keyframes w3m-iframe-zoom-in-mobile {
        0% {
          transform: scale(0.95);
          opacity: 0;
        }
        100% {
          transform: scale(1);
          opacity: 1;
        }
      }
      :root {
        --w3m-modal-width: 360px;
        --w3m-color-mix-strength: ${(0,t.unsafeCSS)(r?.["--w3m-color-mix-strength"]?`${r["--w3m-color-mix-strength"]}%`:"0%")};
        --w3m-font-family: ${(0,t.unsafeCSS)(r?.["--w3m-font-family"]||"Inter, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;")};
        --w3m-font-size-master: ${(0,t.unsafeCSS)(r?.["--w3m-font-size-master"]||"10px")};
        --w3m-border-radius-master: ${(0,t.unsafeCSS)(r?.["--w3m-border-radius-master"]||"4px")};
        --w3m-z-index: ${(0,t.unsafeCSS)(r?.["--w3m-z-index"]||999)};

        --wui-font-family: var(--w3m-font-family);

        --wui-font-size-mini: calc(var(--w3m-font-size-master) * 0.8);
        --wui-font-size-micro: var(--w3m-font-size-master);
        --wui-font-size-tiny: calc(var(--w3m-font-size-master) * 1.2);
        --wui-font-size-small: calc(var(--w3m-font-size-master) * 1.4);
        --wui-font-size-paragraph: calc(var(--w3m-font-size-master) * 1.6);
        --wui-font-size-medium: calc(var(--w3m-font-size-master) * 1.8);
        --wui-font-size-large: calc(var(--w3m-font-size-master) * 2);
        --wui-font-size-title-6: calc(var(--w3m-font-size-master) * 2.2);
        --wui-font-size-medium-title: calc(var(--w3m-font-size-master) * 2.4);
        --wui-font-size-2xl: calc(var(--w3m-font-size-master) * 4);

        --wui-border-radius-5xs: var(--w3m-border-radius-master);
        --wui-border-radius-4xs: calc(var(--w3m-border-radius-master) * 1.5);
        --wui-border-radius-3xs: calc(var(--w3m-border-radius-master) * 2);
        --wui-border-radius-xxs: calc(var(--w3m-border-radius-master) * 3);
        --wui-border-radius-xs: calc(var(--w3m-border-radius-master) * 4);
        --wui-border-radius-s: calc(var(--w3m-border-radius-master) * 5);
        --wui-border-radius-m: calc(var(--w3m-border-radius-master) * 7);
        --wui-border-radius-l: calc(var(--w3m-border-radius-master) * 9);
        --wui-border-radius-3xl: calc(var(--w3m-border-radius-master) * 20);

        --wui-font-weight-light: 400;
        --wui-font-weight-regular: 500;
        --wui-font-weight-medium: 600;
        --wui-font-weight-bold: 700;

        --wui-letter-spacing-2xl: -1.6px;
        --wui-letter-spacing-medium-title: -0.96px;
        --wui-letter-spacing-title-6: -0.88px;
        --wui-letter-spacing-large: -0.8px;
        --wui-letter-spacing-medium: -0.72px;
        --wui-letter-spacing-paragraph: -0.64px;
        --wui-letter-spacing-small: -0.56px;
        --wui-letter-spacing-tiny: -0.48px;
        --wui-letter-spacing-micro: -0.2px;
        --wui-letter-spacing-mini: -0.16px;

        --wui-spacing-0: 0px;
        --wui-spacing-4xs: 2px;
        --wui-spacing-3xs: 4px;
        --wui-spacing-xxs: 6px;
        --wui-spacing-2xs: 7px;
        --wui-spacing-xs: 8px;
        --wui-spacing-1xs: 10px;
        --wui-spacing-s: 12px;
        --wui-spacing-m: 14px;
        --wui-spacing-l: 16px;
        --wui-spacing-2l: 18px;
        --wui-spacing-xl: 20px;
        --wui-spacing-xxl: 24px;
        --wui-spacing-2xl: 32px;
        --wui-spacing-3xl: 40px;
        --wui-spacing-4xl: 90px;
        --wui-spacing-5xl: 95px;

        --wui-icon-box-size-xxs: 14px;
        --wui-icon-box-size-xs: 20px;
        --wui-icon-box-size-sm: 24px;
        --wui-icon-box-size-md: 32px;
        --wui-icon-box-size-mdl: 36px;
        --wui-icon-box-size-lg: 40px;
        --wui-icon-box-size-2lg: 48px;
        --wui-icon-box-size-xl: 64px;

        --wui-icon-size-inherit: inherit;
        --wui-icon-size-xxs: 10px;
        --wui-icon-size-xs: 12px;
        --wui-icon-size-sm: 14px;
        --wui-icon-size-md: 16px;
        --wui-icon-size-mdl: 18px;
        --wui-icon-size-lg: 20px;
        --wui-icon-size-xl: 24px;
        --wui-icon-size-xxl: 28px;

        --wui-wallet-image-size-inherit: inherit;
        --wui-wallet-image-size-sm: 40px;
        --wui-wallet-image-size-md: 56px;
        --wui-wallet-image-size-lg: 80px;

        --wui-visual-size-size-inherit: inherit;
        --wui-visual-size-sm: 40px;
        --wui-visual-size-md: 55px;
        --wui-visual-size-lg: 80px;

        --wui-box-size-md: 100px;
        --wui-box-size-lg: 120px;

        --wui-ease-out-power-2: cubic-bezier(0, 0, 0.22, 1);
        --wui-ease-out-power-1: cubic-bezier(0, 0, 0.55, 1);

        --wui-ease-in-power-3: cubic-bezier(0.66, 0, 1, 1);
        --wui-ease-in-power-2: cubic-bezier(0.45, 0, 1, 1);
        --wui-ease-in-power-1: cubic-bezier(0.3, 0, 1, 1);

        --wui-ease-inout-power-1: cubic-bezier(0.45, 0, 0.55, 1);

        --wui-duration-lg: 200ms;
        --wui-duration-md: 125ms;
        --wui-duration-sm: 75ms;

        --wui-path-network-sm: path(
          'M15.4 2.1a5.21 5.21 0 0 1 5.2 0l11.61 6.7a5.21 5.21 0 0 1 2.61 4.52v13.4c0 1.87-1 3.59-2.6 4.52l-11.61 6.7c-1.62.93-3.6.93-5.22 0l-11.6-6.7a5.21 5.21 0 0 1-2.61-4.51v-13.4c0-1.87 1-3.6 2.6-4.52L15.4 2.1Z'
        );

        --wui-path-network-md: path(
          'M43.4605 10.7248L28.0485 1.61089C25.5438 0.129705 22.4562 0.129705 19.9515 1.61088L4.53951 10.7248C2.03626 12.2051 0.5 14.9365 0.5 17.886V36.1139C0.5 39.0635 2.03626 41.7949 4.53951 43.2752L19.9515 52.3891C22.4562 53.8703 25.5438 53.8703 28.0485 52.3891L43.4605 43.2752C45.9637 41.7949 47.5 39.0635 47.5 36.114V17.8861C47.5 14.9365 45.9637 12.2051 43.4605 10.7248Z'
        );

        --wui-path-network-lg: path(
          'M78.3244 18.926L50.1808 2.45078C45.7376 -0.150261 40.2624 -0.150262 35.8192 2.45078L7.6756 18.926C3.23322 21.5266 0.5 26.3301 0.5 31.5248V64.4752C0.5 69.6699 3.23322 74.4734 7.6756 77.074L35.8192 93.5492C40.2624 96.1503 45.7376 96.1503 50.1808 93.5492L78.3244 77.074C82.7668 74.4734 85.5 69.6699 85.5 64.4752V31.5248C85.5 26.3301 82.7668 21.5266 78.3244 18.926Z'
        );

        --wui-width-network-sm: 36px;
        --wui-width-network-md: 48px;
        --wui-width-network-lg: 86px;

        --wui-height-network-sm: 40px;
        --wui-height-network-md: 54px;
        --wui-height-network-lg: 96px;

        --wui-icon-size-network-xs: 12px;
        --wui-icon-size-network-sm: 16px;
        --wui-icon-size-network-md: 24px;
        --wui-icon-size-network-lg: 42px;

        --wui-color-inherit: inherit;

        --wui-color-inverse-100: #fff;
        --wui-color-inverse-000: #000;

        --wui-cover: rgba(20, 20, 20, 0.8);

        --wui-color-modal-bg: var(--wui-color-modal-bg-base);

        --wui-color-accent-100: var(--wui-color-accent-base-100);
        --wui-color-accent-090: var(--wui-color-accent-base-090);
        --wui-color-accent-080: var(--wui-color-accent-base-080);

        --wui-color-success-100: var(--wui-color-success-base-100);
        --wui-color-success-125: var(--wui-color-success-base-125);

        --wui-color-warning-100: var(--wui-color-warning-base-100);

        --wui-color-error-100: var(--wui-color-error-base-100);
        --wui-color-error-125: var(--wui-color-error-base-125);

        --wui-color-blue-100: var(--wui-color-blue-base-100);
        --wui-color-blue-90: var(--wui-color-blue-base-90);

        --wui-icon-box-bg-error-100: var(--wui-icon-box-bg-error-base-100);
        --wui-icon-box-bg-blue-100: var(--wui-icon-box-bg-blue-base-100);
        --wui-icon-box-bg-success-100: var(--wui-icon-box-bg-success-base-100);
        --wui-icon-box-bg-inverse-100: var(--wui-icon-box-bg-inverse-base-100);

        --wui-all-wallets-bg-100: var(--wui-all-wallets-bg-100);

        --wui-avatar-border: var(--wui-avatar-border-base);

        --wui-thumbnail-border: var(--wui-thumbnail-border-base);

        --wui-wallet-button-bg: var(--wui-wallet-button-bg-base);

        --wui-box-shadow-blue: var(--wui-color-accent-glass-020);
      }

      @supports (background: color-mix(in srgb, white 50%, black)) {
        :root {
          --wui-color-modal-bg: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-modal-bg-base)
          );

          --wui-box-shadow-blue: color-mix(in srgb, var(--wui-color-accent-100) 20%, transparent);

          --wui-color-accent-100: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 100%,
            transparent
          );
          --wui-color-accent-090: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 90%,
            transparent
          );
          --wui-color-accent-080: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 80%,
            transparent
          );
          --wui-color-accent-glass-090: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 90%,
            transparent
          );
          --wui-color-accent-glass-080: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 80%,
            transparent
          );
          --wui-color-accent-glass-020: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 20%,
            transparent
          );
          --wui-color-accent-glass-015: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 15%,
            transparent
          );
          --wui-color-accent-glass-010: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 10%,
            transparent
          );
          --wui-color-accent-glass-005: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 5%,
            transparent
          );
          --wui-color-accent-002: color-mix(
            in srgb,
            var(--wui-color-accent-base-100) 2%,
            transparent
          );

          --wui-color-fg-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-100)
          );
          --wui-color-fg-125: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-125)
          );
          --wui-color-fg-150: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-150)
          );
          --wui-color-fg-175: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-175)
          );
          --wui-color-fg-200: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-200)
          );
          --wui-color-fg-225: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-225)
          );
          --wui-color-fg-250: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-250)
          );
          --wui-color-fg-275: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-275)
          );
          --wui-color-fg-300: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-300)
          );
          --wui-color-fg-325: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-325)
          );
          --wui-color-fg-350: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-fg-350)
          );

          --wui-color-bg-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-100)
          );
          --wui-color-bg-125: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-125)
          );
          --wui-color-bg-150: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-150)
          );
          --wui-color-bg-175: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-175)
          );
          --wui-color-bg-200: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-200)
          );
          --wui-color-bg-225: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-225)
          );
          --wui-color-bg-250: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-250)
          );
          --wui-color-bg-275: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-275)
          );
          --wui-color-bg-300: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-300)
          );
          --wui-color-bg-325: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-325)
          );
          --wui-color-bg-350: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-bg-350)
          );

          --wui-color-success-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-success-base-100)
          );
          --wui-color-success-125: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-success-base-125)
          );

          --wui-color-warning-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-warning-base-100)
          );

          --wui-color-error-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-error-base-100)
          );
          --wui-color-blue-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-blue-base-100)
          );
          --wui-color-blue-90: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-blue-base-90)
          );
          --wui-color-error-125: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-color-error-base-125)
          );

          --wui-icon-box-bg-error-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-icon-box-bg-error-base-100)
          );
          --wui-icon-box-bg-accent-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-icon-box-bg-blue-base-100)
          );
          --wui-icon-box-bg-success-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-icon-box-bg-success-base-100)
          );
          --wui-icon-box-bg-inverse-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-icon-box-bg-inverse-base-100)
          );

          --wui-all-wallets-bg-100: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-all-wallets-bg-100)
          );

          --wui-avatar-border: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-avatar-border-base)
          );

          --wui-thumbnail-border: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-thumbnail-border-base)
          );

          --wui-wallet-button-bg: color-mix(
            in srgb,
            var(--w3m-color-mix) var(--w3m-color-mix-strength),
            var(--wui-wallet-button-bg-base)
          );
        }
      }
    `,light:t.css`
      :root {
        --w3m-color-mix: ${(0,t.unsafeCSS)(r?.["--w3m-color-mix"]||"#fff")};
        --w3m-accent: ${(0,t.unsafeCSS)((0,a.getW3mThemeVariables)(r,"dark")["--w3m-accent"])};
        --w3m-default: #fff;

        --wui-color-modal-bg-base: ${(0,t.unsafeCSS)((0,a.getW3mThemeVariables)(r,"dark")["--w3m-background"])};
        --wui-color-accent-base-100: var(--w3m-accent);

        --wui-color-blueberry-100: hsla(230, 100%, 67%, 1);
        --wui-color-blueberry-090: hsla(231, 76%, 61%, 1);
        --wui-color-blueberry-080: hsla(230, 59%, 55%, 1);
        --wui-color-blueberry-050: hsla(231, 100%, 70%, 0.1);

        --wui-color-fg-100: #e4e7e7;
        --wui-color-fg-125: #d0d5d5;
        --wui-color-fg-150: #a8b1b1;
        --wui-color-fg-175: #a8b0b0;
        --wui-color-fg-200: #949e9e;
        --wui-color-fg-225: #868f8f;
        --wui-color-fg-250: #788080;
        --wui-color-fg-275: #788181;
        --wui-color-fg-300: #6e7777;
        --wui-color-fg-325: #9a9a9a;
        --wui-color-fg-350: #363636;

        --wui-color-bg-100: #141414;
        --wui-color-bg-125: #191a1a;
        --wui-color-bg-150: #1e1f1f;
        --wui-color-bg-175: #222525;
        --wui-color-bg-200: #272a2a;
        --wui-color-bg-225: #2c3030;
        --wui-color-bg-250: #313535;
        --wui-color-bg-275: #363b3b;
        --wui-color-bg-300: #3b4040;
        --wui-color-bg-325: #252525;
        --wui-color-bg-350: #ffffff;

        --wui-color-success-base-100: #26d962;
        --wui-color-success-base-125: #30a46b;

        --wui-color-warning-base-100: #f3a13f;

        --wui-color-error-base-100: #f25a67;
        --wui-color-error-base-125: #df4a34;

        --wui-color-blue-base-100: rgba(102, 125, 255, 1);
        --wui-color-blue-base-90: rgba(102, 125, 255, 0.9);

        --wui-color-success-glass-001: rgba(38, 217, 98, 0.01);
        --wui-color-success-glass-002: rgba(38, 217, 98, 0.02);
        --wui-color-success-glass-005: rgba(38, 217, 98, 0.05);
        --wui-color-success-glass-010: rgba(38, 217, 98, 0.1);
        --wui-color-success-glass-015: rgba(38, 217, 98, 0.15);
        --wui-color-success-glass-020: rgba(38, 217, 98, 0.2);
        --wui-color-success-glass-025: rgba(38, 217, 98, 0.25);
        --wui-color-success-glass-030: rgba(38, 217, 98, 0.3);
        --wui-color-success-glass-060: rgba(38, 217, 98, 0.6);
        --wui-color-success-glass-080: rgba(38, 217, 98, 0.8);

        --wui-color-success-glass-reown-020: rgba(48, 164, 107, 0.2);

        --wui-color-warning-glass-reown-020: rgba(243, 161, 63, 0.2);

        --wui-color-error-glass-001: rgba(242, 90, 103, 0.01);
        --wui-color-error-glass-002: rgba(242, 90, 103, 0.02);
        --wui-color-error-glass-005: rgba(242, 90, 103, 0.05);
        --wui-color-error-glass-010: rgba(242, 90, 103, 0.1);
        --wui-color-error-glass-015: rgba(242, 90, 103, 0.15);
        --wui-color-error-glass-020: rgba(242, 90, 103, 0.2);
        --wui-color-error-glass-025: rgba(242, 90, 103, 0.25);
        --wui-color-error-glass-030: rgba(242, 90, 103, 0.3);
        --wui-color-error-glass-060: rgba(242, 90, 103, 0.6);
        --wui-color-error-glass-080: rgba(242, 90, 103, 0.8);

        --wui-color-error-glass-reown-020: rgba(223, 74, 52, 0.2);

        --wui-color-gray-glass-001: rgba(255, 255, 255, 0.01);
        --wui-color-gray-glass-002: rgba(255, 255, 255, 0.02);
        --wui-color-gray-glass-005: rgba(255, 255, 255, 0.05);
        --wui-color-gray-glass-010: rgba(255, 255, 255, 0.1);
        --wui-color-gray-glass-015: rgba(255, 255, 255, 0.15);
        --wui-color-gray-glass-020: rgba(255, 255, 255, 0.2);
        --wui-color-gray-glass-025: rgba(255, 255, 255, 0.25);
        --wui-color-gray-glass-030: rgba(255, 255, 255, 0.3);
        --wui-color-gray-glass-060: rgba(255, 255, 255, 0.6);
        --wui-color-gray-glass-080: rgba(255, 255, 255, 0.8);
        --wui-color-gray-glass-090: rgba(255, 255, 255, 0.9);

        --wui-color-dark-glass-100: rgba(42, 42, 42, 1);

        --wui-icon-box-bg-error-base-100: #3c2426;
        --wui-icon-box-bg-blue-base-100: #20303f;
        --wui-icon-box-bg-success-base-100: #1f3a28;
        --wui-icon-box-bg-inverse-base-100: #243240;

        --wui-all-wallets-bg-100: #222b35;

        --wui-avatar-border-base: #252525;

        --wui-thumbnail-border-base: #252525;

        --wui-wallet-button-bg-base: var(--wui-color-bg-125);

        --w3m-card-embedded-shadow-color: rgb(17 17 18 / 25%);
      }
    `,dark:t.css`
      :root {
        --w3m-color-mix: ${(0,t.unsafeCSS)(r?.["--w3m-color-mix"]||"#000")};
        --w3m-accent: ${(0,t.unsafeCSS)((0,a.getW3mThemeVariables)(r,"light")["--w3m-accent"])};
        --w3m-default: #000;

        --wui-color-modal-bg-base: ${(0,t.unsafeCSS)((0,a.getW3mThemeVariables)(r,"light")["--w3m-background"])};
        --wui-color-accent-base-100: var(--w3m-accent);

        --wui-color-blueberry-100: hsla(231, 100%, 70%, 1);
        --wui-color-blueberry-090: hsla(231, 97%, 72%, 1);
        --wui-color-blueberry-080: hsla(231, 92%, 74%, 1);

        --wui-color-fg-100: #141414;
        --wui-color-fg-125: #2d3131;
        --wui-color-fg-150: #474d4d;
        --wui-color-fg-175: #636d6d;
        --wui-color-fg-200: #798686;
        --wui-color-fg-225: #828f8f;
        --wui-color-fg-250: #8b9797;
        --wui-color-fg-275: #95a0a0;
        --wui-color-fg-300: #9ea9a9;
        --wui-color-fg-325: #9a9a9a;
        --wui-color-fg-350: #d0d0d0;

        --wui-color-bg-100: #ffffff;
        --wui-color-bg-125: #f5fafa;
        --wui-color-bg-150: #f3f8f8;
        --wui-color-bg-175: #eef4f4;
        --wui-color-bg-200: #eaf1f1;
        --wui-color-bg-225: #e5eded;
        --wui-color-bg-250: #e1e9e9;
        --wui-color-bg-275: #dce7e7;
        --wui-color-bg-300: #d8e3e3;
        --wui-color-bg-325: #f3f3f3;
        --wui-color-bg-350: #202020;

        --wui-color-success-base-100: #26b562;
        --wui-color-success-base-125: #30a46b;

        --wui-color-warning-base-100: #f3a13f;

        --wui-color-error-base-100: #f05142;
        --wui-color-error-base-125: #df4a34;

        --wui-color-blue-base-100: rgba(102, 125, 255, 1);
        --wui-color-blue-base-90: rgba(102, 125, 255, 0.9);

        --wui-color-success-glass-001: rgba(38, 181, 98, 0.01);
        --wui-color-success-glass-002: rgba(38, 181, 98, 0.02);
        --wui-color-success-glass-005: rgba(38, 181, 98, 0.05);
        --wui-color-success-glass-010: rgba(38, 181, 98, 0.1);
        --wui-color-success-glass-015: rgba(38, 181, 98, 0.15);
        --wui-color-success-glass-020: rgba(38, 181, 98, 0.2);
        --wui-color-success-glass-025: rgba(38, 181, 98, 0.25);
        --wui-color-success-glass-030: rgba(38, 181, 98, 0.3);
        --wui-color-success-glass-060: rgba(38, 181, 98, 0.6);
        --wui-color-success-glass-080: rgba(38, 181, 98, 0.8);

        --wui-color-success-glass-reown-020: rgba(48, 164, 107, 0.2);

        --wui-color-warning-glass-reown-020: rgba(243, 161, 63, 0.2);

        --wui-color-error-glass-001: rgba(240, 81, 66, 0.01);
        --wui-color-error-glass-002: rgba(240, 81, 66, 0.02);
        --wui-color-error-glass-005: rgba(240, 81, 66, 0.05);
        --wui-color-error-glass-010: rgba(240, 81, 66, 0.1);
        --wui-color-error-glass-015: rgba(240, 81, 66, 0.15);
        --wui-color-error-glass-020: rgba(240, 81, 66, 0.2);
        --wui-color-error-glass-025: rgba(240, 81, 66, 0.25);
        --wui-color-error-glass-030: rgba(240, 81, 66, 0.3);
        --wui-color-error-glass-060: rgba(240, 81, 66, 0.6);
        --wui-color-error-glass-080: rgba(240, 81, 66, 0.8);

        --wui-color-error-glass-reown-020: rgba(223, 74, 52, 0.2);

        --wui-icon-box-bg-error-base-100: #f4dfdd;
        --wui-icon-box-bg-blue-base-100: #d9ecfb;
        --wui-icon-box-bg-success-base-100: #daf0e4;
        --wui-icon-box-bg-inverse-base-100: #dcecfc;

        --wui-all-wallets-bg-100: #e8f1fa;

        --wui-avatar-border-base: #f3f4f4;

        --wui-thumbnail-border-base: #eaefef;

        --wui-wallet-button-bg-base: var(--wui-color-bg-125);

        --wui-color-gray-glass-001: rgba(0, 0, 0, 0.01);
        --wui-color-gray-glass-002: rgba(0, 0, 0, 0.02);
        --wui-color-gray-glass-005: rgba(0, 0, 0, 0.05);
        --wui-color-gray-glass-010: rgba(0, 0, 0, 0.1);
        --wui-color-gray-glass-015: rgba(0, 0, 0, 0.15);
        --wui-color-gray-glass-020: rgba(0, 0, 0, 0.2);
        --wui-color-gray-glass-025: rgba(0, 0, 0, 0.25);
        --wui-color-gray-glass-030: rgba(0, 0, 0, 0.3);
        --wui-color-gray-glass-060: rgba(0, 0, 0, 0.6);
        --wui-color-gray-glass-080: rgba(0, 0, 0, 0.8);
        --wui-color-gray-glass-090: rgba(0, 0, 0, 0.9);

        --wui-color-dark-glass-100: rgba(233, 233, 233, 1);

        --w3m-card-embedded-shadow-color: rgb(224 225 233 / 25%);
      }
    `}}let l=t.css`
  *,
  *::after,
  *::before,
  :host {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-style: normal;
    text-rendering: optimizeSpeed;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-tap-highlight-color: transparent;
    font-family: var(--wui-font-family);
    backface-visibility: hidden;
  }
`,n=t.css`
  button,
  a {
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    transition:
      color var(--wui-duration-lg) var(--wui-ease-out-power-1),
      background-color var(--wui-duration-lg) var(--wui-ease-out-power-1),
      border var(--wui-duration-lg) var(--wui-ease-out-power-1),
      border-radius var(--wui-duration-lg) var(--wui-ease-out-power-1),
      box-shadow var(--wui-duration-lg) var(--wui-ease-out-power-1);
    will-change: background-color, color, border, box-shadow, border-radius;
    outline: none;
    border: none;
    column-gap: var(--wui-spacing-3xs);
    background-color: transparent;
    text-decoration: none;
  }

  wui-flex {
    transition: border-radius var(--wui-duration-lg) var(--wui-ease-out-power-1);
    will-change: border-radius;
  }

  button:disabled > wui-wallet-image,
  button:disabled > wui-all-wallets-image,
  button:disabled > wui-network-image,
  button:disabled > wui-image,
  button:disabled > wui-transaction-visual,
  button:disabled > wui-logo {
    filter: grayscale(1);
  }

  @media (hover: hover) and (pointer: fine) {
    button:hover:enabled {
      background-color: var(--wui-color-gray-glass-005);
    }

    button:active:enabled {
      background-color: var(--wui-color-gray-glass-010);
    }
  }

  button:disabled > wui-icon-box {
    opacity: 0.5;
  }

  input {
    border: none;
    outline: none;
    appearance: none;
  }
`,u=t.css`
  .wui-color-inherit {
    color: var(--wui-color-inherit);
  }

  .wui-color-accent-100 {
    color: var(--wui-color-accent-100);
  }

  .wui-color-error-100 {
    color: var(--wui-color-error-100);
  }

  .wui-color-blue-100 {
    color: var(--wui-color-blue-100);
  }

  .wui-color-blue-90 {
    color: var(--wui-color-blue-90);
  }

  .wui-color-error-125 {
    color: var(--wui-color-error-125);
  }

  .wui-color-success-100 {
    color: var(--wui-color-success-100);
  }

  .wui-color-success-125 {
    color: var(--wui-color-success-125);
  }

  .wui-color-inverse-100 {
    color: var(--wui-color-inverse-100);
  }

  .wui-color-inverse-000 {
    color: var(--wui-color-inverse-000);
  }

  .wui-color-fg-100 {
    color: var(--wui-color-fg-100);
  }

  .wui-color-fg-200 {
    color: var(--wui-color-fg-200);
  }

  .wui-color-fg-300 {
    color: var(--wui-color-fg-300);
  }

  .wui-color-fg-325 {
    color: var(--wui-color-fg-325);
  }

  .wui-color-fg-350 {
    color: var(--wui-color-fg-350);
  }

  .wui-bg-color-inherit {
    background-color: var(--wui-color-inherit);
  }

  .wui-bg-color-blue-100 {
    background-color: var(--wui-color-accent-100);
  }

  .wui-bg-color-error-100 {
    background-color: var(--wui-color-error-100);
  }

  .wui-bg-color-error-125 {
    background-color: var(--wui-color-error-125);
  }

  .wui-bg-color-success-100 {
    background-color: var(--wui-color-success-100);
  }

  .wui-bg-color-success-125 {
    background-color: var(--wui-color-success-100);
  }

  .wui-bg-color-inverse-100 {
    background-color: var(--wui-color-inverse-100);
  }

  .wui-bg-color-inverse-000 {
    background-color: var(--wui-color-inverse-000);
  }

  .wui-bg-color-fg-100 {
    background-color: var(--wui-color-fg-100);
  }

  .wui-bg-color-fg-200 {
    background-color: var(--wui-color-fg-200);
  }

  .wui-bg-color-fg-300 {
    background-color: var(--wui-color-fg-300);
  }

  .wui-color-fg-325 {
    background-color: var(--wui-color-fg-325);
  }

  .wui-color-fg-350 {
    background-color: var(--wui-color-fg-350);
  }
`;r.s(["colorStyles",0,u,"elementStyles",0,n,"initializeTheming",0,function(r,t){o=document.createElement("style"),i=document.createElement("style"),e=document.createElement("style"),o.textContent=c(r).core.cssText,i.textContent=c(r).dark.cssText,e.textContent=c(r).light.cssText,document.head.appendChild(o),document.head.appendChild(i),document.head.appendChild(e),s(t)},"resetStyles",0,l,"setColorTheme",0,s,"setThemeVariables",0,function(r){o&&i&&e&&(o.textContent=c(r).core.cssText,i.textContent=c(r).dark.cssText,e.textContent=c(r).light.cssText)}],758901),r.s([],742560)},328189,r=>{"use strict";r.s(["customElement",0,function(r){return function(o){return"function"==typeof o?(customElements.get(r)||customElements.define(r,o),o):function(r,o){let{kind:i,elements:e}=o;return{kind:i,elements:e,finisher(o){customElements.get(r)||customElements.define(r,o)}}}(r,o)}}])},939750,r=>{"use strict";r.i(588984);var o=r.i(861505),i=r.i(872857);r.i(759703);var e=r.i(392074);r.i(865793);var t=r.i(513002),a=r.i(758901),s=r.i(328189),c=r.i(334736);let l=c.css`
  :host {
    display: inline-flex !important;
  }

  slot {
    width: 100%;
    display: inline-block;
    font-style: normal;
    font-family: var(--wui-font-family);
    font-feature-settings:
      'tnum' on,
      'lnum' on,
      'case' on;
    line-height: 130%;
    font-weight: var(--wui-font-weight-regular);
    overflow: inherit;
    text-overflow: inherit;
    text-align: var(--local-align);
    color: var(--local-color);
  }

  .wui-line-clamp-1 {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
  }

  .wui-line-clamp-2 {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }

  .wui-font-medium-400 {
    font-size: var(--wui-font-size-medium);
    font-weight: var(--wui-font-weight-light);
    letter-spacing: var(--wui-letter-spacing-medium);
  }

  .wui-font-medium-600 {
    font-size: var(--wui-font-size-medium);
    letter-spacing: var(--wui-letter-spacing-medium);
  }

  .wui-font-title-600 {
    font-size: var(--wui-font-size-title);
    letter-spacing: var(--wui-letter-spacing-title);
  }

  .wui-font-title-6-600 {
    font-size: var(--wui-font-size-title-6);
    letter-spacing: var(--wui-letter-spacing-title-6);
  }

  .wui-font-mini-700 {
    font-size: var(--wui-font-size-mini);
    letter-spacing: var(--wui-letter-spacing-mini);
    text-transform: uppercase;
  }

  .wui-font-large-500,
  .wui-font-large-600,
  .wui-font-large-700 {
    font-size: var(--wui-font-size-large);
    letter-spacing: var(--wui-letter-spacing-large);
  }

  .wui-font-2xl-500,
  .wui-font-2xl-600,
  .wui-font-2xl-700 {
    font-size: var(--wui-font-size-2xl);
    letter-spacing: var(--wui-letter-spacing-2xl);
  }

  .wui-font-paragraph-400,
  .wui-font-paragraph-500,
  .wui-font-paragraph-600,
  .wui-font-paragraph-700 {
    font-size: var(--wui-font-size-paragraph);
    letter-spacing: var(--wui-letter-spacing-paragraph);
  }

  .wui-font-small-400,
  .wui-font-small-500,
  .wui-font-small-600 {
    font-size: var(--wui-font-size-small);
    letter-spacing: var(--wui-letter-spacing-small);
  }

  .wui-font-tiny-400,
  .wui-font-tiny-500,
  .wui-font-tiny-600 {
    font-size: var(--wui-font-size-tiny);
    letter-spacing: var(--wui-letter-spacing-tiny);
  }

  .wui-font-micro-700,
  .wui-font-micro-600,
  .wui-font-micro-500 {
    font-size: var(--wui-font-size-micro);
    letter-spacing: var(--wui-letter-spacing-micro);
    text-transform: uppercase;
  }

  .wui-font-tiny-400,
  .wui-font-small-400,
  .wui-font-medium-400,
  .wui-font-paragraph-400 {
    font-weight: var(--wui-font-weight-light);
  }

  .wui-font-large-700,
  .wui-font-paragraph-700,
  .wui-font-micro-700,
  .wui-font-mini-700 {
    font-weight: var(--wui-font-weight-bold);
  }

  .wui-font-medium-600,
  .wui-font-medium-title-600,
  .wui-font-title-6-600,
  .wui-font-large-600,
  .wui-font-paragraph-600,
  .wui-font-small-600,
  .wui-font-tiny-600,
  .wui-font-micro-600 {
    font-weight: var(--wui-font-weight-medium);
  }

  :host([disabled]) {
    opacity: 0.4;
  }
`;var n=function(r,o,i,e){var t,a=arguments.length,s=a<3?o:null===e?e=Object.getOwnPropertyDescriptor(o,i):e;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(r,o,i,e);else for(var c=r.length-1;c>=0;c--)(t=r[c])&&(s=(a<3?t(s):a>3?t(o,i,s):t(o,i))||s);return a>3&&s&&Object.defineProperty(o,i,s),s};let u=class extends o.LitElement{constructor(){super(...arguments),this.variant="paragraph-500",this.color="fg-300",this.align="left",this.lineClamp=void 0}render(){let r={[`wui-font-${this.variant}`]:!0,[`wui-color-${this.color}`]:!0,[`wui-line-clamp-${this.lineClamp}`]:!!this.lineClamp};return this.style.cssText=`
      --local-align: ${this.align};
      --local-color: var(--wui-color-${this.color});
    `,i.html`<slot class=${(0,t.classMap)(r)}></slot>`}};u.styles=[a.resetStyles,l],n([(0,e.property)()],u.prototype,"variant",void 0),n([(0,e.property)()],u.prototype,"color",void 0),n([(0,e.property)()],u.prototype,"align",void 0),n([(0,e.property)()],u.prototype,"lineClamp",void 0),u=n([(0,s.customElement)("wui-text")],u),r.s([],939750)},434704,r=>{"use strict";r.s(["UiHelperUtil",0,{getSpacingStyles:(r,o)=>Array.isArray(r)?r[o]?`var(--wui-spacing-${r[o]})`:void 0:"string"==typeof r?`var(--wui-spacing-${r})`:void 0,getFormattedDate:r=>new Intl.DateTimeFormat("en-US",{month:"short",day:"numeric"}).format(r),getHostName(r){try{return new URL(r).hostname}catch(r){return""}},getTruncateString:({string:r,charsStart:o,charsEnd:i,truncate:e})=>r.length<=o+i?r:"end"===e?`${r.substring(0,o)}...`:"start"===e?`...${r.substring(r.length-i)}`:`${r.substring(0,Math.floor(o))}...${r.substring(r.length-Math.floor(i))}`,generateAvatarColors(r){let o=r.toLowerCase().replace(/^0x/iu,"").replace(/[^a-f0-9]/gu,"").substring(0,6).padEnd(6,"0"),i=this.hexToRgb(o),e=getComputedStyle(document.documentElement).getPropertyValue("--w3m-border-radius-master"),t=100-3*Number(e?.replace("px","")),a=`${t}% ${t}% at 65% 40%`,s=[];for(let r=0;r<5;r+=1){let o=this.tintColor(i,.15*r);s.push(`rgb(${o[0]}, ${o[1]}, ${o[2]})`)}return`
    --local-color-1: ${s[0]};
    --local-color-2: ${s[1]};
    --local-color-3: ${s[2]};
    --local-color-4: ${s[3]};
    --local-color-5: ${s[4]};
    --local-radial-circle: ${a}
   `},hexToRgb(r){let o=parseInt(r,16);return[o>>16&255,o>>8&255,255&o]},tintColor(r,o){let[i,e,t]=r;return[Math.round(i+(255-i)*o),Math.round(e+(255-e)*o),Math.round(t+(255-t)*o)]},isNumber:r=>/^[0-9]+$/u.test(r),getColorTheme:r=>r?r:"u">typeof window&&window.matchMedia&&"function"==typeof window.matchMedia?window.matchMedia("(prefers-color-scheme: dark)")?.matches?"dark":"light":"dark",splitBalance(r){let o=r.split(".");return 2===o.length?[o[0],o[1]]:["0","00"]},roundNumber:(r,o,i)=>r.toString().length>=o?Number(r).toFixed(i):r}])},231502,504471,r=>{"use strict";r.i(588984);var o=r.i(861505),i=r.i(872857);r.i(759703);var e=r.i(392074),t=r.i(758901),a=r.i(434704),s=r.i(328189),c=r.i(334736);let l=c.css`
  :host {
    display: flex;
    width: inherit;
    height: inherit;
  }
`;var n=function(r,o,i,e){var t,a=arguments.length,s=a<3?o:null===e?e=Object.getOwnPropertyDescriptor(o,i):e;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(r,o,i,e);else for(var c=r.length-1;c>=0;c--)(t=r[c])&&(s=(a<3?t(s):a>3?t(o,i,s):t(o,i))||s);return a>3&&s&&Object.defineProperty(o,i,s),s};let u=class extends o.LitElement{render(){return this.style.cssText=`
      flex-direction: ${this.flexDirection};
      flex-wrap: ${this.flexWrap};
      flex-basis: ${this.flexBasis};
      flex-grow: ${this.flexGrow};
      flex-shrink: ${this.flexShrink};
      align-items: ${this.alignItems};
      justify-content: ${this.justifyContent};
      column-gap: ${this.columnGap&&`var(--wui-spacing-${this.columnGap})`};
      row-gap: ${this.rowGap&&`var(--wui-spacing-${this.rowGap})`};
      gap: ${this.gap&&`var(--wui-spacing-${this.gap})`};
      padding-top: ${this.padding&&a.UiHelperUtil.getSpacingStyles(this.padding,0)};
      padding-right: ${this.padding&&a.UiHelperUtil.getSpacingStyles(this.padding,1)};
      padding-bottom: ${this.padding&&a.UiHelperUtil.getSpacingStyles(this.padding,2)};
      padding-left: ${this.padding&&a.UiHelperUtil.getSpacingStyles(this.padding,3)};
      margin-top: ${this.margin&&a.UiHelperUtil.getSpacingStyles(this.margin,0)};
      margin-right: ${this.margin&&a.UiHelperUtil.getSpacingStyles(this.margin,1)};
      margin-bottom: ${this.margin&&a.UiHelperUtil.getSpacingStyles(this.margin,2)};
      margin-left: ${this.margin&&a.UiHelperUtil.getSpacingStyles(this.margin,3)};
    `,i.html`<slot></slot>`}};u.styles=[t.resetStyles,l],n([(0,e.property)()],u.prototype,"flexDirection",void 0),n([(0,e.property)()],u.prototype,"flexWrap",void 0),n([(0,e.property)()],u.prototype,"flexBasis",void 0),n([(0,e.property)()],u.prototype,"flexGrow",void 0),n([(0,e.property)()],u.prototype,"flexShrink",void 0),n([(0,e.property)()],u.prototype,"alignItems",void 0),n([(0,e.property)()],u.prototype,"justifyContent",void 0),n([(0,e.property)()],u.prototype,"columnGap",void 0),n([(0,e.property)()],u.prototype,"rowGap",void 0),n([(0,e.property)()],u.prototype,"gap",void 0),n([(0,e.property)()],u.prototype,"padding",void 0),n([(0,e.property)()],u.prototype,"margin",void 0),u=n([(0,s.customElement)("wui-flex")],u),r.s([],504471),r.s([],231502)},400241,r=>{"use strict";r.i(939750),r.s([])},668236,r=>{"use strict";r.i(588984);var o=r.i(861505),i=r.i(872857);r.i(759703);var e=r.i(392074);r.i(891237);var t=r.i(412088);let a=new class{constructor(){this.cache=new Map}set(r,o){this.cache.set(r,o)}get(r){return this.cache.get(r)}has(r){return this.cache.has(r)}delete(r){this.cache.delete(r)}clear(){this.cache.clear()}};var s=r.i(758901),c=r.i(328189),l=r.i(334736);let n=l.css`
  :host {
    display: flex;
    aspect-ratio: var(--local-aspect-ratio);
    color: var(--local-color);
    width: var(--local-width);
  }

  svg {
    width: inherit;
    height: inherit;
    object-fit: contain;
    object-position: center;
  }

  .fallback {
    width: var(--local-width);
    height: var(--local-height);
  }
`;var u=function(r,o,i,e){var t,a=arguments.length,s=a<3?o:null===e?e=Object.getOwnPropertyDescriptor(o,i):e;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(r,o,i,e);else for(var c=r.length-1;c>=0;c--)(t=r[c])&&(s=(a<3?t(s):a>3?t(o,i,s):t(o,i))||s);return a>3&&s&&Object.defineProperty(o,i,s),s};let w={add:async()=>(await r.A(477319)).addSvg,allWallets:async()=>(await r.A(760196)).allWalletsSvg,arrowBottomCircle:async()=>(await r.A(6559)).arrowBottomCircleSvg,appStore:async()=>(await r.A(321143)).appStoreSvg,apple:async()=>(await r.A(858486)).appleSvg,arrowBottom:async()=>(await r.A(237653)).arrowBottomSvg,arrowLeft:async()=>(await r.A(461747)).arrowLeftSvg,arrowRight:async()=>(await r.A(481396)).arrowRightSvg,arrowTop:async()=>(await r.A(207630)).arrowTopSvg,bank:async()=>(await r.A(994138)).bankSvg,browser:async()=>(await r.A(819062)).browserSvg,bin:async()=>(await r.A(356236)).binSvg,bitcoin:async()=>(await r.A(597987)).bitcoinSvg,card:async()=>(await r.A(863035)).cardSvg,checkmark:async()=>(await r.A(230383)).checkmarkSvg,checkmarkBold:async()=>(await r.A(11463)).checkmarkBoldSvg,chevronBottom:async()=>(await r.A(117637)).chevronBottomSvg,chevronLeft:async()=>(await r.A(234084)).chevronLeftSvg,chevronRight:async()=>(await r.A(774537)).chevronRightSvg,chevronTop:async()=>(await r.A(253991)).chevronTopSvg,chromeStore:async()=>(await r.A(14798)).chromeStoreSvg,clock:async()=>(await r.A(763449)).clockSvg,close:async()=>(await r.A(577305)).closeSvg,compass:async()=>(await r.A(632888)).compassSvg,coinPlaceholder:async()=>(await r.A(342012)).coinPlaceholderSvg,copy:async()=>(await r.A(825943)).copySvg,cursor:async()=>(await r.A(213564)).cursorSvg,cursorTransparent:async()=>(await r.A(672573)).cursorTransparentSvg,circle:async()=>(await r.A(67291)).circleSvg,desktop:async()=>(await r.A(360328)).desktopSvg,disconnect:async()=>(await r.A(953551)).disconnectSvg,discord:async()=>(await r.A(841607)).discordSvg,download:async()=>(await r.A(314163)).downloadSvg,ethereum:async()=>(await r.A(89922)).ethereumSvg,etherscan:async()=>(await r.A(661846)).etherscanSvg,extension:async()=>(await r.A(390835)).extensionSvg,externalLink:async()=>(await r.A(124898)).externalLinkSvg,facebook:async()=>(await r.A(349695)).facebookSvg,farcaster:async()=>(await r.A(751511)).farcasterSvg,filters:async()=>(await r.A(700737)).filtersSvg,github:async()=>(await r.A(112158)).githubSvg,google:async()=>(await r.A(654796)).googleSvg,helpCircle:async()=>(await r.A(608720)).helpCircleSvg,image:async()=>(await r.A(403416)).imageSvg,id:async()=>(await r.A(990712)).idSvg,infoCircle:async()=>(await r.A(614431)).infoCircleSvg,lightbulb:async()=>(await r.A(147689)).lightbulbSvg,mail:async()=>(await r.A(321319)).mailSvg,mobile:async()=>(await r.A(872199)).mobileSvg,more:async()=>(await r.A(495819)).moreSvg,networkPlaceholder:async()=>(await r.A(434070)).networkPlaceholderSvg,nftPlaceholder:async()=>(await r.A(572419)).nftPlaceholderSvg,off:async()=>(await r.A(288)).offSvg,playStore:async()=>(await r.A(442928)).playStoreSvg,plus:async()=>(await r.A(338519)).plusSvg,qrCode:async()=>(await r.A(750654)).qrCodeIcon,recycleHorizontal:async()=>(await r.A(267478)).recycleHorizontalSvg,refresh:async()=>(await r.A(680437)).refreshSvg,search:async()=>(await r.A(709331)).searchSvg,send:async()=>(await r.A(13418)).sendSvg,swapHorizontal:async()=>(await r.A(24287)).swapHorizontalSvg,swapHorizontalMedium:async()=>(await r.A(92187)).swapHorizontalMediumSvg,swapHorizontalBold:async()=>(await r.A(768623)).swapHorizontalBoldSvg,swapHorizontalRoundedBold:async()=>(await r.A(272360)).swapHorizontalRoundedBoldSvg,swapVertical:async()=>(await r.A(635885)).swapVerticalSvg,solana:async()=>(await r.A(413349)).solanaSvg,telegram:async()=>(await r.A(793494)).telegramSvg,threeDots:async()=>(await r.A(854042)).threeDotsSvg,twitch:async()=>(await r.A(364496)).twitchSvg,twitter:async()=>(await r.A(168287)).xSvg,twitterIcon:async()=>(await r.A(169312)).twitterIconSvg,user:async()=>(await r.A(147311)).userSvg,verify:async()=>(await r.A(375950)).verifySvg,verifyFilled:async()=>(await r.A(872245)).verifyFilledSvg,wallet:async()=>(await r.A(466294)).walletSvg,walletConnect:async()=>(await r.A(145475)).walletConnectSvg,walletConnectLightBrown:async()=>(await r.A(145475)).walletConnectLightBrownSvg,walletConnectBrown:async()=>(await r.A(145475)).walletConnectBrownSvg,walletPlaceholder:async()=>(await r.A(352216)).walletPlaceholderSvg,warningCircle:async()=>(await r.A(464636)).warningCircleSvg,x:async()=>(await r.A(168287)).xSvg,info:async()=>(await r.A(9376)).infoSvg,exclamationTriangle:async()=>(await r.A(84284)).exclamationTriangleSvg,reown:async()=>(await r.A(17468)).reownSvg,"x-mark":async()=>(await r.A(114907)).xMarkSvg,dollar:async()=>(await r.A(508571)).dollarSvg};async function g(r){if(a.has(r))return a.get(r);let o=(w[r]??w.copy)();return a.set(r,o),o}let b=class extends o.LitElement{constructor(){super(...arguments),this.size="md",this.name="copy",this.color="fg-300",this.aspectRatio="1 / 1"}render(){return this.style.cssText=`
      --local-color: var(--wui-color-${this.color});
      --local-width: var(--wui-icon-size-${this.size});
      --local-aspect-ratio: ${this.aspectRatio}
    `,i.html`${(0,t.until)(g(this.name),i.html`<div class="fallback"></div>`)}`}};b.styles=[s.resetStyles,s.colorStyles,n],u([(0,e.property)()],b.prototype,"size",void 0),u([(0,e.property)()],b.prototype,"name",void 0),u([(0,e.property)()],b.prototype,"color",void 0),u([(0,e.property)()],b.prototype,"aspectRatio",void 0),b=u([(0,c.customElement)("wui-icon")],b),r.s([],668236)}]);