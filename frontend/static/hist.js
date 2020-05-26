var cpt=0;
function histogramme(y,x,ny,nx,id) {
				var canvas = document.getElementById(id);
				var context = canvas.getContext('2d');
		  	


				
			  
				// Origine du repère
				if(cpt ==0){context.translate(32,350);cpt++;}
				// restorer un contexte vide 
				context.save();
        context.setTransform(1, 0, 0, 1, 0, 0);
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.restore();
        
				var x0 = 0;
				var y0 = 0;
				
				var largeur_barre = 45;
				context.lineWidth = '1.0';
				
				// Couleur et largeur du trait
				context.fillStyle = '#000';
				context.lineWidth = '1.0';
				
				// Axe des ordonnées
				tracer (context,x0,y0,x0,-310);
				// Flèche
				tracer (context,x0-8,-300+3,x0,-300-10);
				tracer (context,x0+8,-300+3,x0,-300-10);
				
				context.textAlign = 'center';
				context.font = '9pt Tahoma';
				var graduation = 0;
				var pas = Math.trunc(Math.max(...y)/14)+1;
				console.log("ss");
				console.log(pas);
				console.log(Math.max(y));
				console.log(pas);
				
				for (var i=0; i<15; i++) {
					tracer (context,x0-3,y0-20*(i),x0+3,y0-20*(i));
					graduation = pas*i;
					context.fillText(graduation, (x0 - 20), (y0 - i*20+4));
				}
				context.fillText(ny, (x0 +50), (y0 - 280));
				
				// Axe des abscisses
				tracer (context,x0,y0,540,y0);
				// Flèche
				tracer (context,530-3,y0-8,530+10,y0);
				tracer (context,530-3,y0+8,530+10,y0);
				
				context.textAlign = 'left';
				context.fillText(nx,  (x0 +500), (y0+30));
				
				context.lineWidth = '1.0';
				// Tracée du diagramme rectangulaire, légende de l'axe des abscisses
				for (i=0; i<y.length; i++) {
				  var echelle = pas 
					context.fillStyle = 'blue';				
					context.beginPath();
					context.rect(x0+10 + (i * largeur_barre) +5*i, y0 -1 - y[i]/echelle*20, largeur_barre, y[i]/echelle*20);
					context.closePath();
					context.stroke();
					context.fill();
					context.fillStyle = '#000';
					var mesure_texte = context.measureText(x [i]).width;
					var centrer_texte = (largeur_barre - mesure_texte)/2;
					context.fillText(x[i], x0+10 +centrer_texte + (i * largeur_barre) + 5*i, y0 + 18);
				}
			}
// tracéde trait
function tracer (ctx,x1,y1,x2,y2)  {
	ctx.beginPath();
	ctx.moveTo(x1, y1);
	ctx.lineTo(x2, y2);
	ctx.closePath();
	ctx.stroke();
}