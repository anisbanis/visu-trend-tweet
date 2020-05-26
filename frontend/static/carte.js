function draw() {
    var canvas=document.getElementById("carte");
    var context=canvas.getContext('2d');
    var image=new Image();
    image.onload=function(){
    context.drawImage(image,0,0,canvas.width,canvas.height);
    };
    image.src="../images/world_map.png";
  }
  
function dess(x,y,ln,lg) {
    var canvas=document.getElementById("carte");
    var context=canvas.getContext('2d');
    var image=new Image();
    image.onload=function(){
    context.drawImage(image,x,y,ln,lg);
    };
    image.src="../images/pos.png";
  }
  
  


 let cal_rad=function(degres){
     return degres / (180/Math.PI)
 }
 let ln=function(x) {
  return Math.log(x) / Math.LN2;
}
 
 let cal_position = function(lat,lon,canvas){
     let x =canvas.width * (lon + 180 ) / (360);
     let y =ln(Math.tan(Math.PI/4 + cal_rad(lat)/2));
     y=canvas.height /2 - canvas.width* y /(2 * Math.PI)
     let dot ={"x":x,"y":y};
     return dot;
 }
 
 let good_dim= function(circle,left,top,widh,height){
   circle.style.top = top +"px"; 
   circle.style.top = left +"px";  
   circle.style.top = width +"px";
   circle.style.top = height +"px";  

 }
 
 let create_point=function(lat,lon,size,canvas){
     let pos=cal_position(lat,lon,canvas);
     var ctx = canvas.getContext('2d');

    dess(pos.x,pos.y, 10,10);

    /*
     let pt=document.createElement("div");
     pt.className="map_point";
     good_dim=(pt,pos.x-size/3,pos.t-size/3,size,size);
     pt.style.lineHeight=pt.style.height;
     pt.innerHTML=size;
     canvas.appendChild(pt);*/
 }

 
 
 let create_points=function(tab){
     
     var canvas=document.getElementById("carte");
     var context=canvas.getContext('2d');
     
     context.translate(-45,55);
     dess(0,0, 10,10);
        
     for (let i=0;i<tab.length;i++){    
         console.log(tab[i][0],tab[i][1]);
         create_point(tab[i][0],tab[i][1],3,canvas)
         console.log(cal_position(tab[i][0],tab[i][1],canvas));     
     }
     
     
 }