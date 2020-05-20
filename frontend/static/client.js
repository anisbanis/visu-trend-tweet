var Client = {};

let search_query = document.getElementByID("search_query");
let search_button = docuement.getElementByID("search_button");


console.log('Client');

Client.ajax = function (method, url) {
	return new Promise ((resolve, reject) => {
		let xhr = new XMLHttpRequest();
		xhr.addEventListener("readystatechange", function() {
			/* requete teminée */
			if (this.readyState == 4 ) {
				if (this.status == 200)
					resolve(this. responseText);
                else
                    reject(this.status + " : " + this.responseText);
            }
        });
        xhr.open(method, url);

        xhr.send();
    })
};

Client.query = async function (params) {
	let strParam = "";
	for (var p in params ) {
		if (params.hasOwnProperty(p)) {
			strParam += "?" + p + "=" encodeURIComponent(params[p]);
		}:
	};
	
	let url = "http:/: .....tweet"
		+ strParam,
		console.log("url :",url)
		
		try {
			res = await Client.ajax("GET", url)
			return res;
			}
		catch (str) {
			alert ("ERROR")
			res= str;
		}
		return res;
};

search_buttom.addEventListener("click",function(){
	console.log("//");
	let exemple_param =("country":search_buttom.value};
	console.log(Client.query(exemple_param));
	
	});


		
	



