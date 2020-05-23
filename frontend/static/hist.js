function histogramme(y,x,ny,nx) {
				var canvas = document.getElementById('diagramme');
				var context = canvas.getContext('2d');
				
			
				// Origine du repère
				context.translate(150,320);
				var x0 = 0;
				var y0 = 0;
				
				var largeur_barre = 90;
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
				var pas = 20;
				for (var i=0; i<13; i++) {
					tracer (context,x0-3,y0-20*(i),x0+3,y0-20*(i));
					graduation = pas*i;
					context.fillText(graduation, (x0 - 20), (y0 - graduation+4));
				}
				context.fillText(ny, (x0 -80), (y0 - 280));
				
				// Axe des abscisses
				tracer (context,x0,y0,420,y0);
				// Flèche
				tracer (context,410-3,y0-8,410+10,y0);
				tracer (context,410-3,y0+8,410+10,y0);
				
				context.textAlign = 'left';
				context.fillText(nx, x0 + canvas.width - 260, y0 + 60);
				
				context.lineWidth = '1.0';
				// Tracée du diagramme rectangulaire, légende de l'axe des abscisses
				for (i=0; i<y.length; i++) {
					context.fillStyle = 'grey';				
					context.beginPath();
					context.rect(x0+10 + (i * largeur_barre) +5*i, y0 -1 - y[i], largeur_barre, y[i]);
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