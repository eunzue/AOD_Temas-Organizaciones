/*** Funciones para el funcionamiento de la app **/

/* Copyright (c) 2006 Mathias Bank (http://www.mathias-bank.de)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php) 
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 * 
 * Thanks to Hinnerk Ruemenapf - http://hinnerk.ruemenapf.de/ for bug reporting and fixing.
 */
jQuery.extend({
/**
* Returns get parameters.
*
* If the desired param does not exist, null will be returned
*
* @example value = $.getURLParam("paramName");
*/ 
	getURLParam: function(strParamName){
		var strReturn = "";
		var strHref = window.location.href;
		var bFound=false;
		
		var cmpstring = strParamName + "=";
		var cmplen = cmpstring.length;

		if ( strHref.indexOf("?") > -1 ){
			var strQueryString = strHref.substr(strHref.indexOf("?")+1);
			var aQueryString = strQueryString.split("&");
			for ( var iParam = 0; iParam < aQueryString.length; iParam++ ){
				if (aQueryString[iParam].substr(0,cmplen)==cmpstring){
					var aParam = aQueryString[iParam].split("=");
					strReturn = aParam[1];
					bFound=true;
					break;
				}
				
			}
		}
		if (bFound==false) return null;
		return decodeURIComponent(strReturn);
	}
});


function tryToSelectItem(obj, txt) {
	if (obj != null) {
		for (k =0 ; k < obj.length; k++) {
			if (obj[k].value == txt) {
				obj[k].selected = true;
			}
		}
	}
}







//Función que sirve para cuando se haga over sobre una organizacion y cambie el div con más info
function organizacionOver(){
	$(".resultadosOrganizaciones .thumbnail").hover(
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').addClass("oculto");
			$('#'+id+' .back').removeClass("oculto");
//			console.log('Se entra en '+id);
		}, 
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').removeClass("oculto");
			$('#'+id+' .back').addClass("oculto");
//			console.log('Se sale de '+id);
		}
	);
}

//Función que sirve para cuando se haga over sobre un tema y cambie el div con más info
function temaOver(){
	$(".resultadosTemas .thumbnail").hover(
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').addClass("oculto");
			$('#'+id+' .back').removeClass("oculto");
//			console.log('Se entra en '+id);
		}, 
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').removeClass("oculto");
			$('#'+id+' .back').addClass("oculto");
//			console.log('Se sale de '+id);
		}
	);
}


$(document).ready(function() {
	
	var pathname = window.location.pathname;
	if (pathname=='/tema'){
		temaOver();
	}
	else if (pathname=='/organizacion'){
		organizacionOver();
	}
	
	if ((pathname.indexOf('/tema/')>-1) || (pathname.indexOf('/organizacion/')>-1)){
		$('.tablaResultadosDataset').DataTable({
			"pagingType": "simple_numbers",
			"pageLength": 20,
			"language": {
				"paginate": {
					"previous": "<<",
					"next": ">>"
				}
			}
		});
		$('.dataTables_length').remove();
		$('.dataTables_filter').remove();
		$('.dataTables_info').remove();
	}
	
	
	
} );
