webpackJsonp([0],{j7e0:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r=s("7+uW"),n=s("yPE/"),i=s.n(n),a=s("G0J2"),o=s.n(a);r.default.use(o.a);var l=i.a.import("parchment"),c=new l.Attributor.Class("box","line",{scope:l.Scope.INLINE,whitelist:["error","suggest"]});i.a.register(c);var u={data:function(){return{paperOn:!1,showESpelling:!0,showEGrammar:!0,showESemantic:!0,showSSemantic:!0,showSStructure:!0,paperTitle:"",paperBody:"",errorSpelling:"",errorGrammar:"",errorSemantic:"",suggestSemantic:"",suggestStructure:"",sumNum:"",judgeAdd:"",errorSpellingArr:[],errorSpellingPosL:[],errorSpellingPosR:[],errorSpellingRight:[],errorSpellingExplain:[],errorGrammarArr:[],errorGrammarPosL:[],errorGrammarPosR:[],errorGrammarRight:[],errorGrammarExplain:[],errorSemanticArr:[],errorSemanticPosL:[],errorSemanticPosR:[],errorSemanticRight:[],errorSemanticExplain:[],suggestSemanticArr:[],suggestSemanticPosL:[],suggestSemanticPosR:[],suggestSemanticRight:[],suggestSemanticExplain:[],suggestStructureArr:[],suggestStructurePosL:[],suggestStructurePosR:[],suggestStructureRight:[],suggestStructureExplain:[],titleContent:"",bodyContent:"",bodyContentArray:[],spanArray:[],spanString:"",htmlContent:"",titleEditorOption:{theme:"bubble",placeholder:"PASTE TITLE",modules:{}},bodyEditorOption:{theme:"bubble",placeholder:"PASTE PAPER",modules:{}}}},mounted:function(){this.changeHtml()},methods:{changeMS:function(){document.getElementById("mistakes-spelling").style.backgroundColor="#eaeaea";var t=document.getElementById("mistakes-spelling-circle");t&&(t.style.backgroundColor="#ef4632");var e=document.getElementById("mistakes-spelling-num");e&&(e.style.color="white")},returnMS:function(){document.getElementById("mistakes-spelling").style.backgroundColor="white";var t=document.getElementById("mistakes-spelling-circle");t&&(t.style.backgroundColor="#ededed");var e=document.getElementById("mistakes-spelling-num");e&&(e.style.color="#898989")},changeMG:function(){document.getElementById("mistakes-grammar").style.backgroundColor="#eaeaea";var t=document.getElementById("mistakes-grammar-circle");t&&(t.style.backgroundColor="#ef4632");var e=document.getElementById("mistakes-grammar-num");e&&(e.style.color="white")},returnMG:function(){document.getElementById("mistakes-grammar").style.backgroundColor="white";var t=document.getElementById("mistakes-grammar-circle");t&&(t.style.backgroundColor="#ededed");var e=document.getElementById("mistakes-grammar-num");e&&(e.style.color="#898989")},changeML:function(){document.getElementById("mistakes-lexeme").style.backgroundColor="#eaeaea";var t=document.getElementById("mistakes-lexeme-circle");t&&(t.style.backgroundColor="#ef4632");var e=document.getElementById("mistakes-lexeme-num");e&&(e.style.color="white")},returnML:function(){document.getElementById("mistakes-lexeme").style.backgroundColor="white";var t=document.getElementById("mistakes-lexeme-circle");t&&(t.style.backgroundColor="#ededed");var e=document.getElementById("mistakes-lexeme-num");e&&(e.style.color="#898989")},changeSL:function(){document.getElementById("suggestions-lexeme").style.backgroundColor="#eaeaea";var t=document.getElementById("suggestions-lexeme-circle");t&&(t.style.backgroundColor="#ef4632");var e=document.getElementById("suggestions-lexeme-num");e&&(e.style.color="white")},returnSL:function(){document.getElementById("suggestions-lexeme").style.backgroundColor="white";var t=document.getElementById("suggestions-lexeme-circle");t&&(t.style.backgroundColor="#ededed");var e=document.getElementById("suggestions-lexeme-num");e&&(e.style.color="#898989")},changeSS:function(){document.getElementById("suggestions-structure").style.backgroundColor="#eaeaea";var t=document.getElementById("suggestion-structure-circle");t&&(t.style.backgroundColor="#ef4632");var e=document.getElementById("suggestion-structure-num");e&&(e.style.color="white")},returnSS:function(){document.getElementById("suggestions-structure").style.backgroundColor="white";var t=document.getElementById("suggestion-structure-circle");t&&(t.style.backgroundColor="#ededed");var e=document.getElementById("suggestion-structure-num");e&&(e.style.color="#898989")},changeHtml:function(){var t=this;setInterval(function(){if(t.editor.container.firstChild.innerText.trim()!=t.htmlContent.trim()&&""!=t.editor.container.firstChild.innerText.trim()){console.log("1",t.htmlContent.trim()),console.log("2",t.editor.container.firstChild.innerText.trim());var e=t.editor.container.firstChild.innerText.trim();t.$http.post("/api/num",{paperBody:t.editor.getText()}).then(function(s){if(s.body.success){var r=function(t,e,s){return t.substring(0,e)+s+t.substring(e,t.length)},n=t.editor.getText();t.paperOn=!0,t.errorSpelling=s.body.count.errorSpelling,t.errorGrammar=s.body.count.errorGrammar,t.errorSemantic=s.body.count.errorSemantic,t.suggestSemantic=s.body.count.suggestSemantic,t.suggestStructure=s.body.count.suggestStructure,t.sumNum=s.body.count.sumNum,t.errorSpellingArr=s.body.spelling.err,t.errorGrammarArr=s.body.grammar.err,t.errorSemanticArr=s.body.semantic.err,t.suggestSemanticArr=s.body.semantic.sug,t.suggestStructureArr=s.body.structure.sug;var i=[];[t.errorSpellingArr,t.errorGrammarArr,t.errorSemanticArr,t.suggestSemanticArr,t.suggestStructureArr].forEach(function(t){t.forEach(function(t){if(t.end)for(var e=0;e<t.end.length;e++)i.push({start:t.start[e],end:t.end[e],type:t.type})})}),i.sort(function(t,e){return t.end<e.end}),i.forEach(function(t){1==t.type?(n=r(n,t.end,"</span>"),n=r(n,t.start,'<span class="line-error">')):(n=r(n,t.end,"</span>"),n=r(n,t.start,'<span class="line-suggest">'))}),t.cursorIndex=t.editor.getSelection().index,t.changeEditor(n),t.editor.setSelection(t.cursorIndex,0),t.htmlContent=e}})}},3e3)},toShowAll:function(){this.showESpelling=!0,this.showEGrammar=!0,this.showESemantic=!0,this.showSSemantic=!0,this.showSStructure=!0},toShowMistake:function(){this.showESpelling=!0,this.showEGrammar=!0,this.showESemantic=!0,this.showSSemantic=!1,this.showSStructure=!1},toShowESpelling:function(){this.showESpelling=!0,this.showEGrammar=!1,this.showESemantic=!1,this.showSSemantic=!1,this.showSStructure=!1},toShowEGrammar:function(){this.showESpelling=!1,this.showEGrammar=!0,this.showESemantic=!1,this.showSSemantic=!1,this.showSStructure=!1},toShowESemantic:function(){this.showESpelling=!1,this.showEGrammar=!1,this.showESemantic=!0,this.showSSemantic=!1,this.showSStructure=!1},toShowSSemantic:function(){this.showESpelling=!1,this.showEGrammar=!1,this.showESemantic=!1,this.showSSemantic=!0,this.showSStructure=!1},toShowSStructure:function(){this.showESpelling=!1,this.showEGrammar=!1,this.showESemantic=!1,this.showSSemantic=!1,this.showSStructure=!0},addErrorSpellingTag:function(t,e,s){this.bodyContentArray=s.replace(/(.)(?=[^$])/g,"$1,").split(",");for(var r=t;r<=e;r++)this.spanArray.push(this.bodyContentArray[r]);var n=this.spanArray.join(""),i=this.bodyContentArray.join("");""==this.spanString?this.spanString=i.replace(n,function(t){return'<span class="line-spellingError">'+t+"</span>"}):this.spanString=this.spanString.replace(n,function(t){return'<span class="line-spellingError">'+t+"</span>"}),this.spanArray.splice(0,this.spanArray.length),console.log(this.spanString)},addErrorGrammarTag:function(t,e,s){this.bodyContentArray=s.replace(/(.)(?=[^$])/g,"$1,").split(",");for(var r=t;r<=e;r++)this.spanArray.push(this.bodyContentArray[r]);var n=this.spanArray.join(""),i=this.bodyContentArray.join("");""==this.spanString?this.spanString=i.replace(n,function(t){return'<span class="line-grammarError">'+t+"</span>"}):this.spanString=this.spanString.replace(n,function(t){return'<span class="line-grammarError">'+t+"</span>"}),this.spanArray.splice(0,this.spanArray.length),console.log(this.spanString)},addErrorLexemeTag:function(t,e,s){this.bodyContentArray=s.replace(/(.)(?=[^$])/g,"$1,").split(",");for(var r=t;r<=e;r++)this.spanArray.push(this.bodyContentArray[r]);var n=this.spanArray.join(""),i=this.bodyContentArray.join("");""==this.spanString?this.spanString=i.replace(n,function(t){return'<span class="line-semanticError">'+t+"</span>"}):this.spanString=this.spanString.replace(n,function(t){return'<span class="line-semanticError">'+t+"</span>"}),this.spanArray.splice(0,this.spanArray.length),console.log(this.spanString)},addSuggestLexemeTag:function(t,e,s){this.bodyContentArray=s.replace(/(.)(?=[^$])/g,"$1,").split(",");for(var r=t;r<=e;r++)this.spanArray.push(this.bodyContentArray[r]);var n=this.spanArray.join(""),i=this.bodyContentArray.join("");""==this.spanString?this.spanString=i.replace(n,function(t){return'<span class="line-semanticSuggest">'+t+"</span>"}):this.spanString=this.spanString.replace(n,function(t){return'<span class="line-semanticSuggest">'+t+"</span>"}),this.spanArray.splice(0,this.spanArray.length),console.log(this.spanString)},addSuggestStructureTag:function(t,e,s){this.bodyContentArray=s.replace(/(.)(?=[^$])/g,"$1,").split(",");for(var r=t;r<=e;r++)this.spanArray.push(this.bodyContentArray[r]);var n=this.spanArray.join(""),i=this.bodyContentArray.join("");""==this.spanString?this.spanString=i.replace(n,function(t){return'<span class="line-structureSuggest">'+t+"</span>"}):this.spanString=this.spanString.replace(n,function(t){return'<span class="line-structureSuggest">'+t+"</span>"}),this.spanArray.splice(0,this.spanArray.length),console.log(this.spanString)},changeEditor:function(t){0===t.trim().length?this.htmlContent=t:this.htmlContent="<p>"+t+"</p>",console.log("htmlContent",this.htmlContent);var e=this.editor.getLength();this.editor.deleteText(0,e-1),this.editor.clipboard.dangerouslyPasteHTML(0,this.htmlContent)}},created:function(){},computed:{editor:function(){return this.$refs.myTextEditor.quill}}},m={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"base"},[s("div",{staticClass:"topper"}),t._v(" "),s("div",{staticClass:"left"},[s("div",{staticClass:"reload"},[s("img",{staticClass:"reload-img",attrs:{src:"/static/img/reload.png",onclick:"reloadPaper()"}}),t._v(" "),s("span",{staticClass:"reload-num"},[t._v(t._s(t.sumNum))])]),t._v(" "),s("div",{staticClass:"clear-float"}),t._v(" "),s("div",{staticClass:"show-all",on:{click:function(e){t.toShowAll()}}},[s("div",{staticClass:"show-all-circle"}),t._v(" "),s("span",{staticClass:"show-all-title"},[t._v("SHOW ALL")])]),t._v(" "),s("div",{staticClass:"clear-float"}),t._v(" "),s("div",{staticClass:"mistakes"},[s("div",{staticClass:"mistakes-circle"}),t._v(" "),s("span",{staticClass:"mistakes-title"},[t._v("MISTAKES")]),t._v(" "),s("ul",{staticClass:"mistakes-list"},[s("li",{attrs:{id:"mistakes-spelling"},on:{mouseover:function(e){t.changeMS()},mouseout:function(e){t.returnMS()},click:function(e){t.toShowESpelling()}}},[s("span",{staticClass:"list-title"},[t._v("SPELLING")]),t._v(" "),t.paperOn?s("div",{attrs:{id:"mistakes-spelling-circle"}},[s("span",{attrs:{id:"mistakes-spelling-num"}},[t._v(t._s(t.errorSpelling))])]):t._e(),t._v(" "),s("div",{staticClass:"clear-float"})]),t._v(" "),s("li",{attrs:{id:"mistakes-grammar"},on:{mouseover:function(e){t.changeMG()},mouseout:function(e){t.returnMG()},click:function(e){t.toShowEGrammar()}}},[s("span",{staticClass:"list-title"},[t._v("GRAMMAR")]),t._v(" "),t.paperOn?s("div",{attrs:{id:"mistakes-grammar-circle"}},[s("span",{attrs:{id:"mistakes-grammar-num"}},[t._v(t._s(t.errorGrammar))])]):t._e(),t._v(" "),s("div",{staticClass:"clear-float"})]),t._v(" "),s("li",{attrs:{id:"mistakes-lexeme"},on:{mouseover:function(e){t.changeML()},mouseout:function(e){t.returnML()},click:function(e){t.toShowESemantic()}}},[s("span",{staticClass:"list-title"},[t._v("SEMANTIC")]),t._v(" "),t.paperOn?s("div",{attrs:{id:"mistakes-lexeme-circle"}},[s("span",{attrs:{id:"mistakes-lexeme-num"}},[t._v(t._s(t.errorSemantic))])]):t._e(),t._v(" "),s("div",{staticClass:"clear-float"})])])]),t._v(" "),s("div",{staticClass:"clear-float"}),t._v(" "),s("div",{staticClass:"suggestions"},[s("div",{staticClass:"suggestions-circle"}),t._v(" "),s("span",{staticClass:"suggestions-title"},[t._v("SUGGESTIONS")]),t._v(" "),s("ul",{staticClass:"suggestions-list"},[s("li",{attrs:{id:"suggestions-lexeme"},on:{mouseover:function(e){t.changeSL()},mouseout:function(e){t.returnSL()},click:function(e){t.toShowSSemantic()}}},[s("span",{staticClass:"list-title"},[t._v("SEMANTIC")]),t._v(" "),t.paperOn?s("div",{attrs:{id:"suggestions-lexeme-circle"}},[s("span",{attrs:{id:"suggestions-lexeme-num"}},[t._v(t._s(t.suggestSemantic))])]):t._e(),t._v(" "),s("div",{staticClass:"clear-float"})]),t._v(" "),s("li",{attrs:{id:"suggestions-structure"},on:{mouseover:function(e){t.changeSS()},mouseout:function(e){t.returnSS()},click:function(e){t.toShowSStructure()}}},[s("span",{staticClass:"list-title"},[t._v("SENTENCE STRUCTURE")]),t._v(" "),t.paperOn?s("div",{attrs:{id:"suggestion-structure-circle"}},[s("span",{attrs:{id:"suggestion-structure-num"}},[t._v(t._s(t.suggestStructure))])]):t._e(),t._v(" "),s("div",{staticClass:"clear-float"})])])]),t._v(" "),s("div",{staticClass:"clear-float"}),t._v(" "),t._m(0)]),t._v(" "),s("div",{staticClass:"splender-left"}),t._v(" "),s("div",{staticClass:"middle"},[s("quill-editor",{ref:"myTextEditor",staticClass:"title-paste",attrs:{content:t.titleContent,options:t.titleEditorOption}}),t._v(" "),s("quill-editor",{ref:"myTextEditor",staticClass:"body-paste",attrs:{content:t.bodyContent,options:t.bodyEditorOption}})],1),t._v(" "),s("div",{staticClass:"splender-right"}),t._v(" "),s("div",{staticClass:"right"},[s("el-collapse",{attrs:{accordion:""}},[t._l(t.errorSpellingArr,function(e,r){return t.showESpelling?s("el-collapse-item",{key:r},[s("template",{slot:"title"},[s("li",{staticClass:"right-spelling"},[t._v(t._s(e.rep))])]),t._v(" "),s("div",{staticClass:"es-second-floor"},[s("span",[t._v(t._s(e.exp))])])],2):t._e()}),t._v(" "),t._l(t.errorGrammarArr,function(e,r){return t.showEGrammar?s("el-collapse-item",{key:r},[s("template",{slot:"title"},[s("li",{staticClass:"right-grammar"},[t._v(t._s(e.rep))])]),t._v(" "),s("div",{staticClass:"eg-second-floor"},[s("span",[t._v(t._s(e.exp))])])],2):t._e()}),t._v(" "),t._l(t.errorSemanticArr,function(e,r){return t.showESemantic?s("el-collapse-item",{key:r},[s("template",{slot:"title"},[s("li",{staticClass:"right-semantic"},[t._v(t._s(e.rep))])]),t._v(" "),s("div",{staticClass:"ese-second-floor"},[s("span",[t._v(t._s(e.exp))])])],2):t._e()}),t._v(" "),t._l(t.suggestSemanticArr,function(e,r){return t.showSSemantic?s("el-collapse-item",{key:r},[s("template",{slot:"title"},[s("li",{staticClass:"suggest-semantic"},[t._v(t._s(e.rep))])]),t._v(" "),s("div",{staticClass:"ss-second-floor"},[s("span",[t._v(t._s(e.exp))])])],2):t._e()}),t._v(" "),t._l(t.suggestStructureArr,function(e,r){return t.showSStructure?s("el-collapse-item",{key:r},[s("template",{slot:"title"},[s("li",{staticClass:"suggest-structure"},[t._v(t._s(e.rep))])]),t._v(" "),s("div",{staticClass:"sst-second-floor"},[s("span",[t._v(t._s(e.exp))])])],2):t._e()})],2)],1)])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"advanced-issues"},[e("img",{staticClass:"advanced-issues-img",attrs:{src:"/static/img/more.png"}}),this._v(" "),e("span",{staticClass:"advanced-issues-title"},[this._v("ADVANCED ISSUES")])])}]};var g=s("VU/8")(u,m,!1,function(t){s("khA+")},null,null);e.default=g.exports},"khA+":function(t,e){}});
//# sourceMappingURL=0.8ded49b1703870a425a0.js.map