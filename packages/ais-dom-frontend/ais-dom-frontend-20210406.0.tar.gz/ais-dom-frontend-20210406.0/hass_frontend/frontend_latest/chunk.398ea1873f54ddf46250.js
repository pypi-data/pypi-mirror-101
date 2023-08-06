(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[854],{32205:(e,i,t)=>{"use strict";t.r(i),t.d(i,{AddMediaSourceAisWs:()=>y,HuiDialogAddMediaSourceAis:()=>v});t(53918),t(36051),t(81689),t(53973),t(84281),t(27662),t(30879);var a=t(15652),r=(t(31206),t(88324),t(43709),t(34821)),n=t(11654),o=t(26765),s=t(47181);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,i){["method","field"].forEach((function(t){i.forEach((function(i){i.kind===t&&"own"===i.placement&&this.defineClassElement(e,i)}),this)}),this)},initializeClassElements:function(e,i){var t=e.prototype;["method","field"].forEach((function(a){i.forEach((function(i){var r=i.placement;if(i.kind===a&&("static"===r||"prototype"===r)){var n="static"===r?e:t;this.defineClassElement(n,i)}}),this)}),this)},defineClassElement:function(e,i){var t=i.descriptor;if("field"===i.kind){var a=i.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,i.key,t)},decorateClass:function(e,i){var t=[],a=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!h(e))return t.push(e);var i=this.decorateElement(e,r);t.push(i.element),t.push.apply(t,i.extras),a.push.apply(a,i.finishers)}),this),!i)return{elements:t,finishers:a};var n=this.decorateConstructor(t,i);return a.push.apply(a,n.finishers),n.finishers=a,n},addElementPlacement:function(e,i,t){var a=i[e.placement];if(!t&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,i){for(var t=[],a=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=i[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),d=this.toElementFinisherExtras((0,r[n])(s)||s);e=d.element,this.addElementPlacement(e,i),d.finisher&&a.push(d.finisher);var l=d.extras;if(l){for(var c=0;c<l.length;c++)this.addElementPlacement(l[c],i);t.push.apply(t,l)}}return{element:e,finishers:a,extras:t}},decorateConstructor:function(e,i){for(var t=[],a=i.length-1;a>=0;a--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,i[a])(r)||r);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:t}},fromElementDescriptor:function(e){var i={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(i,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(i.initializer=e.initializer),i},toElementDescriptors:function(e){var i;if(void 0!==e)return(i=e,function(e){if(Array.isArray(e))return e}(i)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(i)||function(e,i){if(e){if("string"==typeof e)return f(e,i);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?f(e,i):void 0}}(i)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var i=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),i}),this)},toElementDescriptor:function(e){var i=String(e.kind);if("method"!==i&&"field"!==i)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+i+'"');var t=u(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:i,key:t,placement:a,descriptor:Object.assign({},r)};return"field"!==i?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var i={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(i,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),i},toClassDescriptor:function(e){var i=String(e.kind);if("class"!==i)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+i+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var t=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:t}},runClassFinishers:function(e,i){for(var t=0;t<i.length;t++){var a=(0,i[t])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,i,t){if(void 0!==e[i])throw new TypeError(t+" can't have a ."+i+" property.")}};return e}function l(e){var i,t=u(e.key);"method"===e.kind?i={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?i={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?i={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(i={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:t,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:i};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function c(e,i){void 0!==e.descriptor.get?i.descriptor.get=e.descriptor.get:i.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,i){var t=e[i];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+i+"' to be a function");return t}function u(e){var i=function(e,i){if("object"!=typeof e||null===e)return e;var t=e[Symbol.toPrimitive];if(void 0!==t){var a=t.call(e,i||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===i?String:Number)(e)}(e,"string");return"symbol"==typeof i?i:String(i)}function f(e,i){(null==i||i>e.length)&&(i=e.length);for(var t=0,a=new Array(i);t<i;t++)a[t]=e[t];return a}const y=(e,i,t,a,r,n,o)=>e.callWS({type:"ais_cloud/add_ais_media_source",mediaCategory:i,mediaName:t,mediaType:a,mediaStreamUrl:r,mediaImageUrl:n,mediaShare:o});let v=function(e,i,t,a){var r=d();if(a)for(var n=0;n<a.length;n++)r=a[n](r);var o=i((function(e){r.initializeInstanceElements(e,s.elements)}),t),s=r.decorateClass(function(e){for(var i=[],t=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},a=0;a<e.length;a++){var r,n=e[a];if("method"===n.kind&&(r=i.find(t)))if(m(n.descriptor)||m(r.descriptor)){if(h(n)||h(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(h(n)){if(h(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}c(n,r)}else i.push(n)}return i}(o.d.map(l)),e);return r.initializeClassElements(o.F,s.elements),r.runClassFinishers(o.F,s.finishers)}([(0,a.Mo)("hui-dialog-add-media-source-ais")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1}),(0,a.sz)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,a.sz)()],key:"_opened",value:()=>!1},{kind:"field",decorators:[(0,a.sz)()],key:"mediaCategory",value:()=>"radio"},{kind:"field",decorators:[(0,a.sz)()],key:"mediaName",value:()=>""},{kind:"field",decorators:[(0,a.sz)()],key:"mediaType",value:()=>""},{kind:"field",decorators:[(0,a.sz)()],key:"mediaStreamUrl",value:()=>""},{kind:"field",decorators:[(0,a.sz)()],key:"mediaImageUrl",value:()=>""},{kind:"field",decorators:[(0,a.sz)()],key:"mediaShare",value:()=>!1},{kind:"field",decorators:[(0,a.sz)()],key:"mediaChips",value:()=>[]},{kind:"field",key:"_params",value:void 0},{kind:"field",key:"_aisMediaInfo",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._opened=!0,this._params=e,this._aisMediaInfo=this.hass.states["media_player.wbudowany_glosnik"],this.mediaCategory="radio",this.mediaName="",this.mediaType="",this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id?this.mediaStreamUrl=this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id:this.mediaStreamUrl="",this.mediaImageUrl="",this.mediaShare=!1,this.mediaChips=[];this.hass.states["input_select.radio_type"].attributes.options.forEach((e=>{e.startsWith("Moje")||e.startsWith("Udostępnione")||this.mediaChips.push(e)}))}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._opened=!1,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return a.dy`
      <ha-dialog
        .open=${this._opened}
        hideActions
        .heading=${(0,r.i)(this.hass,"Dodaj nowe Multimedia do biblioteki")}
        @closed=${this.closeDialog}
      >
        ${this._loading?a.dy`<ha-circular-progress active></ha-circular-progress>`:a.dy`<p>
                ${this._isAudioPlaying()&&!this._loading?a.dy`
                  <span class="aisUrl">
                    Odtwarzasz z URL, <ha-icon icon="mdi:web"></ha-icon>:
                    <b></b>${this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id}</b>
                    <br/>ten adres został wypełniony automatycznie - sprawdź czy się zgadza.
                    </span
                  >
                  `:a.dy`
                      Obecnie na wbudowanym odtwarzaczu nie odtwarzasz żadnych
                      mediów. Sugerujemy sprawdzenie działania mediów na
                      odtwarzaczu przed ich dodaniem.
                    `}
              </p>

              <label>
                Typ audio:
              </label>
              <paper-radio-group
                .selected=${this.mediaCategory}
                .value=${this.mediaCategory}
                @selected-changed=${this._mediaCategoryChanged}
              >
                <paper-radio-button name="radio">
                  <ha-icon icon="mdi:radio"></ha-icon>
                </paper-radio-button>

                <paper-radio-button name="podcast">
                  <ha-icon icon="mdi:podcast"></ha-icon>
                </paper-radio-button>
                <paper-radio-button name="audiobook">
                  <ha-icon icon="mdi:book-music"></ha-icon>
                </paper-radio-button>
                <paper-radio-button name="music">
                  <ha-icon icon="mdi:music"></ha-icon>
                </paper-radio-button>
              </paper-radio-group>
              <br />
              ${"radio"===this.mediaCategory?a.dy`
                    <paper-input
                      placeholder="Nazwa (komenda: Włącz radio nazwa)"
                      type="text"
                      value=${this.mediaName}
                      id="audio_name"
                      @value-changed=${this._mediaNameChanged}
                    >
                      <ha-icon icon="mdi:account-voice" slot="suffix"></ha-icon>
                    </paper-input>

                    <paper-input
                      placeholder="Typ radia"
                      type="text"
                      value=${this.mediaType}
                      id="audio_category"
                      @value-changed=${this._mediaTypeChanged}
                    >
                      <ha-icon
                        icon="mdi:format-list-bulleted-type"
                        slot="suffix"
                      ></ha-icon>
                    </paper-input>
                    <ha-chip
                      @chip-clicked=${this._mediaTypePicket}
                      .items=${this.mediaChips}
                    >
                    </ha-chip>
                    <paper-input
                      placeholder="Adres URL Strumienia"
                      type="text"
                      value=${this.mediaStreamUrl}
                      @value-changed=${this._mediaStreamUrlChanged}
                    >
                      <ha-icon icon="mdi:play-network" slot="suffix"></ha-icon>
                    </paper-input>

                    <paper-input
                      placeholder="Adres URL Okładki"
                      type="text"
                      value=${this.mediaImageUrl}
                      @value-changed=${this._mediaImageUrlChanged}
                    >
                      <ha-icon icon="mdi:image-edit" slot="suffix"></ha-icon>
                    </paper-input>
                    <br />
                    <div style="text-align:center;">
                      <ha-icon icon="mdi:share-variant"></ha-icon>
                      <ha-switch
                        .checked=${this.mediaShare}
                        @change=${this._mediaShareChanged}
                      >
                      </ha-switch>
                      Udostępnij dla wszystkich (po sprawdzeniu w AIS)
                      <br /><br />
                    </div>
                    ${this._canSourceBeAdded()?a.dy` <div class="sourceCheckButton">
                            <mwc-button raised @click=${this._handleAddMedia}>
                              <ha-icon icon="hass:music-note-plus"></ha-icon>
                              ${this.mediaShare?a.dy`Dodaj do swojej biblioteki i udostępnij
                                  dla wszystkich`:a.dy` Dodaj do swojej biblioteki `}
                            </mwc-button>
                          </div>
                          <br />`:a.dy`
                          <div style="text-align: center;">
                            <h2>
                              Wypełnij wszsytkie wymagane pola.
                            </h2>
                          </div>
                          <br />
                        `}
                  `:a.dy`<div class="WorkInProgress">
                      <img src="/static/ais_work_in_progress.png" />
                    </div>
                    <div class="AisGithub">
                      <a href="https://github.com/sviete" target="_blank"
                        ><ha-icon icon="hass:github"></ha-icon> Join AI-Speaker
                        on Github</a
                      >
                    </div>
                    <br />`} `}
      </ha-dialog>
    `}},{kind:"method",key:"_addMediaToAis",value:async function(){this._loading=!0;let e={message:"",error:!1};try{e=await y(this.hass,this.mediaCategory,this.mediaName,this.mediaType,this.mediaStreamUrl,this.mediaImageUrl,this.mediaShare)}catch{this._loading=!1}return this._loading=!1,e}},{kind:"method",key:"_handleAddMedia",value:async function(){const e=await this._addMediaToAis();if(e.error)return void await(0,o.Ys)(this,{title:"AIS",text:e.message});await(0,o.g7)(this,{title:"AIS",text:e.message+" Czy chcesz dodać kolejne media?",confirmText:"TAK",dismissText:"NIE"})?(this.mediaCategory="radio",this.mediaName="",this.mediaType="",this.mediaStreamUrl="",this.mediaImageUrl="",this.mediaShare=!1):this.closeDialog()}},{kind:"method",key:"_isAudioPlaying",value:function(){var e;return!!(null===(e=this._aisMediaInfo)||void 0===e?void 0:e.attributes.media_content_id)}},{kind:"method",key:"_canSourceBeAdded",value:function(){return!(this.mediaName.length<3)&&(!(this.mediaType.length<3)&&!(this.mediaStreamUrl.length<10))}},{kind:"method",key:"_mediaCategoryChanged",value:function(e){const i=e.detail.value;i!==this.mediaCategory&&(this.mediaCategory=i)}},{kind:"method",key:"_mediaTypeChanged",value:function(e){const i=e.detail.value;i!==this.mediaType&&(this.mediaType=i)}},{kind:"method",key:"_mediaTypePicket",value:function(e){const i=e.detail.index,t=this.mediaChips[i];t!==this.mediaType&&(this.mediaType=t)}},{kind:"method",key:"_mediaStreamUrlChanged",value:function(e){const i=e.detail.value;i!==this.mediaStreamUrl&&(this.mediaStreamUrl=i)}},{kind:"method",key:"_mediaImageUrlChanged",value:function(e){const i=e.detail.value;i!==this.mediaImageUrl&&(this.mediaImageUrl=i)}},{kind:"method",key:"_mediaShareChanged",value:function(e){const i=e.target.checked;i!==this.mediaShare&&(this.mediaShare=i)}},{kind:"method",key:"_mediaNameChanged",value:function(e){const i=e.detail.value;i!==this.mediaName&&(this.mediaName=i)}},{kind:"get",static:!0,key:"styles",value:function(){return[n.yu,a.iv`
        ha-dialog {
          --dialog-content-padding: 0 24px 20px;
        }
        div.sourceCheckButton {
          text-align: center;
        }
        div.WorkInProgress {
          text-align: center;
        }
        div.AisGithub {
          text-align: right;
        }
        img {
          max-width: 500px;
          max-height: 300px;
        }
        span.aisUrl {
          word-wrap: break-word;
        }
        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin-top: 40px;
        }
      `]}}]}}),a.oi)}}]);
//# sourceMappingURL=chunk.398ea1873f54ddf46250.js.map