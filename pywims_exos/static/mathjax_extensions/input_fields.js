MathJax.Callback.Queue(
MathJax.Hub.Register.StartupHook("TeX Jax Ready",function () {
  var VERSION = "1.0";
  var TEX = MathJax.InputJax.TeX,
      TEXDEF = TEX.Definitions,
      MML = MathJax.ElementJax.mml,
      HTML = MathJax.HTML;
  TEXDEF.macros.inp = "inp";
  TEX.Parse.Augment({
    //  Implements \inp{property: value, ...}{style}
    inp: function (name) {
      var props = this.GetArgument(name);
      var style = this.GetArgument(name);
      var inptype = "input";
      props = props.split(","); style = style.trim();
      for (var i=props.length-1; i>=0; --i) {
          props[i] = props[i].split(":");
          if (props[i].length !== 2) {TEX.Error("Wrong number of arguments in "+name+" for attribute "+props[i][0]); return;}
          props[i][0] = props[i][0].trim(); props[i][1] = props[i][1].trim();
          if (props[i][0] === "type" && props[i][1] === "select") {
             inptype = "select";
             props.splice(i, 1);
          }
          if (props[i][0] === "options") var options = props.splice(i, 1);
      }
      if (inptype === "select" && typeof options === "undefined") {TEX.Error(name+" type=select needs options: |o1|o2|..."); return;}
      if (style.indexOf("position") === -1) {  // if no position is given in style it is now added in order to activate the z-Index
  if (style.charAt(style.length - 1) !== ";") style += ";";
         style += " position:relative;";
      }
      if (style.indexOf("z-index") === -1) {  // if no z-Index is given in style it is now added in order to prevent a covering of input boxes by nearby math
  if (style.charAt(style.length - 1) !== ";") style += ";";
         style += " z-index:5;";
      }
      var input = HTML.Element(inptype);
      for (var i=0, j=props.length; i < j; ++i) input.setAttribute(props[i][0], props[i][1]);
      input.setAttribute("style", style);
      input.setAttribute("xmlns","http://www.w3.org/1999/xhtml");
      if (inptype === "select") {
         options = options[0][1].split(options[0][1].substr(0, 1));
         options[0] = 'Please select';
         for (i=0; i<options.length; ++i) {
             var opt = document.createElement("option");
             if (i>0) opt.value = i; else opt.value = "";
             var opttext = document.createTextNode(options[i].trim());
             opt.appendChild(opttext);
             input.appendChild(opt);
         }
      }
      var mml = MML["annotation-xml"](MML.xml(input)).With({encoding:"application/xhtml+xml",isToken:true});
      this.Push(MML.semantics(mml));
    }
  });
 
}));
MathJax.Ajax.loadComplete("[Extra]/input_fields.js");


